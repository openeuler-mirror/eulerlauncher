import copy
import lzma
import wget
import os
import shutil
import ssl

from omnivirt.backends.win import powershell
from omnivirt.utils import constants
from omnivirt.utils import utils as omni_utils
from omnivirt.utils import objs


ssl._create_default_https_context = ssl._create_unverified_context


class WinImageHandler(object):
    
    def __init__(self, conf, work_dir, image_dir, image_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger

    def download_and_transform(self, images, img_to_download):

        # Download the image
        img_name = wget.filename_from_url(images['remote'][img_to_download]['path'])
        img_dict = copy.deepcopy(images['remote'][img_to_download])

        if not os.path.exists(os.path.join(self.image_dir, img_name)):
            self.LOG.debug(f'Downloading image: {img_to_download} from remote repo ...')
            img_dict['location'] = constants.IMAGE_LOCATION_LOCAL
            img_dict['status'] = constants.IMAGE_STATUS_DOWNLOADING
            images['local'][img_to_download] = img_dict
            omni_utils.save_json_data(self.image_record_file, images)
            wget.download(url=images['remote'][img_to_download]['path'], out=os.path.join(self.image_dir, img_name), bar=None)
            self.LOG.debug(f'Image: {img_to_download} succesfully downloaded from remote repo ...')
    
        # Decompress the image
        self.LOG.debug(f'Decompressing image file: {img_name} ...')
        qcow2_name = img_name[:-3]
        with open(os.path.join(self.image_dir, img_name), 'rb') as pr, open(os.path.join(self.image_dir, qcow2_name), 'wb') as pw:
            data = pr.read()
            data_dec = lzma.decompress(data)
            pw.write(data_dec)
    
        # Convert the qcow2 img to vhdx
        vhdx_name = img_to_download + '.vhdx'
        self.LOG.debug(f'Converting image file: {img_name} to {vhdx_name} ...')
        with powershell.PowerShell('GBK') as ps:
            cmd = 'qemu-img convert -O vhdx {0} {1}'
            outs, errs = ps.run(cmd.format(os.path.join(self.image_dir, qcow2_name), os.path.join(self.image_dir, vhdx_name)))

        self.LOG.debug(f'Cleanup temp files ...')
        os.remove(os.path.join(self.image_dir, qcow2_name))

        # Record local image
        img_dict['status'] = constants.IMAGE_STATUS_READY
        img_dict['path'] = os.path.join(self.image_dir, vhdx_name)
        images['local'][img_to_download] = img_dict
        omni_utils.save_json_data(self.image_record_file, images)
        self.LOG.debug(f'Image: {img_to_download} is ready ...')

    def delete_image(self, images, img_to_delete):
        if img_to_delete not in images['local'].keys():
            return 1
        else:
            return self._delete_image(images, img_to_delete)

    def _delete_image(self, images, img_to_delete):
        img_path = images['local'][img_to_delete]['path']
        if os.path.exists(img_path):
            self.LOG.debug(f'Deleting: {img_path} ...')
            os.remove(img_path)
        
        self.LOG.debug(f'Deleting: {img_to_delete} from image database ...')
        del images['local'][img_to_delete]
        omni_utils.save_json_data(self.image_record_file, images)

        return 0

    def load_and_transform(self, images, img_to_load, path, fmt, update=False):

        if update:
            self._delete_image(images, img_to_load)
        
        image = objs.Image()
        image.name = img_to_load
        image.path = ''
        image.location = constants.IMAGE_LOCATION_LOCAL
        image.status = constants.IMAGE_STATUS_LOADING
        images['local'][image.name] = image.to_dict()
        omni_utils.save_json_data(self.image_record_file, images)

        if fmt == 'qcow2':
            qcow2_name = f'{img_to_load}.qcow2'
            shutil.copyfile(path, os.path.join(self.image_dir, qcow2_name))
        else:
            # Decompress the image
            self.LOG.debug(f'Decompressing image file: {path} ...')
            qcow2_name = f'{img_to_load}.qcow2'
            with open(path, 'rb') as pr, open(os.path.join(self.image_dir, qcow2_name), 'wb') as pw:
                data = pr.read()
                data_dec = lzma.decompress(data)
                pw.write(data_dec)
        
        # Convert the qcow2 img to vhdx
        vhdx_name = img_to_load + '.vhdx'
        self.LOG.debug(f'Converting image file: {qcow2_name} to {vhdx_name} ...')
        with powershell.PowerShell('GBK') as ps:
            cmd = 'qemu-img convert -O vhdx {0} {1}'
            outs, errs = ps.run(cmd.format(os.path.join(self.image_dir, qcow2_name), os.path.join(self.image_dir, vhdx_name)))
        self.LOG.debug(f'Cleanup temp files ...')
        os.remove(os.path.join(self.image_dir, qcow2_name))

        # Record local image
        image.path = os.path.join(self.image_dir, vhdx_name)
        image.status = constants.IMAGE_STATUS_READY
        images['local'][image.name] = image.to_dict()
        omni_utils.save_json_data(self.image_record_file, images)
        self.LOG.debug(f'Image: {vhdx_name} is ready ...')
