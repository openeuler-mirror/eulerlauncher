import lzma
import wget
import os
import subprocess
import shutil
import ssl

from eulerlauncher.utils import constants
from eulerlauncher.utils import utils


ssl._create_default_https_context = ssl._create_unverified_context


class MacImageHandler(object):

    def __init__(self, CONF, work_dir, image_dir, LOG) -> None:
        self.CONF = CONF
        self.work_dir = work_dir
        self.image_dir = image_dir
        self.image_record_path = os.path.join(image_dir, 'images.json')
        self.LOG = LOG


    def list_images(self):
        image_record = utils.load_json_data(self.image_record_path)
        all_images = list(image_record["remote"].values()) + list(image_record["local"].values())
        return all_images
    

    def download_image(self, name):
        image_record = utils.load_json_data(self.image_record_path)
        if name not in image_record['remote'].keys():
            self.LOG.debug(f'Image: {name} not valid for download')
            return 1
        
        @utils.asyncwrapper
        def download_and_transform(name):
            image_record = utils.load_json_data(self.image_record_path)
            image_url = image_record['remote'][name]['path']
            image_file = wget.filename_from_url(image_url)
            image_path = os.path.join(self.image_dir, image_file)

            # Download the image
            self.LOG.debug(f'Downloading image: {name} from remote repo ...')
            image_record['local'][name] = {
                'name': name,
                'location': constants.IMAGE_LOCATION_LOCAL,
                'status': constants.IMAGE_STATE_MAP[2],
                'path': image_url
            }
            utils.save_json_data(self.image_record_path, image_record)
            wget_bin = shutil.which('wget_bin')
            download_cmd = [wget_bin, image_url,
                            '-O', image_path, 
                            '--no-check-certificate',
                            '--user-agent', 'Mozilla']
            self.LOG.debug(' '.join(download_cmd))
            subprocess.call(' '.join(download_cmd), shell=True)
            self.LOG.debug(f'Image: {name} succesfully downloaded from remote repo ...')

            # Decompress the image
            self.LOG.debug(f'Decompressing image: {image_file} ...')
            with open(image_path, 'rb') as pr, open(os.path.join(self.image_dir, name), 'wb') as pw:
                data = pr.read()
                data_dec = lzma.decompress(data)
                pw.write(data_dec)
            
            self.LOG.debug(f'Cleanup temp files ...')
            os.remove(image_path)

            # Record local image
            image_record = utils.load_json_data(self.image_record_path)
            image_record['local'][name]['status'] = constants.IMAGE_STATE_MAP[4]
            image_record['local'][name]['path'] = os.path.join(self.image_dir, name)
            utils.save_json_data(self.image_record_path, image_record)
            self.LOG.debug(f'Image: {name} is ready ...')     
        
        download_and_transform(name)
        return 0


    def delete_image(self, name):
        image_record = utils.load_json_data(self.image_record_path)
        if name not in image_record['local'].keys():
            self.LOG.debug(f'Image: {name} not valid for delete')
            return 1

        image_path = image_record['local'][name]['path']
        self.LOG.debug(f'Deleting: {name} from image database ...')
        os.remove(image_path)
        del image_record['local'][name]
        utils.save_json_data(self.image_record_path, image_record)
        self.LOG.debug(f'Image: {name} succesfully deleted ...')
        return 0

    
    def load_image(self, name, path):
        if not os.path.exists(path):
            self.LOG.debug(f'Image: {path} does not exist')
            return 1

        supported, fmt = utils.check_format(path, constants.IMAGE_LOAD_SUPPORTED_TYPES)
        if not supported:
            self.LOG.debug(f'Image: {name} not valid for load')
            return 2
        
        @utils.asyncwrapper
        def load_and_transform(name, path):
            image_record = utils.load_json_data(self.image_record_path)
            image_path = os.path.join(self.image_dir, name)
            supported, fmt = utils.check_format(path, constants.IMAGE_LOAD_SUPPORTED_TYPES)
            self.LOG.debug(f'Loading image: {name} from image file: {path} ...')
            image_record['local'][name] = {
                'name': name,
                'location': constants.IMAGE_LOCATION_LOCAL,
                'status': constants.IMAGE_STATE_MAP[3],
                'path': ''
            }
            utils.save_json_data(self.image_record_path, image_record)

            if fmt == 'qcow2':
                shutil.copyfile(path, image_path)
            else:
                # Decompress the image
                self.LOG.debug(f'Decompressing image file: {path} ...')
                with open(path, 'rb') as pr, open(image_path, 'wb') as pw:
                    data = pr.read()
                    data_dec = lzma.decompress(data)
                    pw.write(data_dec)

            # Record local image
            image_record = utils.load_json_data(self.image_record_path)
            image_record['local'][name]['status'] = constants.IMAGE_STATE_MAP[4]
            image_record['local'][name]['path'] = image_path
            utils.save_json_data(self.image_record_path, image_record)
            self.LOG.debug(f'Image: {name} is ready ...')

        load_and_transform(name, path)
        return 0