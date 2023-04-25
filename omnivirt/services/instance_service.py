import logging
import os

from omnivirt.grpcs.omnivirt_grpc import instances_pb2, instances_pb2_grpc
from omnivirt.utils import utils


LOG = logging.getLogger(__name__)

class InstanceService(instances_pb2_grpc.InstanceGrpcServiceServicer):
    '''
    The Instance GRPC Handler
    '''

    def __init__(self, arch, host_os, conf, svc_base_dir) -> None:
        self.CONF = conf
        self.svc_base_dir = svc_base_dir
        self.work_dir = self.CONF.conf.get('default', 'work_dir')
        self.instance_dir = os.path.join(self.work_dir, 'instances')
        self.instance_record_file = os.path.join(self.instance_dir, 'instances.json')
        self.image_dir = os.path.join(self.work_dir, 'images')
        self.img_record_file = os.path.join(self.image_dir, 'images.json')
        if host_os == 'Win':
            from omnivirt.backends.win import instance_handler as win_instance_handler
            self.backend = win_instance_handler.WinInstanceHandler(
                self.CONF, self.work_dir, self.instance_dir, self.image_dir, self.img_record_file, LOG)
        elif host_os == 'MacOS':
            from omnivirt.backends.mac import instance_handler as mac_instance_handler
            self.backend = mac_instance_handler.MacInstanceHandler(
                self.CONF, self.work_dir, self.instance_dir, self.image_dir,
                self.img_record_file, LOG, self.svc_base_dir)

    def list_instances(self, request, context):
        LOG.debug(f"Get request to list instances ...")
        instances_obj = self.backend.list_instances()

        ret = []
        for vm_obj in instances_obj:
            instance_dict = {
                'name': vm_obj.name,
                'image': vm_obj.image,
                'vm_state': vm_obj.vm_state,
                'ip_address': vm_obj.ip if vm_obj.ip else 'N/A'
            }
            ret.append(instance_dict)
            
        return instances_pb2.ListInstancesResponse(instances=ret)

    def create_instance(self, request, context):
        LOG.debug(f"Get request to create instance: {request.name} with image {request.image} ...")
        
        all_img = utils.load_json_data(self.img_record_file)
        if request.image not in all_img['local'].keys():
            msg = f'Error: Image "{request.image}" is not available locally, please check again or (down)load it before using ...'
            return instances_pb2.CreateInstanceResponse(ret=2, msg=msg)

        all_instances = utils.load_json_data(self.instance_record_file)
        if request.name in all_instances['instances'].keys():
            msg = f'Error: Instance with name {request.name} already exist, please specify another name.'
            return instances_pb2.CreateInstanceResponse(ret=2, msg=msg)
        
        check_result = self.backend.check_names(request.name, all_instances)
        if check_result == 1:
            msg = f'Error: Instance with name {request.name} already exist in exixting Hyper-V or Qemu backend, please specify another name.'
            return instances_pb2.CreateInstanceResponse(ret=2, msg=msg)

        vm = self.backend.create_instance(
            request.name, request.image, self.instance_record_file, all_instances, all_img)
        msg = f'Successfully created {request.name} with image {request.image}'
        return instances_pb2.CreateInstanceResponse(ret=1, msg=msg, instance=vm)
    
    def delete_instance(self, request, context):
        LOG.debug(f"Get request to delete instance: {request.name} ...")
        all_instances = utils.load_json_data(self.instance_record_file)
        if request.name not in all_instances['instances'].keys():
            msg = f'Error: Instance with name {request.name} does not exist.'
            return instances_pb2.DeleteInstanceResponse(ret=2, msg=msg)
        
        self.backend.delete_instance(request.name, self.instance_record_file, all_instances)
        msg = f'Successfully deleted instance: {request.name}.'
        return instances_pb2.DeleteInstanceResponse(ret=1, msg=msg)
