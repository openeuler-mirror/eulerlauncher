import os
import shutil
import time

from oslo_utils import uuidutils
from os_win import constants as os_win_const
from os_win import exceptions as os_win_exc

from omnivirt.backends.win import powershell
from omnivirt.backends.win import vmops
from omnivirt.utils import constants
from omnivirt.utils import utils as omni_utils
from omnivirt.utils import objs


_vmops = vmops.VMOps()

class WinInstanceHandler(object):
    
    def __init__(self, conf, work_dir, instance_dir, image_dir, image_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.instance_dir = instance_dir
        self.instance_record_file = os.path.join(instance_dir, 'instances.json')
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger

    def list_instances(self):
        vms = _vmops.list_instances()
        return vms
    
    def check_names(self, name, all_instances):
        ret = _vmops.check_all_instance_names(name)
        return ret
    
    def create_instance(self, name, image_id, instance_record, all_instances, all_images):
        # Create dir for the instance
        vm_dict = {
            'name': name,
            'uuid': uuidutils.generate_uuid(),
            'image': image_id,
            'vm_state': constants.VM_STATE_MAP[99],
            'ip_address': 'N/A',
            'mac_address': 'N/A',
            'identification': {
                'type': 'name',
                'id': name
            }
        }

        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        img_path = all_images['local'][image_id]['path']
    
        root_disk_path = shutil.copyfile(img_path, os.path.join(instance_path, image_id + '.vhdx'))
        _vmops.build_and_run_vm(name, vm_dict['uuid'], image_id, False, 2, instance_path, root_disk_path)

        info = _vmops.get_info(name)
        vm_dict['vm_state'] = constants.VM_STATE_MAP[info['EnabledState']]
        ip = _vmops.get_instance_ip_addr(name)
        if ip: 
            vm_dict['ip_address'] = ip
        
        instance_record_dict = {
            'name': name,
            'uuid': vm_dict['uuid'],
            'image': image_id,
            'path': instance_path,
            'mac_address': vm_dict['mac_address'],
            'ip_address': vm_dict['ip_address'],
            'identification': vm_dict['identification']
        }

        all_instances['instances'][name] = instance_record_dict
        omni_utils.save_json_data(instance_record, all_instances)

        return {
            'name': name,
            'vm_state': vm_dict['vm_state'],
            'image': image_id,
            'ip_address': vm_dict['ip_address']
        }
    
    def delete_instance(self, name, instance_record, all_instances):
        # Delete instance
        _vmops.delete_instance(name)

        # Cleanup files and records
        instance_dir = all_instances['instances'][name]['path']
        shutil.rmtree(instance_dir)
        del all_instances['instances'][name]

        omni_utils.save_json_data(instance_record, all_instances)

        return 0

    def reboot(self, instance, reboot_type='soft'):
        """Reboot the specified instance."""
        self.LOG.debug("Rebooting instance", instance=instance)

        if reboot_type == 'soft':
            if self._soft_shutdown(instance):
                self.power_on(instance)
                return

        self._set_vm_state(instance,
                           os_win_const.HYPERV_VM_STATE_REBOOT)

    def _soft_shutdown(self, instance,
                       timeout=5,
                       retry_interval=1):
        """Perform a soft shutdown on the VM.

           :return: True if the instance was shutdown within time limit,
                    False otherwise.
        """
        self.LOG.debug("Performing Soft shutdown on instance", instance=instance)

        while timeout > 0:
            # Perform a soft shutdown on the instance.
            # Wait maximum timeout for the instance to be shutdown.
            # If it was not shutdown, retry until it succeeds or a maximum of
            # time waited is equal to timeout.
            wait_time = min(retry_interval, timeout)
            try:
                self.LOG.debug("Soft shutdown instance, timeout remaining: %d",
                          timeout, instance=instance)
                self._vmutils.soft_shutdown_vm(instance.name)
                if self._wait_for_power_off(instance.name, wait_time):
                    self.LOG.info("Soft shutdown succeeded.",
                             instance=instance)
                    return True
            except os_win_exc.HyperVException as e:
                # Exception is raised when trying to shutdown the instance
                # while it is still booting.
                self.LOG.debug("Soft shutdown failed: %s", e, instance=instance)
                time.sleep(wait_time)

            timeout -= retry_interval

        self.LOG.warning("Timed out while waiting for soft shutdown.",
                    instance=instance)
        return False

    def pause(self, instance):
        """Pause VM instance."""
        self.LOG.debug("Pause instance", instance=instance)
        self._set_vm_state(instance,
                           os_win_const.HYPERV_VM_STATE_PAUSED)

    def unpause(self, instance):
        """Unpause paused VM instance."""
        self.LOG.debug("Unpause instance", instance=instance)
        self._set_vm_state(instance,
                           os_win_const.HYPERV_VM_STATE_ENABLED)

    def suspend(self, instance):
        """Suspend the specified instance."""
        self.LOG.debug("Suspend instance", instance=instance)
        self._set_vm_state(instance,
                           os_win_const.HYPERV_VM_STATE_SUSPENDED)

    def resume(self, instance):
        """Resume the suspended VM instance."""
        self.LOG.debug("Resume instance", instance=instance)
        self._set_vm_state(instance,
                           os_win_const.HYPERV_VM_STATE_ENABLED)

    def power_off(self, instance, timeout=0, retry_interval=0):
        """Power off the specified instance."""
        self.LOG.debug("Power off instance", instance=instance)

        # We must make sure that the console log workers are stopped,
        # otherwise we won't be able to delete or move the VM log files.
        self._serial_console_ops.stop_console_handler(instance.name)

        if retry_interval <= 0:
            retry_interval = SHUTDOWN_TIME_INCREMENT

        try:
            if timeout and self._soft_shutdown(instance,
                                               timeout,
                                               retry_interval):
                return

            self._set_vm_state(instance,
                               os_win_const.HYPERV_VM_STATE_DISABLED)
        except os_win_exc.HyperVVMNotFoundException:
            # The manager can call the stop API after receiving instance
            # power off events. If this is triggered when the instance
            # is being deleted, it might attempt to power off an unexisting
            # instance. We'll just pass in this case.
            self.LOG.debug("Instance not found. Skipping power off",
                      instance=instance)

    def power_on(self, instance):
        """Power on the specified instance."""
        self.LOG.debug("Power on instance", instance=instance)
        self._set_vm_state(instance, os_win_const.HYPERV_VM_STATE_ENABLED)
