# vm_operations_service.py

import grpc
from concurrent import futures
import vm_operations_pb2
import vm_operations_pb2_grpc

# 导入你的后端代码中的相关类和方法
from backends import VMOps, Flavor

class VmOperationsService(vm_operations_pb2_grpc.VmOperationsServiceServicer):
    def __init__(self):
        # 初始化后端代码的对象
        self.vm_ops = VMOps()

    def CreateVm(self, request, context):
        # 调用后端代码中的创建虚拟机方法
        # 这里需要根据请求中的参数构造适当的参数
        vm_name = request.vm_name
        vnuma_enabled = request.vnuma_enabled
        vm_gen = request.vm_gen
        instance_path = request.instance_path
        root_disk_path = request.root_disk_path
        flavor_data = request.flavor
        flavor = Flavor(flavor_data.flavor_name, flavor_data.cpucores_num, flavor_data.ram_capacity, flavor_data.disk_capacity)
        response_message = self.vm_ops.build_and_run_vm(vm_name, uuid, image_name, vnuma_enabled, vm_gen, instance_path, root_disk_path, flavor)
        return vm_operations_pb2.VmResponse(message=response_message)

    def StartVm(self, request, context):
        # 实现启动虚拟机方法
        vm_name = request.vm_name
        response_message = self.vm_ops.start_vm(vm_name)  # 调用后端代码中的启动虚拟机方法
        return vm_operations_pb2.VmResponse(message=response_message)

    def StopVm(self, request, context):
        # 实现停止虚拟机方法
        vm_name = request.vm_name
        response_message = self.vm_ops.stop_vm(vm_name)  # 调用后端代码中的停止虚拟机方法
        return vm_operations_pb2.VmResponse(message=response_message)

    def AttachDisk(self, request, context):
        # 实现挂载磁盘方法
        vm_name = request.vm_name
        disk_path = request.disk_path
        drive_type = request.drive_type
        response_message = self.vm_ops.attach_disk(vm_name, disk_path, drive_type)  # 调用后端代码中的挂载磁盘方法
        return vm_operations_pb2.VmResponse(message=response_message)

    def DetachDisk(self, request, context):
        # 实现卸载磁盘方法
        vm_name = request.vm_name
        disk_path = request.disk_path
        response_message = self.vm_ops.detach_disk(vm_name, disk_path)  # 调用后端代码中的卸载磁盘方法
        return vm_operations_pb2.VmResponse(message=response_message)

    def CreateFlavor(self, request, context):
        # 实现创建虚拟机规格方法
        flavor_name = request.flavor_name
        cpucores_num = request.cpucores_num
        ram_capacity = request.ram_capacity
        disk_capacity = request.disk_capacity
        response_message = self.vm_ops.create_flavor(flavor_name, cpucores_num, ram_capacity, disk_capacity)
        # 调用后端代码中的创建虚拟机规格方法
        return vm_operations_pb2.VmResponse(message=response_message)

    def DeleteFlavor(self, request, context):
        # 实现删除虚拟机规格方法
        flavor_id = request.flavor_id
        response_message = self.vm_ops.delete_flavor(flavor_id)  # 调用后端代码中的删除虚拟机规格方法
        return vm_operations_pb2.VmResponse(message=response_message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vm_operations_pb2_grpc.add_VmOperationsServiceServicer_to_server(VmOperationsService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()