import os
import psutil
import shutil
import signal
import subprocess
import sys
import time
import paramiko

from oslo_utils import uuidutils

from eulerlauncher.utils import constants
from eulerlauncher.utils import utils as omni_utils
from eulerlauncher.utils import objs
from eulerlauncher.backends.mac import qemu


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

    def create_instance(self, name, image_id, instance_record, all_instances, all_images, is_same, mac_address, uuid, arch='x86'):
        # Create dir for the instance
        if not is_same:
            vm_uuid = uuidutils.generate_uuid()
            vm_mac_address = omni_utils.generate_mac()
        else:
            vm_uuid = uuid
            vm_mac_address = mac_address
        vm_dict = {
            'name': name,
            'uuid': vm_uuid,
            'image': image_id,
            'vm_state': constants.VM_STATE_MAP[99],
            'ip_address': 'N/A',
            'mac_address': vm_mac_address,
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

    def _get_vm_img_id_by_name(self, name):
        instance = omni_utils.load_json_data(self.instance_record_file)['instances'][name]
        return instance['image']

    def take_snapshot(self, name, snapshot_name, dest_path, all_instances, all_images, instance_record):
        vm_img_id = self._get_vm_img_id_by_name(name)
        vm_root_disk_src_path = os.path.join(self.instance_dir, name, vm_img_id + '.qcow2')
        vm_root_disk_dst_path = os.path.join(self.instance_dir, vm_img_id + '.qcow2')
        mac_address = all_instances['instances'][name]['mac_address']
        vm_uuid = all_instances['instances'][name]['uuid']
        # shutdown the vm first for taking snapshot
        shutil.copyfile(vm_root_disk_src_path, vm_root_disk_dst_path)
        self.delete_instance(name, instance_record, all_instances)
        self.driver.take_and_export_snapshot(snapshot_name, vm_root_disk_dst_path, snapshot_name, dest_path)
        # a little hack here, since the running vm's image is already deleted, change the local image path to the copyed image path
        all_images['local'][vm_img_id]['path'] = vm_root_disk_dst_path
        self.create_instance(name, vm_img_id, instance_record, all_instances, all_images, True, mac_address, vm_uuid, 'x86')
        os.remove(vm_root_disk_dst_path)
        return os.path.join(dest_path, f'{snapshot_name}.qcow2')

    def _get_vm_ip_by_name(self, name):
        instance = omni_utils.load_json_data(self.instance_record_file)['instances'][name]
        if not instance['ip_address']:
            ip_address = self._parse_ip_addr(instance['mac_address'])
        else:
            ip_address = instance['ip_address']
        return ip_address

    def make_development_image(self, name, pwd):
        ssh_client = paramiko.SSHClient()
        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self._get_vm_ip_by_name(name), 22, "root", pwd)
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