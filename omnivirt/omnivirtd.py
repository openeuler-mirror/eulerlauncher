import argparse
from concurrent import futures
import grpc
import logging
import os
import PIL.Image
import platform
import pystray
import requests
import signal
import subprocess
import sys
import time

from omnivirt.grpcs.omnivirt_grpc import images_pb2, images_pb2_grpc
from omnivirt.grpcs.omnivirt_grpc import instances_pb2, instances_pb2_grpc
from omnivirt.services import imager_service, instance_service
from omnivirt.utils import constants
from omnivirt.utils import objs
from omnivirt.utils import utils


IMG_URL = 'https://gitee.com/openeuler/omnivirt/raw/master/etc/supported_images.json'

# Avoid create zombie children in MacOS and Linux
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

parser = argparse.ArgumentParser()
parser.add_argument('conf_file', help='Configuration file for the application', type=str)
parser.add_argument('base_dir', help='The base work directory of the daemon')


def config_logging(config):
    log_dir = config.conf.get('default', 'log_dir')
    debug = config.conf.get('default', 'debug')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, 'omnivirt.log')
    
    if debug == 'True':
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        filename=log_file, level=log_level, filemode='a+')


def init(arch, config, LOG):
    work_dir = config.conf.get('default', 'work_dir')
    image_dir = os.path.join(work_dir, 'images')
    instance_dir = os.path.join(work_dir, 'instances')
    instance_record_file = os.path.join(instance_dir, 'instances.json')
    img_record_file = os.path.join(image_dir, 'images.json')

    LOG.debug('Initializing OmniVirtd ...')
    LOG.debug('Checking for work directory ...')
    if not os.path.exists(work_dir):
        LOG.debug('Create %s as working directory ...' % work_dir)
        os.makedirs(work_dir)
    LOG.debug('Checking for instances directory ...')
    if not os.path.exists(instance_dir):
        LOG.debug('Create %s as working directory ...' % work_dir)
        os.makedirs(instance_dir)
    LOG.debug('Checking for instance database ...')
    if not os.path.exists(instance_record_file):
        instances = {
            'instances': {}
        }
        utils.save_json_data(instance_record_file, instances)

    LOG.debug('Checking for image directory ...')
    if not os.path.exists(image_dir):
        LOG.debug('Create %s as image directory ...' % image_dir)
        os.makedirs(image_dir)

    LOG.debug('Checking for image database ...')
    remote_img_resp = requests.get(IMG_URL, verify=False)
    remote_imgs = remote_img_resp.json()[arch]
    if not os.path.exists(img_record_file):
        images = {}
        for name, path in remote_imgs.items():
            image = objs.Image()
            image.name = name
            image.path = path
            image.location = constants.IMAGE_LOCATION_REMOTE
            image.status = constants.IMAGE_STATUS_DOWLOADABLE
            images[image.name] = image.to_dict()

        image_body = {
            'remote': images,
            'local': {}
        }
        utils.save_json_data(img_record_file, image_body)

def serve(arch, host_os, CONF, LOG, base_dir):
    '''
    Run the Omnivirtd Service
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    images_pb2_grpc.add_ImageGrpcServiceServicer_to_server(imager_service.ImagerService(arch, host_os, CONF, base_dir), server)
    instances_pb2_grpc.add_InstanceGrpcServiceServicer_to_server(instance_service.InstanceService(arch, host_os, CONF, base_dir), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    LOG.debug('OmniVirtd Service Started ...')

    def term_handler(signum, frame):
        pid = os.getpid()
        os.killpg(os.getpgid(pid), signal.SIGKILL)

    # Avoid create orphan children in MacOS and Linux
    signal.signal(signal.SIGTERM, term_handler)
    
    while True:
            time.sleep(1)

def init_omnivirtd(conf, base_dir):
    CONF = objs.Conf(conf)

    config_logging(CONF)
    LOG = logging.getLogger(__name__)

    host_arch_raw = platform.uname().machine
    host_os_raw = platform.uname().system

    host_arch = constants.ARCH_MAP[host_arch_raw]
    host_os = constants.OS_MAP[host_os_raw]

    try:
        init(host_arch, CONF, LOG)
    except Exception as e:
        LOG.debug('Error: ' + str(e))
        return str(e)
    else:
        serve(host_arch, host_os, CONF, LOG, base_dir)


if __name__ == '__main__':
    args = parser.parse_args()
    conf_file = args.conf_file
    try:
        pass
    except Exception as e:
        print('Error: ' + str(e))
    else:
        init_omnivirtd(conf_file, args.base_dir)
