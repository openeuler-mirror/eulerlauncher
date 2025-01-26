import grpc

from eulerlauncher.grpcs.eulerlauncher_grpc import images_pb2, images_pb2_grpc
from eulerlauncher.grpcs.eulerlauncher_grpc import instances_pb2, instances_pb2_grpc
from eulerlauncher.grpcs import images, instances
from eulerlauncher.utils import utils


class Client(object):
    def __init__(self, channel_target=None):
        if not channel_target:
            channel_target = 'localhost:50052'
        channel = grpc.insecure_channel(channel_target)

        images_client = images_pb2_grpc.ImageGrpcServiceStub(channel)
        instances_client = instances_pb2_grpc.InstanceGrpcServiceStub(channel)

        self._images = images.Image(images_client)
        self._instances = instances.Instance(instances_client)


    @utils.response2dict
    def list_images(self, filters=None):
        """ [IMAGE] List images

        :param filters(list): None
        :return: dict -- list of images' info
        """

        return self._images.list()
    

    @utils.response2dict
    def download_image(self, name):
        """ Download image
        """

        return self._images.download(name)


    @utils.response2dict
    def load_image(self, name, path):
        """ Load local image file
        """
        
        return self._images.load(name, path)


    @utils.response2dict
    def delete_image(self, name):
        """ Delete the requested image
        """

        return self._images.delete(name)


    @utils.response2dict
    def list_instances(self):
        """ List instances
        :return: dict -- list of instances' info
        """

        return self._instances.list()


    @utils.response2dict
    def create_instance(self, name, image):
        """ Create instance
        :return: dict -- dict of instance's info
        """

        return self._instances.create(name, image)


    @utils.response2dict
    def delete_instance(self, name):
        """ Delete the requested instance
        """

        return self._instances.delete(name)
    
    @utils.response2dict
    def suspend_instance(self, name):
        """ Suspend the requested instance
        """

        return self._instances.suspend(name)
    
    @utils.response2dict
    def resume_instance(self, name):
        """ Resume the requested instance
        """

        return self._instances.resume(name)


    @utils.response2dict
    def console_instance(self, name):
        """ connect the requested instance
        """

        return self._instances.console(name)