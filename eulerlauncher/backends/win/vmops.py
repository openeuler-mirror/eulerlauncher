import json
import psutil
import random
import subprocess
import time


from os_win import constants as os_win_const
from os_win import exceptions as os_win_exc
from os_win.utils.compute import vmutils10
from os_win import utilsfactory
from oslo_utils import uuidutils

from eulerlauncher.utils import objs
from eulerlauncher.utils import constants
from eulerlauncher.utils import utils as omni_utils
from eulerlauncher.backends.win import powershell

SWITCH_NAME = 'Default Switch'


class VMUtils_omni(vmutils10.VMUtils10):

    def __init__(self) -> None:
        super().__init__()

    def get_instance_notes(self, instance_name):
        instance_notes = self._get_instance_notes(instance_name)
        return instance_notes
    
    def get_vm_nic_uids(self, vm_name):
        nics = self._get_vm_nics(vm_name)
        return nics

class Flavor(object):
    def __init__(self, flavor_name, cpucores_num, ram_capacity, disk_capacity, flavor_id=None):
        self.flavor_id = flavor_id or self.generate_unique_id()  # 初始化虚拟机规格的唯一ID
        self.flavor_name = flavor_name  # 虚拟机规格名称
        self.cpucores_num = str(cpucores_num)  # CPU核心数（转换为字符串类型）
        self.ram_capacity = ram_capacity  # 内存大小（MB）
        self.disk_capacity = disk_capacity  # 磁盘大小（GB）

    def generate_unique_id(self):
        # 生成唯一ID的方法，使用时间戳和随机数结合
        timestamp = int(time.time() * 1000)  # 当前时间的毫秒级别时间戳
        random_part = random.randint(0, 1000)  # 0到1000之间的随机数
        return f'{timestamp}-{random_part}'

    def to_dict(self):
        # 将Flavor对象转换为字典
        return {
            'flavor_id': self.flavor_id,
            'flavor_name': self.flavor_name,
            'cpucores_num': self.cpucores_num,
            'ram_capacity': self.ram_capacity,
            'disk_capacity': self.disk_capacity
        }

    @classmethod
    def from_dict(cls, data):
        # 从字典创建Flavor对象的类方法
        return cls(data['flavor_name'], int(data['cpucores_num']), data['ram_capacity'], data['disk_capacity'],
                   data.get('flavor_id'))


