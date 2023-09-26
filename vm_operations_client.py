# vm_operations_client.py

import grpc
import vm_operations_pb2
import vm_operations_pb2_grpc

def create_vm(grpc_client, vm_name, vnuma_enabled, vm_gen, instance_path, root_disk_path, flavor_name, cpucores_num, ram_capacity, disk_capacity):
    # 创建虚拟机
    request = vm_operations_pb2.CreateVmRequest(
        vm_name=vm_name,
        vnuma_enabled=vnuma_enabled,
        vm_gen=vm_gen,
        instance_path=instance_path,
        root_disk_path=root_disk_path,
        flavor=vm_operations_pb2.Flavor(
            flavor_name=flavor_name,
            cpucores_num=cpucores_num,
            ram_capacity=ram_capacity,
            disk_capacity=disk_capacity
        )
    )
    response = grpc_client.CreateVm(request)
    print(f"Create VM Response: {response.message}")

def start_vm(grpc_client, vm_name):
    # 启动虚拟机
    request = vm_operations_pb2.StartVmRequest(vm_name=vm_name)
    response = grpc_client.StartVm(request)
    print(f"Start VM Response: {response.message}")

def stop_vm(grpc_client, vm_name):
    # 停止虚拟机
    request = vm_operations_pb2.StopVmRequest(vm_name=vm_name)
    response = grpc_client.StopVm(request)
    print(f"Stop VM Response: {response.message}")

def attach_disk(grpc_client, vm_name, disk_path, drive_type):
    # 挂载磁盘
    request = vm_operations_pb2.AttachDiskRequest(
        vm_name=vm_name,
        disk_path=disk_path,
        drive_type=drive_type
    )
    response = grpc_client.AttachDisk(request)
    print(f"Attach Disk Response: {response.message}")

def detach_disk(grpc_client, vm_name, disk_path):
    # 卸载磁盘
    request = vm_operations_pb2.DetachDiskRequest(
        vm_name=vm_name,
        disk_path=disk_path
    )
    response = grpc_client.DetachDisk(request)
    print(f"Detach Disk Response: {response.message}")

def create_flavor(grpc_client, flavor_name, cpucores_num, ram_capacity, disk_capacity):
    # 创建虚拟机规格
    request = vm_operations_pb2.CreateFlavorRequest(
        flavor_name=flavor_name,
        cpucores_num=cpucores_num,
        ram_capacity=ram_capacity,
        disk_capacity=disk_capacity
    )
    response = grpc_client.CreateFlavor(request)
    print(f"Create Flavor Response: {response.message}")

def delete_flavor(grpc_client, flavor_id):
    # 删除虚拟机规格
    request = vm_operations_pb2.DeleteFlavorRequest(flavor_id=flavor_id)
    response = grpc_client.DeleteFlavor(request)
    print(f"Delete Flavor Response: {response.message}")

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        grpc_client = vm_operations_pb2_grpc.VmOperationsServiceStub(channel)
        # 解析命令行参数并调用相应的 gRPC 方法

if __name__ == '__main__':
    main()