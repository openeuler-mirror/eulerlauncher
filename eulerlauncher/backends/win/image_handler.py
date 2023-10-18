import copy
import lzma
import wget
import os
import shutil
import ssl

from eulerlauncher.backends.win import powershell
from eulerlauncher.utils import constants
from eulerlauncher.utils import utils as omni_utils
from eulerlauncher.utils import objs


ssl._create_default_https_context = ssl._create_unverified_context


class WinImageHandler(object):
    
    def __init__(self, conf, work_dir, image_dir, image_record_file, logger) -> None:
        self.conf = conf
        self.work_dir = work_dir
        self.image_dir = image_dir
        self.image_record_file = image_record_file
        self.LOG = logger
        self.pattern = conf.conf.get('default', 'pattern')

    def download_and_transform(self, images, img_to_download):

        # Download the image
        img_name = wget.filename_from_url(images['remote'][img_to_download]['path'])
        img_dict = copy.deepcopy(images['remote'][img_to_download])
        downloaded_bytes = 0

        def progress_bar(current, total, width):
            nonlocal downloaded_bytes
            if current == 0 or current - downloaded_bytes > 1024*1024 or current == total:
                progress_percent = int((current / total) * 100)
                downloaded_bytes = current
                with open(os.path.join(self.image_dir, 'download_progress_bar_' + img_to_download), 'w') as progress_file:
                    progress_file.write(f"{current/1024/1024: .2f}/{total/1024/1024: .2f}MB ({progress_percent}%)")

        if not os.path.exists(os.path.join(self.image_dir, img_name)):
            self.LOG.debug(f'Downloading image: {img_to_download} from remote repo ...')
            img_dict['location'] = constants.IMAGE_LOCATION_LOCAL
            img_dict['status'] = constants.IMAGE_STATUS_DOWNLOADING
            images['local'][img_to_download] = img_dict
            omni_utils.save_json_data(self.image_record_file, images)
            wget.download(url=images['remote'][img_to_download]['path'], out=os.path.join(self.image_dir, img_name), bar=progress_bar)
            self.LOG.debug(f'Image: {img_to_download} succesfully downloaded from remote repo ...')
    
        # Decompress the image
        self.LOG.debug(f'Decompressing image file: {img_name} ...')
        qcow2_name = img_to_download + '.qcow2'
        with open(os.path.join(self.image_dir, img_name), 'rb') as pr, open(os.path.join(self.image_dir, qcow2_name), 'wb') as pw:
            data = pr.read()
            data_dec = lzma.decompress(data)
            pw.write(data_dec)

        image_name = ""
        if self.pattern == "hyper-v":
            # Convert the img to vhdx
            vhdx_name = img_to_download + '.vhdx'
            image_name = vhdx_name
            self.LOG.debug(f'Converting image file: {img_name} to {vhdx_name} ...')
            with powershell.PowerShell('GBK') as ps:
                cmd = 'qemu-img convert -O vhdx {0} {1}'
                outs, errs = ps.run(cmd.format(os.path.join(self.image_dir, qcow2_name), os.path.join(self.image_dir, vhdx_name)))

            self.LOG.debug(f'Cleanup temp files ...')
            os.remove(os.path.join(self.image_dir, qcow2_name))
            if os.path.exists(os.path.join(self.image_dir, "download_progress_bar_" + img_to_download)):
                os.remove(os.path.join(self.image_dir, "download_progress_bar_" + img_to_download))
        elif self.pattern == 'qemu':
            image_name = qcow2_name

        # Record local image
        img_dict['status'] = constants.IMAGE_STATUS_READY
        img_dict['path'] = os.path.join(self.image_dir, image_name)
        images['local'][img_to_download] = img_dict
        omni_utils.save_json_data(self.image_record_file, images)
        self.LOG.debug(f'Image: {img_to_download} is ready ...')

    def download_progress_bar(self, img_name):
        progress_bar = ""
        progress_bar_path = os.path.join(self.image_dir, 'download_progress_bar_' + img_name)
        if os.path.exists(progress_bar_path):
            with open(progress_bar_path, "r") as progress_bar_file:
                progress_bar = progress_bar_file.read()
        if progress_bar != "":
            return constants.IMAGE_STATUS_DOWNLOADING + ": " + progress_bar
        else:
            return constants.IMAGE_STATUS_DOWNLOADING

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

        if fmt not in constants.IMAGE_LOAD_SUPPORTED_TYPES_COMPRESSED:
            img_name = f'{img_to_load}.{fmt}'
            shutil.copyfile(path, os.path.join(self.image_dir, img_name))
        else:
            # Decompress the image
            self.LOG.debug(f'Decompressing image file: {path} ...')
            fmt = fmt.split('.')[0]
            img_name = f'{img_to_load}.{fmt}'
            with open(path, 'rb') as pr, open(os.path.join(self.image_dir, img_name), 'wb') as pw:
                data = pr.read()
                data_dec = lzma.decompress(data)
                pw.write(data_dec)
        qcow2_name = img_name
        image_name = ''
        if self.pattern == 'hyper-v':
            # Convert the qcow2 img to vhdx
            vhdx_name = img_to_load + '.vhdx'
            self.LOG.debug(f'Converting image file: {qcow2_name} to {vhdx_name} ...')
            load_progress_bar_path = os.path.join(self.image_dir, "load_progress_bar_" + img_to_load)
            with powershell.PowerShell('GBK') as ps:
                cmd = 'qemu-img convert -p -O vhdx {0} {1} | Out-File -FilePath {2}'
                outs, errs = ps.run(cmd.format(os.path.join(self.image_dir, img_name), os.path.join(self.image_dir, vhdx_name), load_progress_bar_path))
            self.LOG.debug(f'Cleanup temp files ...')
            os.remove(os.path.join(self.image_dir, qcow2_name))
            os.remove(load_progress_bar_path)
            image_name = vhdx_name
        elif self.pattern == 'qemu':
            image_name = qcow2_name

        # Record local image
        image.path = os.path.join(self.image_dir, image_name)
        image.status = constants.IMAGE_STATUS_READY
        images['local'][image.name] = image.to_dict()
        omni_utils.save_json_data(self.image_record_file, images)
        self.LOG.debug(f'Image: {vhdx_name} is ready ...')

    def load_progress_bar(self, img_name):
        progress_bar_lines = []
        progress_bar_path = os.path.join(self.image_dir, "load_progress_bar_" + img_name)
        if os.path.exists(progress_bar_path):
            with open(progress_bar_path, 'r', encoding=omni_utils.detect_encoding(progress_bar_path), errors='ignore') as progress_bar_file:
                progress_bar_lines = progress_bar_file.readlines()
        if len(progress_bar_lines) > 1 and progress_bar_lines[-2].strip() != "":
            return constants.IMAGE_STATUS_LOADING + ": " + progress_bar_lines[-2].strip()
        else:
            return constants.IMAGE_STATUS_LOADING
        self.LOG.debug(f'Image: {image_name} is ready ...')