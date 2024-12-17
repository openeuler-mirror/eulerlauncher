import os

from eulerlauncher.grpcs.eulerlauncher_grpc import images_pb2, images_pb2_grpc
from eulerlauncher.utils import constants


class ImageService(images_pb2_grpc.ImageGrpcServiceServicer):
    '''
    The Image GRPC Handler
    '''

    def __init__(self, arch, host_os, CONF, LOG) -> None:
        self.CONF = CONF
        self.LOG = LOG
        self.work_dir = self.CONF.get('default', 'work_dir')
        self.image_dir = os.path.join(self.work_dir, 'images')
        self.image_record_file = os.path.join(self.image_dir, 'images.json')
        if host_os == 'Win':
            pass
            # from eulerlauncher.backends.win import image_handler as win_image_handler
            # self.backend = win_image_handler.WinImageHandler(
            #     self.CONF, self.work_dir, self.image_dir, self.LOG)
        elif host_os == 'MacOS':
            from eulerlauncher.backends import image_handler as mac_image_handler
            self.backend = mac_image_handler.MacImageHandler(
                self.CONF, self.work_dir, self.image_dir, self.LOG)


    def list_images(self, request, context):
        self.LOG.debug(f"Get request to list images ...")
        all_images = self.backend.list_images()
        ret = []
        for image in all_images:
            ret.append({
                'name': image['name'],
                'location': image['location'],
                'status': image['status']
            })
        return images_pb2.ListImageResponse(images=ret)
    

    def download_image(self, request, context):
        self.LOG.debug(f"Get request to download image: {request.name} ...")
        ret = self.backend.download_image(request.name)
        msg = ''
        if ret == 0:
            msg = f'Downloading: {request.name}, this might take a while, please check image status with "images" command.'
        elif ret == 1:
            msg = f'Image: {request.name} is valid for download, please check image name from REMOTE IMAGE LIST using "images" command ...'
        return images_pb2.GeneralImageResponse(ret=ret, msg=msg)


    def delete_image(self, request, context):
        self.LOG.debug(f"Get request to delete image: {request.name}  ...")
        ret = self.backend.delete_image(request.name)
        msg = ''
        if ret == 0:
            msg = f'Image: {request.name} has been successfully deleted.'
        elif ret == 1:
            msg = f'Image: {request.name} does not exist, please check again.'
        return images_pb2.GeneralImageResponse(ret=ret, msg=msg)


    def load_image(self, request, context):
        self.LOG.debug(f"Get request to load image: {request.name} from path: {request.path} ...")
        ret = self.backend.load_image(request.name, request.path)
        msg = ''
        if ret == 0:
            msg = f'Loading: {request.name}, this might take a while, please check image status with "images" command.'
        elif ret == 1:
            msg = f'Image: {request.path} does not exist, please check again.'
        elif ret == 2:
            supported_fmt = ', '.join(constants.IMAGE_LOAD_SUPPORTED_TYPES)
            msg = f'Unsupported image format, the current supported format are: {supported_fmt}.'
        return images_pb2.GeneralImageResponse(ret=ret, msg=msg)
