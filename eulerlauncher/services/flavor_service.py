import logging
import os

from eulerlauncher.backends import flavor_handler
from eulerlauncher.grpcs.eulerlauncher_grpc import flavors_pb2, flavors_pb2_grpc

LOG = logging.getLogger(__name__)


class FlavorService(flavors_pb2_grpc.FlavorGrpcServiceServicer):
    '''
    The Flavor GRPC Handler
    '''

    def __init__(self, arch, host_os, conf, svc_base_dir) -> None:
        self.CONF = conf
        self.svc_base_dir = svc_base_dir
        self.work_dir = self.CONF.conf.get('default', 'work_dir')
        self.flavor_dir = os.path.join(self.work_dir, 'flavor')
        self.flavor_record_file = os.path.join(self.flavor_dir, 'flavors.json')
        self.backend = flavor_handler.FlavorHandler(
                self.CONF, self.work_dir, self.flavor_dir, self.flavor_record_file,
                LOG, self.svc_base_dir)
    
    def list_flavors(self, request, context):
        LOG.debug(f"Get request to list all flavors ...")
        pass

    def create_flavor(self, request, context):
        LOG.debug(f"Get request to create flavor ...")
        pass

    def delete_flavor(self, request, context):
        LOG.debug(f"Get request to delete a flavor ...")
        pass