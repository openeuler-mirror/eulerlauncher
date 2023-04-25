import os
import configparser

from omnivirt.utils import exceptions
from omnivirt.utils import constants

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


class Conf(object):

    def __init__(self, config_file) -> None:
        self.conf = configparser.ConfigParser()
        if not os.path.exists(config_file):
            raise exceptions.NoSuchFile(file=config_file)
        self.conf.read(config_file)
