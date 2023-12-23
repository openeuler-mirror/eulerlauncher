import configparser
import os
import random
import time

from eulerlauncher.utils import exceptions
from eulerlauncher.utils import constants

class Instance(object):

    def __init__(self, name='') -> None:
        self.name = name
        self.uuid = ''
        self.identifier = {}
        self.metadata = None
        self.vm_state = None
        self.vcpu = None
        self.ram = None
        self.disk = None
        self.info = None
        self.image = None
        self.ip = 'N/A'
        self.mac = 'N/A'


class Image(object):
    
    def __init__(self) -> None:
        self.name = ''
        self.location = ''
        self.status = constants.IMAGE_STATUS_INIT
        self.path = ''
    
    def to_dict(self):
        image_dict = {
            'name': self.name,
            'location': self.location,
            'status': self.status,
            'path': self.path
        }
        return image_dict
    
    def from_dict(self, img_dict):
        self.name = img_dict['name']
        self.location = img_dict['location']
        self.status = img_dict['status']
        self.path = img_dict['path']


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


class Conf(object):

    def __init__(self, config_file) -> None:
        self.conf = configparser.ConfigParser()
        if not os.path.exists(config_file):
            raise exceptions.NoSuchFile(file=config_file)
        self.conf.read(config_file)
