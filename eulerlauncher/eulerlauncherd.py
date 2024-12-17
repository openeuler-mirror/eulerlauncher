import argparse
import grpc
import logging
import os
import PIL.Image
import platform
import pystray
import requests
import signal
import sys
import time
import configparser
from concurrent import futures


from eulerlauncher.grpcs.eulerlauncher_grpc import images_pb2, images_pb2_grpc
from eulerlauncher.grpcs.eulerlauncher_grpc import instances_pb2, instances_pb2_grpc
from eulerlauncher.services import image_service, instance_service
from eulerlauncher.utils import exceptions
from eulerlauncher.utils import constants
from eulerlauncher.utils import utils


IMG_URL = 'https://gitee.com/openeuler/eulerlauncher/raw/master/etc/supported_images.json'

# Avoid create zombie children in MacOS and Linux
host_os_raw = platform.uname().system
if host_os_raw != 'Windows':
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

parser = argparse.ArgumentParser()
parser.add_argument('conf_file', help='Configuration file for the application', type=str)

def init_log(CONF):
    log_dir = CONF.get('default', 'log_dir')
    debug = CONF.get('default', 'debug')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, 'eulerlauncher.log')
    
    if debug == 'True':
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        filename=log_file, level=log_level, filemode='a+')


def init_workdir(arch, CONF, LOG):
    work_dir = CONF.get('default', 'work_dir')
    image_dir = os.path.join(work_dir, 'images')
    instance_dir = os.path.join(work_dir, 'instances')
    instance_record_file = os.path.join(instance_dir, 'instances.json')
    image_record_file = os.path.join(image_dir, 'images.json')

    LOG.debug('Initializing EulerLauncherd ...')
    LOG.debug('Checking for work directory ...')
    if not os.path.exists(work_dir):
        LOG.debug('Create %s as working directory ...' % work_dir)
        os.makedirs(work_dir)

    LOG.debug('Checking for instance directory ...')
    if not os.path.exists(instance_dir):
        LOG.debug('Create %s as instance directory ...' % instance_dir)
        os.makedirs(instance_dir)
    LOG.debug('Checking for instance database ...')
    if not os.path.exists(instance_record_file):
        LOG.debug('Create %s as instance database ...' % instance_record_file)
        instances = {
        }
        utils.save_json_data(instance_record_file, instances)

    LOG.debug('Checking for image directory ...')
    if not os.path.exists(image_dir):
        LOG.debug('Create %s as image directory ...' % image_dir)
        os.makedirs(image_dir)
    LOG.debug('Checking for image database ...')
    if not os.path.exists(image_record_file):
        LOG.debug('Create %s as image database ...' % image_record_file)
        remote_image_resp = requests.get(IMG_URL, verify=False)
        remote_images = remote_image_resp.json()[arch]
        image_record = {
            'remote': {},
            'local': {}
        }
        for name, path in remote_images.items():
            image_record['remote'][name] = {
                'name': name,
                'path': path,
                'location': constants.IMAGE_LOCATION_REMOTE,
                'status': constants.IMAGE_STATUS_DOWLOADABLE
            }
        utils.save_json_data(image_record_file, image_record)

def serve(host_arch, host_os, CONF, LOG):
    '''
    Run the EulerLauncherd service
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    images_pb2_grpc.add_ImageGrpcServiceServicer_to_server(image_service.ImageService(host_arch, host_os, CONF, LOG), server)
    instances_pb2_grpc.add_InstanceGrpcServiceServicer_to_server(instance_service.InstanceService(host_arch, host_os, CONF, LOG), server)
    server.add_insecure_port('localhost:50052')
    server.start()
    LOG.debug('EulerLauncherd service started ...')

    if host_os == 'Win':
        return server
    else:
        def term_handler(signum, frame):
            pid = os.getpid()
            os.killpg(os.getpgid(pid), signal.SIGKILL)

        # Avoid create orphan children in MacOS and Linux
        signal.signal(signal.SIGTERM, term_handler)
    
        while True:
            time.sleep(1)

def init_launcherd(conf_file):
    CONF = configparser.ConfigParser()
    if not os.path.exists(conf_file):
        raise exceptions.NoSuchFile(file=conf_file)
    CONF.read(conf_file)

    init_log(CONF)
    LOG = logging.getLogger(__name__)

    host_arch_raw = platform.uname().machine
    host_os_raw = platform.uname().system

    host_arch = constants.ARCH_MAP[host_arch_raw]
    host_os = constants.OS_MAP[host_os_raw]

    init_workdir(host_arch, CONF, LOG)

    return serve(host_arch, host_os, CONF, LOG)


if __name__ == '__main__':
    host_os_raw = platform.uname().system
    if host_os_raw != 'Windows':
        args = parser.parse_args()
        conf_file = args.conf_file
    else:
        conf_file = os.path.join(os.getcwd(), 'etc', 'eulerlauncher.conf')

    if host_os_raw != 'Windows':
        init_launcherd(conf_file)
    else:
        try:
            logo = PIL.Image.open(os.path.join(os.getcwd(), 'etc', 'favicon.png'))

            def on_clicked(icon, item):
                icon.stop()
    
            icon = pystray.Icon('EulerLauncher', logo, menu=pystray.Menu(
                pystray.MenuItem('Exit EulerLauncher', on_clicked)
            ))

        except Exception as e:
            print('Error: ' + str(e))
            sys.exit(0)
        
        server = init_launcherd(conf_file)

        icon.run()
        server.stop(None)
        sys.exit(0)
            
