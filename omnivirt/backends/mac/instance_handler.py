import os
import psutil
import shutil
import signal
import subprocess
import sys
import time

from oslo_utils import uuidutils

from omnivirt.utils import constants
from omnivirt.utils import utils as omni_utils
from omnivirt.utils import objs
from omnivirt.backends.mac import qemu


class MacInstanceHandler(object):
    
    def __init__(self, conf, work_dir, instance_dir, image_dir,
                 image_record_file, logger, base_dir) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.instance_dir = instance_dir
        self.instance_record_file = os.path.join(instance_dir, 'instances.json')
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.driver = qemu.QemuDriver(self.conf, logger)
        self.running_instances = {}
        self.instance_pids = []
        self.base_dir = base_dir
        self.LOG = logger

    def list_instances(self):
        instances = omni_utils.load_json_data(self.instance_record_file)['instances']
        vm_list = []

        for instance in instances.values():
            vm = objs.Instance(name=instance['name'])
            vm.uuid = instance['uuid']
            vm.mac = instance['mac_address']
            vm.info = None
            vm.vm_state = self._check_vm_state(instance)
            if not instance['ip_address']:
                ip_address = self._parse_ip_addr(vm.mac)
                vm.ip = ip_address
            else:
                vm.ip = instance['ip_address']
            vm.image = instance['image']
            vm_list.append(vm)

        return vm_list

    def _check_vm_state(self, instance):
        if instance['identification']['type'] == 'pid':
            instance_pid = instance['identification']['id']
            if instance_pid in psutil.pids() and \
                psutil.Process(instance_pid).status() == 'running' and \
                psutil.Process(instance_pid).name().startswith('qemu'):
                return constants.VM_STATE_MAP[2]
            else:
                return constants.VM_STATE_MAP[3]
        else:
            return constants.VM_STATE_MAP[99]

    def _parse_ip_addr(self, mac_addr):
        ip = ''
        cmd = 'arp -a'
        start_time = time.time()
        while(ip == '' and time.time() - start_time < 20):
            pr = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            arp_result = pr.stdout.decode('utf-8').split('\n')
            founded = False
            for str in arp_result:
                # The result for 'arp -a' in MacOS is different with Linux, it erase
                # the first 0 if the first digit is 0 for this mac section, add it
                # back before compare
                try:
                    arp_ip = str.split(' ')[1].replace("(", "").replace(")", "")
                    mac = str.split(' ')[3].replace("(", "").replace(")", "")
                except IndexError:
                    continue
                mac_list = mac.split(':')
                for i in range(0, len(mac_list)):
                    if len(mac_list[i]) == 1:
                        mac_list[i] = '0' + mac_list[i]
                mac_0 = ':'.join(mac_list)
                if mac_addr == mac_0:
                    ip = arp_ip
                    founded = True
                    break
            if founded:
                break
        
        return ip

    def check_names(self, name, all_instances):
        try:
            all_instances['instances'][name]
            return 1
        except KeyError:
            return 0

    def create_instance(self, name, image_id, instance_record, all_instances, all_images):
        # Create dir for the instance
        vm_uuid = uuidutils.generate_uuid()
        vm_dict = {
            'name': name,
            'uuid': vm_uuid,
            'image': image_id,
            'vm_state': constants.VM_STATE_MAP[99],
            'ip_address': 'N/A',
            'mac_address': omni_utils.generate_mac(),
            'identification': {
                'type': 'pid',
                'id': None
            }
        }

        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        img_path = all_images['local'][image_id]['path']
    
        root_disk_path = shutil.copyfile(img_path, os.path.join(instance_path, image_id + '.qcow2'))

        vm_process = self.driver.create_vm(name, vm_uuid, vm_dict['mac_address'], root_disk_path)

        self.running_instances[vm_process.pid] = vm_process
        self.instance_pids.append(vm_process.pid)
        
        vm_dict['identification']['id'] = vm_process.pid

        vm_ip = self._parse_ip_addr(vm_dict['mac_address'])
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
            'vm_state': self._check_vm_state(vm_dict),
            'image': image_id,
            'ip_address': vm_dict['ip_address']
        }

    def delete_instance(self, name, instance_record, all_instances):
        # Delete instance process
        instance = all_instances['instances'][name]
        if instance['identification']['type'] == 'pid':            
            instance_pid = instance['identification']['id']
            if instance_pid in psutil.pids() and \
                psutil.Process(instance_pid).is_running():
                psutil.Process(instance_pid).kill()
                self.LOG.debug(f'Instance: {name} with PID {instance_pid} succesfully killed ...')
            else:
                self.LOG.debug(f'Instance: {name} with PID {instance_pid} already stopped, skip ...')
        else:
            self.LOG.debug(f'Instance: {name} unable to handled, skip ...')

        # Cleanup files and records
        instance_dir = instance['path']
        shutil.rmtree(instance_dir)
        del all_instances['instances'][name]

        omni_utils.save_json_data(instance_record, all_instances)

        return 0

