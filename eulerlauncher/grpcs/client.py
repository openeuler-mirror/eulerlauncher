import grpc
import os

from eulerlauncher.grpcs.eulerlauncher_grpc import images_pb2_grpc
from eulerlauncher.grpcs.eulerlauncher_grpc import instances_pb2_grpc
from eulerlauncher.grpcs.eulerlauncher_grpc import flavors_pb2_grpc
from eulerlauncher.grpcs import images, instances, flavors
from eulerlauncher.utils import constants
from eulerlauncher.utils import utils as eulerlauncher_utils


class Client(object):
    def __init__(self, channel_target=None):
        if not channel_target:
            channel_target = 'localhost:50052'
        channel = grpc.insecure_channel(channel_target)

        images_client = images_pb2_grpc.ImageGrpcServiceStub(channel)
        instances_client = instances_pb2_grpc.InstanceGrpcServiceStub(channel)
        flavors_client = flavors_pb2_grpc.FlavorGrpcServiceStub(channel)

        self._images = images.Image(images_client)
        self._instances = instances.Instance(instances_client)
        self._flavors = flavors.Flavor(flavors_client)

    @eulerlauncher_utils.response2dict
    def list_images(self, filters=None):
        """ [IMAGE] List images

        :param filters(list): None
        :return: dict -- list of images' info
        """

        return self._images.list()
    
    @eulerlauncher_utils.response2dict
    def download_image(self, name):
        """ Download image
        """

        return self._images.download(name)

    @eulerlauncher_utils.response2dict
    def load_image(self, name, path):
        """ Load local image file
        """

        if not os.path.exists(path):
            err_msg = {
                'ret': 1,
                'msg': f'No such file or directory: {path}, please check again.'
            }
            return err_msg
        
        supported = False
        for tp in constants.IMAGE_LOAD_SUPPORTED_TYPES + constants.IMAGE_LOAD_SUPPORTED_TYPES_COMPRESSED:
            if path.endswith(tp):
                supported = True
                break
        
        if not supported:
            err_msg = {
                'ret': 1,
                'msg': f'Image file format does not supported: {path}, please check again.'
            }
            return err_msg
        
        return self._images.load(name, path)

    @eulerlauncher_utils.response2dict
    def delete_image(self, name):
        """ Delete the requested image
        """

        return self._images.delete(name)

    @eulerlauncher_utils.response2dict
    def list_flavors(self, filters=None):
        """ List flavors

        :param filters(list): None
        :return: dict -- list of flavors' info
        """

        return self._flavors.list()

    @eulerlauncher_utils.response2dict
    def create_flavor(self, name, cpu, ram, disk):
        """ Create a new flavor
        """

        return self._flavors.create(name, cpu, ram, disk)

    @eulerlauncher_utils.response2dict
    def delete_flavor(self, name):
        """ Delete the requested image
        """

        return self._flavors.delete(name)

    @eulerlauncher_utils.response2dict
    def list_instances(self):
        """ List instances
        :return: dict -- list of instances' info
        """

        return self._instances.list()

    @eulerlauncher_utils.response2dict
    def create_instance(self, name, image, arch):
        """ Create instance
        :return: dict -- dict of instance's info
        """


        return self._instances.create(name, image, arch)

    @eulerlauncher_utils.response2dict
    def delete_instance(self, name):
        """ Delete the requested instance
        """

        return self._instances.delete(name)

    @eulerlauncher_utils.response2dict
    def take_snapshot(self, vm_name, snapshot_name, export_path):
        """ Take snapshot
        """

        return self._instances.take_snapshot(vm_name, snapshot_name, export_path)

    @eulerlauncher_utils.response2dict
    def export_development_image(self, vm_name, image_name, export_path, pwd):
        """ Export Python/Go/Java development image
        """

        return self._instances.export_development_image(vm_name, image_name, export_path, pwd)