class VMOps(object):
    _ROOT_DISK_CTRL_ADDR = 0

    def __init__(self, virtapi=None):
        self._virtapi = virtapi
        self._vmutils = VMUtils_omni()
        self._migrationutils = utilsfactory.get_migrationutils()
        self._netutils = utilsfactory.get_networkutils()
        self._hostutils = utilsfactory.get_hostutils()

    def _set_vm_state(self, instance, req_state):
        instance_name = instance.name
        self._vmutils.set_vm_state(instance_name, req_state)

    def list_instance_uuids(self):
        instance_uuids = []
        for (instance_name, notes) in self._vmutils.list_instance_notes():
            if notes and uuidutils.is_uuid_like(notes[0]):
                instance_uuids.append(str(notes[0]))
            else:
                pass
                #LOG.debug("Notes not found or not resembling a GUID for "
                #          "instance: %s", instance_name)
        return instance_uuids

    def check_all_instance_names(self, name):
        instance_names =  self._vmutils.list_instances()
        if name in instance_names:
            return 1
        else:
            return 0

    def list_instances(self):
        instance_names =  self._vmutils.list_instances()
        vm_list = []
        for instance_name in instance_names:
            vm = objs.Instance(name=instance_name)
            meta = self.get_meta(instance_name)
            if not meta or not meta['creator'] == 'eulerlauncher':
                continue
            else:
                vm.metadata = meta
                vm.uuid = meta['uuid']
                info = self.get_info(instance_name)
                vm.info = info
                vm.vm_state = constants.VM_STATE_MAP[info['EnabledState']]
                ip_address = self.get_instance_ip_addr(instance_name)
                vm.ip = ip_address
                vm.image = meta['image']
                vm_list.append(vm)

        return vm_list


    def get_instance_ip_addr(self, instance_name):
        nic_name = instance_name + '_eth0'
        nic = self.get_vm_nics(instance_name, nic_name)
        mac_address = omni_utils.format_mac_addr(nic.Address)
        with powershell.PowerShell('GBK') as ps:
            outs, errs = ps.run('arp -a | findstr /i {}'.format(mac_address))
        ip_address = outs.strip(' ').split(' ')[0]

        return ip_address

    
    def get_info(self, instance):
        """Get information about the VM."""
        # LOG.debug("get_info called for instance", instance=instance)

        instance_name = instance
        if not self._vmutils.vm_exists(instance_name):
            raise # exception.InstanceNotFound(instance_id=instance.uuid)

        info = self._vmutils.get_vm_summary_info(instance_name)

        return info

    def create_flavor(self, flavor_name, cpucores_num, ram_capacity, disk_capacity):
        # 创建虚拟机规格
        flavor = Flavor(flavor_name, cpucores_num, ram_capacity, disk_capacity)
        self.save_flavor(flavor)

    def delete_flavor(self, flavor_id):
        # 删除虚拟机规格
        flavors = self.load_flavors()
        flavor_to_delete = None

        # 查找要删除的虚拟机规格
        for flavor in flavors:
            if flavor.flavor_id == flavor_id:
                flavor_to_delete = flavor
                break

        if flavor_to_delete:
            flavors.remove(flavor_to_delete)
            self.save_flavors(flavors)
            print(f"Flavor with flavor_id {flavor_id} has been deleted.")
        else:
            print(f"Flavor with flavor_id {flavor_id} not found.")

    def save_flavor(self, flavor):
        # 将Flavor对象保存到配置文件
        flavors = self.load_flavors()
        flavors.append(flavor.to_dict())
        with open('flavors.json', 'w') as f:
            json.dump(flavors, f)

    def load_flavors(self):
        try:
            # 从配置文件加载Flavor对象列表
            with open('flavors.json', 'r') as f:
                data = json.load(f)
                return [Flavor.from_dict(item) for item in data]
        except FileNotFoundError:
            return []  # 如果配置文件不存在，返回空列表

    def print_all_flavors(self):
        flavors = self.load_flavors()
        if not flavors:
            print("No virtual machine flavors found.")
            return

        print("All Virtual Machine Flavors:")
        for flavor in flavors:
            print(f"Flavor ID: {flavor.flavor_id}")
            print(f"Flavor Name: {flavor.flavor_name}")
            print(f"CPU Cores: {flavor.cpucores_num}")
            print(f"RAM Capacity: {flavor.ram_capacity} MB")
            print(f"Disk Capacity: {flavor.disk_capacity} GB")
            print("-------------")

    def create_vm(self, vm_name, vnuma_enabled, vm_gen, instance_path,
                  meta_data):
        self._vmutils.create_vm(vm_name,
                                vnuma_enabled,
                                vm_gen,
                                instance_path,
                                [json.dumps(meta_data)])

    def build_and_run_vm(self, vm_name, uuid, image_name, vnuma_enabled, vm_gen, instance_path, root_disk_path, flavor):
        meta_data = {
            'uuid': uuid,
            'image': image_name,
            'creator': 'eulerlauncher'
        }

        # Create an instance
        self.create_vm(vm_name, vnuma_enabled, vm_gen, instance_path, meta_data)
        # Create a scsi controller for this instance
        self._vmutils.create_scsi_controller(vm_name)
        # 创建规定大小的磁盘文件
        # 创建一个VHDUtils实例
        vhd_utils = VHDUtils()
        # 调用create_vhd方法
        vhd_utils.create_vhd(root_disk_path, constants.VHD_TYPE_FIXED,
                             max_internal_size=flavor.disk_capacity * 1024 * 1024 * 1024)
        # Attach the root disk to the driver
        self.attach_disk(vm_name, root_disk_path, constants.DISK)
        # 设置虚拟机的 CPU、内存
        self._vmutils.update_vm(vm_name, flavor.ram_capacity, 0, flavor.cpucores_num, 0, False, 0)
        # Start the instance
        self.power_up(vm_name)
        nic_name = vm_name + '_eth0'
        self.add_nic(vm_name, nic_name)
        self.connect_vnic_to_switch(SWITCH_NAME, nic_name)
        return 0

    def get_meta(self, instance_name, expect_existing=False):
        try:
            instance_notes = self._vmutils.get_instance_notes(instance_name)
            if instance_notes:
                return json.loads(instance_notes[0])
            else:
                return instance_notes
        except os_win_exc.HyperVVMNotFoundException:
            raise

    def delete_instance(self, vm_name):
        # Stop the VM first.
        self._vmutils.stop_vm_jobs(vm_name)
        self._vmutils.set_vm_state(vm_name, os_win_const.HYPERV_VM_STATE_DISABLED)
        self._vmutils.destroy_vm(vm_name)

        while(1):
            if not self._vmutils.vm_exists(vm_name):
                break
        return 0

    def get_vm_disks(self, vm_name):
        return self._vmutils.get_vm_disks(vm_name)

    def attach_disk(self, instance_name, path, drive_type):
        self._vmutils.attach_scsi_drive(instance_name, path, drive_type)
    
    def power_up(self, instance_name):
        req_state = os_win_const.HYPERV_VM_STATE_ENABLED
        self._vmutils.set_vm_state(instance_name, req_state)
    
    def add_nic(self, instance_name, nic_name):
        self._vmutils.create_nic(instance_name, nic_name)
    
    def get_vm_nics(self, instance_name, nic_name):
        return self._vmutils._get_nic_data_by_name(nic_name)
    
    def list_switch_ports(self, switch_name):
        return self._netutils.get_switch_ports(switch_name)
    
    def connect_vnic_to_switch(self, switch_name, vnic_name):
        self._netutils.connect_vnic_to_vswitch(switch_name, vnic_name)
    
    def get_switch_port(self, switch_name, port_id):
        return self._netutils.get_port_by_id(port_id, switch_name)
    
    def get_host_ips(self):
        return self._hostutils.get_local_ips()

    def take_snapshot(self, vm_name, snapshot_name):
        self._vmutils.take_vm_snapshot(vm_name, snapshot_name)

    def export_vm(self, vm_name, dest_path):
        self._migrationutils.export_vm(vm_name, dest_path, copy_snapshots_config=os_win_const.EXPORT_CONFIG_NO_SNAPSHOTS, copy_vm_storage=True, create_export_subdir=True)

    def parse_ip_addr(self, mac_addr):
        ip = ''
        macs = mac_addr.split(':')
        mac_addr1 = '-'.join(macs)
        cmd = f'arp -a|findstr {mac_addr1}'
        start_time = time.time()
        while (ip == '' and time.time() - start_time < 30):
            pr = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            arp_result = pr.stdout.decode('gbk').strip()
            founded = False
            if arp_result:
                # The result for 'arp -a' in MacOS is different with Linux, it erase
                # the first 0 if the first digit is 0 for this mac section, add it
                # back before compare
                try:
                    arp_ip = arp_result.split()[0]
                    mac = arp_result.split()[1]
                except IndexError:
                    continue
                if mac_addr1 == mac:
                    ip = arp_ip
                    founded = True
            if founded:
                break

        return ip

    def check_vm_state(self, instance):
        if instance['identification']['type'] == 'pid':
            instance_pid = instance['identification']['id']
            if instance_pid in psutil.pids() and \
                psutil.Process(instance_pid).status() == 'running':
                children = psutil.Process(instance_pid).children(recursive=True)
                for chird in children:
                    if chird.name().startswith('qemu') and chird.is_running():
                        return constants.VM_STATE_MAP[2]
            return constants.VM_STATE_MAP[3]
        else:
            return constants.VM_STATE_MAP[99]
