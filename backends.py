import json
import time
import random

from os_win import constants as os_win_const
from os_win import exceptions as os_win_exc
from os_win.utils.compute import vmutils10
from os_win import utilsfactory
from oslo_utils import uuidutils

from eulerlauncher.utils import objs
from eulerlauncher.utils import constants
from eulerlauncher.utils import utils as omni_utils
from eulerlauncher.backends.win import powershell
from os_win.utils.storage.virtdisk import VHDUtils

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


class VMOps(object):
    _ROOT_DISK_CTRL_ADDR = 0

    def __init__(self, virtapi=None):
        self._virtapi = virtapi
        self._vmutils = VMUtils_omni()
        self._netutils = utilsfactory.get_networkutils()
        self._hostutils = utilsfactory.get_hostutils()

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


    def create_vm(self, vm_name, vnuma_enabled, vm_gen, instance_path, meta_data):
        # 创建虚拟机
        self._vmutils.create_vm(vm_name,
                                vnuma_enabled,
                                vm_gen,
                                instance_path,
                                [json.dumps(meta_data)])

    def build_and_run_vm(self, vm_name, uuid, image_name, vnuma_enabled, vm_gen, instance_path, root_disk_path, flavor):
        # 指定规格创建并启动虚拟机
        meta_data = {
            'uuid': uuid,
            'image': image_name,
            'creator': 'eulerlauncher'
        }

        # 使用传入的虚拟机规格创建虚拟机
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


    def delete_instance(self, vm_name):
        # 删除虚拟机
        # Stop the VM first.
        self._vmutils.stop_vm_jobs(vm_name)
        self._vmutils.set_vm_state(vm_name, os_win_const.HYPERV_VM_STATE_DISABLED)
        self._vmutils.destroy_vm(vm_name)

        while (1):
            if not self._vmutils.vm_exists(vm_name):
                break
        return 0

    def get_vm_disks(self, vm_name):
        return self._vmutils.get_vm_disks(vm_name)

    def attach_disk(self, instance_name, path, drive_type):
        # 挂载磁盘
        self._vmutils.attach_scsi_drive(instance_name, path, drive_type)

    def power_up(self, instance_name):
        # 启动虚拟机
        req_state = os_win_const.HYPERV_VM_STATE_ENABLED
        self._vmutils.set_vm_state(instance_name, req_state)

    def start_vm(self, vm_name):
        # 启动虚拟机并连接网络
        self.power_up(vm_name)

        # 添加并配置网络适配器
        nic_name = vm_name + '_eth0'
        self.add_nic(vm_name, nic_name)

        # 连接虚拟机的网络适配器到指定的交换机
        self.connect_vnic_to_switch(SWITCH_NAME, nic_name)

    def stop_vm(self, vm_name):
        # 停止虚拟机
        self._vmutils.soft_shutdown_vm(vm_name)

    def detach_disk(self, vm_name, disk_path=None, is_physical=True, serial=None):
        # 卸载虚拟机磁盘，如果不传入disk_path的话则默认会分离所有磁盘资源
        self._vmutils.detach_vm_disk(vm_name, disk_path, is_physical, serial)

    def add_nic(self, instance_name, nic_name):
        # 添加并配置网络适配器
        self._vmutils.create_nic(instance_name, nic_name)

    def get_vm_nics(self, instance_name, nic_name):
        # 获取虚拟机的网络适配器
        return self._vmutils._get_nic_data_by_name(nic_name)


    def connect_vnic_to_switch(self, switch_name, vnic_name):
        # 连接虚拟机的网络适配器到指定的交换机
        self._netutils.connect_vnic_to_vswitch(switch_name, vnic_name)


