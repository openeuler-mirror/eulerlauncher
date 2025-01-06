import os

from eulerlauncher.grpcs.eulerlauncher_grpc import instances_pb2, instances_pb2_grpc


class InstanceService(instances_pb2_grpc.InstanceGrpcServiceServicer):
    '''
    The Instance GRPC Handler
    '''

    def __init__(self, host_arch, host_os, CONF, LOG) -> None:
        self.CONF = CONF
        self.LOG = LOG
        self.work_dir = self.CONF.get('default', 'work_dir')
        self.instance_dir = os.path.join(self.work_dir, 'instances')
        self.instance_record_path = os.path.join(self.instance_dir, 'instances.json')
        self.image_dir = os.path.join(self.work_dir, 'images')
        self.image_record_path = os.path.join(self.image_dir, 'images.json')
        if host_os == 'Win':
            pass
            # from eulerlauncher.backends.win import instance_handler as win_instance_handler
            # self.backend = win_instance_handler.WinInstanceHandler(
            #     self.CONF, self.work_dir, self.instance_dir, self.image_dir, self.LOG)
        elif host_os == 'MacOS':
            from eulerlauncher.backends import instance_handler as mac_instance_handler
            self.backend = mac_instance_handler.MacInstanceHandler(
                self.CONF, self.work_dir, self.instance_dir, self.image_dir, self.LOG)


    def list_instances(self, request, context):
        self.LOG.debug(f"Get request to list instances ...")
        all_instances = self.backend.list_instances()
        ret = []
        for instance in all_instances:
            ret.append({
                'name': instance['name'],
                'image': instance['image'],
                'vm_state': instance['state'],
                'ip_address': instance['ip_address']
            })
        return instances_pb2.ListInstancesResponse(instances=ret)


    def create_instance(self, request, context):
        self.LOG.debug(f"Get request to create instance: {request.name} with image: {request.image} ...")
        ret = self.backend.create_instance(request.name, request.image)
        msg = ''
        if ret == 0:
            msg = f'Successfully created instance: {request.name} with image: {request.image}.'
        elif ret == 1:
            msg = f'Error: Image "{request.image}" is not available locally, please check again or (down)load it before using ...'
        elif ret == 2:
            msg = f'Error: Instance with name {request.name} already exist, please specify another name.'
        return instances_pb2.CreateInstanceResponse(ret=ret, msg=msg)
    

    def delete_instance(self, request, context):
        self.LOG.debug(f"Get request to delete instance: {request.name} ...")
        ret = self.backend.delete_instance(request.name)
        msg = ''
        if ret == 0:
            msg = f'Successfully deleted instance: {request.name}.'
        elif ret == 1:
            msg = f'Error: Instance with name {request.name} does not exist.'
        return instances_pb2.DeleteInstanceResponse(ret=ret, msg=msg)


    def suspend_instance(self, request, context):
        self.LOG.debug(f"Get request to suspend instance: {request.name} ...")
        ret = self.backend.suspend_instance(request.name)
        msg = ''
        if ret == 0:
            msg = f'Successfully suspended instance: {request.name}.'
        elif ret == 1:
            msg = f'Error: Instance with name {request.name} does not exist.'
        return instances_pb2.SuspendInstanceResponse(ret=ret, msg=msg)


    def resume_instance(self, request, context):
        self.LOG.debug(f"Get request to resume instance: {request.name} ...")
        ret = self.backend.resume_instance(request.name)
        msg = ''
        if ret == 0:
            msg = f'Successfully resumed instance: {request.name}.'
        elif ret == 1:
            msg = f'Error: Instance with name {request.name} does not exist.'
        return instances_pb2.ResumeInstanceResponse(ret=ret, msg=msg)
    

    def console_instance(self, request, context):
        self.LOG.debug(f"Get request to connect instance: {request.name} ...")
        ret = self.backend.console_instance(request.name)
        msg = ''
        if ret == 0:
            msg = f'Successfully connected instance: {request.name}.'
        elif ret == 1:
            msg = f'Error: Instance with name {request.name} does not exist.'
        return instances_pb2.ConsoleInstanceResponse(ret=ret, msg=msg)