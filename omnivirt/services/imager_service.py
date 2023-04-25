import logging
import os

from omnivirt.backends.mac import image_handler as mac_image_handler
from omnivirt.backends.win import image_handler as win_image_handler
from omnivirt.grpcs.omnivirt_grpc import images_pb2, images_pb2_grpc
from omnivirt.utils import constants as omni_constants
from omnivirt.utils import utils as omni_utils


LOG = logging.getLogger(__name__)


class ImagerService(images_pb2_grpc.ImageGrpcServiceServicer):
    '''
    The Imager GRPC Handler
    '''

    def __init__(self, arch, host_os, conf, svc_base_dir) -> None:
        self.CONF = conf
        self.svc_base_dir = svc_base_dir
        self.work_dir = self.CONF.conf.get('default', 'work_dir')
        self.image_dir = os.path.join(self.work_dir, 'images')
        self.img_record_file = os.path.join(self.image_dir, 'images.json')
        if host_os == 'Win':
            self.backend = win_image_handler.WinImageHandler(
                self.CONF, self.work_dir, self.image_dir, self.img_record_file, LOG)
        elif host_os == 'MacOS':
            self.backend = mac_image_handler.MacImageHandler(
                self.CONF, self.work_dir, self.image_dir, self.img_record_file,
                LOG, self.svc_base_dir)

    def list_images(self, request, context):
        LOG.debug(f"Get request to list images ...")
        all_images = omni_utils.load_json_data(self.img_record_file)

        ret = []
        for _, images in all_images.items():
            for _, img in images.items():
                image = images_pb2.Image()
                image.name = img['name']
                image.location = img['location']
                image.status = img['status']
                ret.append(image)
        LOG.debug(f"Responded: {ret}")
        return images_pb2.ListImageResponse(images=ret)
    
    def download_image(self, request, context):
        LOG.debug(f"Get request to download image: {request.name} ...")
        all_images = omni_utils.load_json_data(self.img_record_file)
        
        if request.name not in all_images['remote'].keys():
            LOG.debug(f'Image: {request.name} not valid for download')
            msg = f'Error: Image {request.name} is valid for download, please check image name from REMOTE IMAGE LIST using "images" command ...'
            return images_pb2.GeneralImageResponse(ret=1, msg=msg)
        
        @omni_utils.asyncwrapper
        def do_download(images, name):
            self.backend.download_and_transform(images, name)
        
        do_download(all_images, request.name)

        msg = f'Downloading: {request.name}, this might take a while, please check image status with "images" command.'
        return images_pb2.GeneralImageResponse(ret=0, msg=msg)

    def load_image(self, request, context):
        LOG.debug(f"Get request to load image: {request.name} from path: {request.path} ...")

        supported, fmt = omni_utils.check_file_tail(
            request.path, omni_constants.IMAGE_LOAD_SUPPORTED_TYPES)
        
        if not supported:
            supported_fmt = ', '.join(omni_constants.IMAGE_LOAD_SUPPORTED_TYPES)
            msg = f'Unsupported image format, the current supported format are: {supported_fmt}.'

            return images_pb2.GeneralImageResponse(ret=1, msg=msg)

        all_images = omni_utils.load_json_data(self.img_record_file)

        msg = f'Loading: {request.name}, this might take a while, please check image status with "images" command.'
        update = False

        local_images = all_images['local']
        if request.name in local_images.keys():
            LOG.debug(f"Image: {request.name} already existed, replace it with: {request.path} ...")
            msg = f'Replacing: {request.name}, with new image file: {request.path}, this might take a while, please check image status with "images" command.'
            update = True

        @omni_utils.asyncwrapper
        def do_load(images, name, path, fmt, update):
            self.backend.load_and_transform(images, name, path, fmt, update)
        
        do_load(all_images, request.name, request.path, fmt, update)

        return images_pb2.GeneralImageResponse(ret=0, msg=msg)

    def delete_image(self, request, context):
        LOG.debug(f"Get request to delete image: {request.name}  ...")
        images = omni_utils.load_json_data(self.img_record_file)
        ret = self.backend.delete_image(images, request.name)
        if ret == 0:
            msg = f'Image: {request.name} has been successfully deleted.'
        elif ret == 1:
            msg = f'Image: {request.name} does not exist, please check again.'

        return images_pb2.GeneralImageResponse(ret=1, msg=msg)
