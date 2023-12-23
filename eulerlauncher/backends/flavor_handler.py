import json
import ssl

from eulerlauncher.utils.objs import Flavor


ssl._create_default_https_context = ssl._create_unverified_context


class FlavorHandler(object):
    
    def __init__(self, conf, work_dir, flavor_dir, flavor_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.flavor_dir = flavor_dir
        self.flavor_record_file = flavor_record_file
        self.LOG = logger
    
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
        with open(self.flavor_record_file, 'w') as f:
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