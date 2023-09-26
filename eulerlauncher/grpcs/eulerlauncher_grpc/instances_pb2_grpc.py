# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from eulerlauncher.grpcs.eulerlauncher_grpc import instances_pb2 as instances__pb2


class InstanceGrpcServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.list_instances = channel.unary_unary(
                '/omnivirt.InstanceGrpcService/list_instances',
                request_serializer=instances__pb2.ListInstancesRequest.SerializeToString,
                response_deserializer=instances__pb2.ListInstancesResponse.FromString,
                )
        self.create_instance = channel.unary_unary(
                '/omnivirt.InstanceGrpcService/create_instance',
                request_serializer=instances__pb2.CreateInstanceRequest.SerializeToString,
                response_deserializer=instances__pb2.CreateInstanceResponse.FromString,
                )
        self.delete_instance = channel.unary_unary(
                '/omnivirt.InstanceGrpcService/delete_instance',
                request_serializer=instances__pb2.DeleteInstanceRequest.SerializeToString,
                response_deserializer=instances__pb2.DeleteInstanceResponse.FromString,
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
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'omnivirt.InstanceGrpcService', rpc_method_handlers)
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
        return grpc.experimental.unary_unary(request, target, '/omnivirt.InstanceGrpcService/list_instances',
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
        return grpc.experimental.unary_unary(request, target, '/omnivirt.InstanceGrpcService/create_instance',
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
        return grpc.experimental.unary_unary(request, target, '/omnivirt.InstanceGrpcService/delete_instance',
            instances__pb2.DeleteInstanceRequest.SerializeToString,
            instances__pb2.DeleteInstanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
