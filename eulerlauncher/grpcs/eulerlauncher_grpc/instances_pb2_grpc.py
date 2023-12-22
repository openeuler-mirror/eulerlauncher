# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import instances_pb2 as instances__pb2


class InstanceGrpcServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.list_instances = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/list_instances',
                request_serializer=instances__pb2.ListInstancesRequest.SerializeToString,
                response_deserializer=instances__pb2.ListInstancesResponse.FromString,
                )
        self.create_instance = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/create_instance',
                request_serializer=instances__pb2.CreateInstanceRequest.SerializeToString,
                response_deserializer=instances__pb2.CreateInstanceResponse.FromString,
                )
        self.delete_instance = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/delete_instance',
                request_serializer=instances__pb2.DeleteInstanceRequest.SerializeToString,
                response_deserializer=instances__pb2.DeleteInstanceResponse.FromString,
                )
        self.start_instance = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/start_instance',
                request_serializer=instances__pb2.StartInstanceRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.stop_instsance = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/stop_instsance',
                request_serializer=instances__pb2.StopInstanceRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.AttachDisk = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/AttachDisk',
                request_serializer=instances__pb2.AttachDiskRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.DetachDisk = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/DetachDisk',
                request_serializer=instances__pb2.DetachDiskRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.CreateFlavor = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/CreateFlavor',
                request_serializer=instances__pb2.CreateFlavorRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.DeleteFlavor = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/DeleteFlavor',
                request_serializer=instances__pb2.DeleteFlavorRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.attach_disk = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/attach_disk',
                request_serializer=instances__pb2.AttachDiskRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.dettach_disk = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/dettach_disk',
                request_serializer=instances__pb2.DetachDiskRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.list_flavor = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/list_flavor',
                request_serializer=instances__pb2.ListFlavorsRequest.SerializeToString,
                response_deserializer=instances__pb2.ListFlavorsResponse.FromString,
                )
        self.create_flavor = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/create_flavor',
                request_serializer=instances__pb2.CreateFlavorRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.delete_flavor = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/delete_flavor',
                request_serializer=instances__pb2.CreateFlavorRequest.SerializeToString,
                response_deserializer=instances__pb2.InstanceResponse.FromString,
                )
        self.take_snapshot = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/take_snapshot',
                request_serializer=instances__pb2.TakeSnapshotRequest.SerializeToString,
                response_deserializer=instances__pb2.TakeSnapshotResponse.FromString,
                )
        self.export_development_image = channel.unary_unary(
                '/eulerlauncher.InstanceGrpcService/export_development_image',
                request_serializer=instances__pb2.ExportDevelopmentImageRequest.SerializeToString,
                response_deserializer=instances__pb2.ExportDevelopmentImageResponse.FromString,
                )


class InstanceGrpcServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def list_instances(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create_instance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_instance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def start_instance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stop_instsance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AttachDisk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DetachDisk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateFlavor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFlavor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def attach_disk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def dettach_disk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list_flavor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create_flavor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_flavor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def take_snapshot(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def export_development_image(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InstanceGrpcServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'list_instances': grpc.unary_unary_rpc_method_handler(
                    servicer.list_instances,
                    request_deserializer=instances__pb2.ListInstancesRequest.FromString,
                    response_serializer=instances__pb2.ListInstancesResponse.SerializeToString,
            ),
            'create_instance': grpc.unary_unary_rpc_method_handler(
                    servicer.create_instance,
                    request_deserializer=instances__pb2.CreateInstanceRequest.FromString,
                    response_serializer=instances__pb2.CreateInstanceResponse.SerializeToString,
            ),
            'delete_instance': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_instance,
                    request_deserializer=instances__pb2.DeleteInstanceRequest.FromString,
                    response_serializer=instances__pb2.DeleteInstanceResponse.SerializeToString,
            ),
            'start_instance': grpc.unary_unary_rpc_method_handler(
                    servicer.start_instance,
                    request_deserializer=instances__pb2.StartInstanceRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'stop_instsance': grpc.unary_unary_rpc_method_handler(
                    servicer.stop_instsance,
                    request_deserializer=instances__pb2.StopInstanceRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'AttachDisk': grpc.unary_unary_rpc_method_handler(
                    servicer.AttachDisk,
                    request_deserializer=instances__pb2.AttachDiskRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'DetachDisk': grpc.unary_unary_rpc_method_handler(
                    servicer.DetachDisk,
                    request_deserializer=instances__pb2.DetachDiskRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'CreateFlavor': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFlavor,
                    request_deserializer=instances__pb2.CreateFlavorRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'DeleteFlavor': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteFlavor,
                    request_deserializer=instances__pb2.DeleteFlavorRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'attach_disk': grpc.unary_unary_rpc_method_handler(
                    servicer.attach_disk,
                    request_deserializer=instances__pb2.AttachDiskRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'dettach_disk': grpc.unary_unary_rpc_method_handler(
                    servicer.dettach_disk,
                    request_deserializer=instances__pb2.DetachDiskRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'list_flavor': grpc.unary_unary_rpc_method_handler(
                    servicer.list_flavor,
                    request_deserializer=instances__pb2.ListFlavorsRequest.FromString,
                    response_serializer=instances__pb2.ListFlavorsResponse.SerializeToString,
            ),
            'create_flavor': grpc.unary_unary_rpc_method_handler(
                    servicer.create_flavor,
                    request_deserializer=instances__pb2.CreateFlavorRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'delete_flavor': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_flavor,
                    request_deserializer=instances__pb2.CreateFlavorRequest.FromString,
                    response_serializer=instances__pb2.InstanceResponse.SerializeToString,
            ),
            'take_snapshot': grpc.unary_unary_rpc_method_handler(
                    servicer.take_snapshot,
                    request_deserializer=instances__pb2.TakeSnapshotRequest.FromString,
                    response_serializer=instances__pb2.TakeSnapshotResponse.SerializeToString,
            ),
            'export_development_image': grpc.unary_unary_rpc_method_handler(
                    servicer.export_development_image,
                    request_deserializer=instances__pb2.ExportDevelopmentImageRequest.FromString,
                    response_serializer=instances__pb2.ExportDevelopmentImageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'eulerlauncher.InstanceGrpcService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class InstanceGrpcService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def list_instances(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/list_instances',
            instances__pb2.ListInstancesRequest.SerializeToString,
            instances__pb2.ListInstancesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create_instance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/create_instance',
            instances__pb2.CreateInstanceRequest.SerializeToString,
            instances__pb2.CreateInstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_instance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/delete_instance',
            instances__pb2.DeleteInstanceRequest.SerializeToString,
            instances__pb2.DeleteInstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def start_instance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/start_instance',
            instances__pb2.StartInstanceRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stop_instsance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/stop_instsance',
            instances__pb2.StopInstanceRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AttachDisk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/AttachDisk',
            instances__pb2.AttachDiskRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DetachDisk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/DetachDisk',
            instances__pb2.DetachDiskRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateFlavor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/CreateFlavor',
            instances__pb2.CreateFlavorRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFlavor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/DeleteFlavor',
            instances__pb2.DeleteFlavorRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def attach_disk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/attach_disk',
            instances__pb2.AttachDiskRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def dettach_disk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/dettach_disk',
            instances__pb2.DetachDiskRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list_flavor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/list_flavor',
            instances__pb2.ListFlavorsRequest.SerializeToString,
            instances__pb2.ListFlavorsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create_flavor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/create_flavor',
            instances__pb2.CreateFlavorRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_flavor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/delete_flavor',
            instances__pb2.CreateFlavorRequest.SerializeToString,
            instances__pb2.InstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def take_snapshot(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/take_snapshot',
            instances__pb2.TakeSnapshotRequest.SerializeToString,
            instances__pb2.TakeSnapshotResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def export_development_image(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/eulerlauncher.InstanceGrpcService/export_development_image',
            instances__pb2.ExportDevelopmentImageRequest.SerializeToString,
            instances__pb2.ExportDevelopmentImageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
