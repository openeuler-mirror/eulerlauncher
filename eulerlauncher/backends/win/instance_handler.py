import os
import shutil
import time
import paramiko
from glob import glob
import psutil

from oslo_utils import uuidutils
from os_win import constants as os_win_const
from os_win import exceptions as os_win_exc

from eulerlauncher.backends.win import powershell
from eulerlauncher.backends.win import vmops
from eulerlauncher.utils import constants
from eulerlauncher.utils import utils as omni_utils
from eulerlauncher.utils import objs
from eulerlauncher.backends.win import qemu



_vmops = vmops.VMOps()

class WinInstanceHandler(object):
    
    def __init__(self, conf, work_dir, instance_dir, image_dir, image_record_file, logger, base_dir) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.instance_dir = instance_dir
        self.instance_record_file = os.path.join(instance_dir, 'instances.json')
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger
        self.driver = qemu.QemuDriver(self.conf, logger)
        self.running_instances = {}
        self.instance_pids = []
        self.base_dir = base_dir
        self.pattern = conf.conf.get('default', 'pattern')

    # def list_instances(self):
    #     vms = _vmops.list_instances()
    #     return vms
    
    def check_names(self, name, all_instances):
        ret = _vmops.check_all_instance_names(name)
        return ret


    def list_instances(self):

        instances = omni_utils.load_json_data(self.instance_record_file)['instances']
        vm_list = []

        if self.pattern == 'qemu':
            for instance in instances.values():
                vm = objs.Instance(name=instance['name'])
                vm.uuid = instance['uuid']
                vm.mac = instance['mac_address']
                vm.info = None
                vm.vm_state = _vmops.check_vm_state(instance)
                if vm.vm_state == constants.VM_STATE_MAP[2] and (not instance['ip_address'] or instance['ip_address'] == 'N/A'):
                    ip_address = _vmops.parse_ip_addr(vm.mac)
                    vm.ip = ip_address
                else:
                    vm.ip = instance['ip_address']
                vm.image = instance['image']
                vm_list.append(vm)
        elif self.pattern == 'hyper-v':
            vm_list = _vmops.list_instances()
        return vm_list

    def create_instance(self, name, image_id, instance_record, all_instances, all_images, is_same, mac_address, uuid, arch='x86'):
        # Create dir for the instance
        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        img_path = all_images['local'][image_id]['path']

        root_disk_path = shutil.copyfile(img_path, os.path.join(instance_path, image_id + '.qcow2')) if self.pattern == 'qemu' \
            else shutil.copyfile(img_path, os.path.join(instance_path, image_id + '.vhdx'))
        vm_ip = ''
        vm_dict = {
            'name': name,
            'uuid': uuidutils.generate_uuid(),
            'image': image_id,
            'vm_state': constants.VM_STATE_MAP[99],
            'ip_address': 'N/A',
            'mac_address': omni_utils.generate_mac() if self.pattern == 'qemu' else 'N/A',
            'identification': {'type': 'pid','id': None} if self.pattern == 'qemu' else {'type': 'name','id': name}
        }
        if self.pattern == 'qemu':
            vm_uuid = uuidutils.generate_uuid()
            vm_process = self.driver.create_vm(name, vm_uuid, vm_dict['mac_address'], root_disk_path, arch)
            self.running_instances[vm_process.pid] = vm_process
            #self.LOG.debug(vm_process.returncode)
            #self.LOG.debug(vm_process.pid)
            self.instance_pids.append(vm_process.pid)
            vm_dict['identification']['id'] = vm_process.pid
            vm_ip = _vmops.parse_ip_addr(vm_dict['mac_address'])
        elif self.pattern == 'hyper-v':
            _vmops.build_and_run_vm(name, vm_dict['uuid'], image_id, False, 2, instance_path, root_disk_path)
            info = _vmops.get_info(name)
            vm_dict['vm_state'] = constants.VM_STATE_MAP[info['EnabledState']]
            vm_ip = _vmops.get_instance_ip_addr(name)
        if vm_ip:
            vm_dict['ip_address'] = vm_ip
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
            'vm_state': _vmops.check_vm_state(vm_dict) if self.pattern == 'qemu' else vm_dict['vm_state'],
            'image': image_id,
            'ip_address': vm_dict['ip_address']
        }


    def delete_instance(self, name, instance_record, all_instances):
        # Delete instance process
        instance = all_instances['instances'][name]
        if self.pattern == 'qemu':
            processes = []
            if instance['identification']['type'] == 'pid':
                instance_pid = instance['identification']['id']
                if instance_pid in psutil.pids():
                    processes = psutil.Process(instance_pid).children(recursive=True)
                    processes.append(psutil.Process(instance_pid))
                for child in processes:
                    if child.pid in psutil.pids() and \
                        child.is_running():
                        child.kill()
                        self.LOG.debug(f'Instance: {child.name()} with PID {child.pid} succesfully killed ...')
                    else:
                        self.LOG.debug(f'Instance: {child.name()} with PID {child.pid} already stopped, skip ...')

            else:
                self.LOG.debug(f'Instance: {name} unable to handled, skip ...')
        elif self.pattern == 'hyper-v':
            _vmops.delete_instance(name)
        # Cleanup files and records
        instance_dir = instance['path']
        if os.path.exists(instance_dir):
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

    def take_snapshot(self, name, snapshot_name, dest_path, all_instances, all_images, instance_record):
        _vmops.take_snapshot(name, snapshot_name)
        _vmops.export_vm(name, os.path.join(dest_path))
        os.rename(glob(os.path.join(dest_path, name, 'Virtual Hard Disks', '*.vhdx'))[0], os.path.join(dest_path, name, 'Virtual Hard Disks', f'{snapshot_name}.vhdx'))
        shutil.move(os.path.join(dest_path, name, 'Virtual Hard Disks', f'{snapshot_name}.vhdx'), os.path.join(dest_path))
        # remove the exported file dir
        shutil.rmtree(os.path.join(dest_path, name))
        return os.path.join(dest_path, f'{snapshot_name}.vhdx')

    def make_development_image(self, name, pwd):
        ssh_client = paramiko.SSHClient()
        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(_vmops.get_instance_ip_addr(name), 22, "root", pwd)
            bash_command = """
            if which apt >/dev/null 2>&1;
                then apt install python3-dev golang openjdk-11-jdk
            elif which yum >/dev/null 2>&1;
                then yum install -y python3-devel golang java-11-openjdk-devel
            elif which dnf >/dev/null 2>&1;
                then dnf install -y python3-devel golang java-11-openjdk-devel
            fi
            """
            stdin, stdout, stderr = ssh_client.exec_command(bash_command)

            self.LOG.debug(stdout.read().decode())
            ssh_client.close()
            return 0
        except Exception as e:
            self.LOG.debug(f"install development environment failed: {str(e)}")
            return 1