from eulerlauncher.grpcs.eulerlauncher_grpc import instances_pb2

class Instance(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        """Get list of instance"""
        request = instances_pb2.ListInstancesRequest()
        response = self.client.list_instances(request)
        return response

    def create(self, name, image, arch):
        """Create instance"""
        request = instances_pb2.CreateInstanceRequest(name=name, image=image, arch=arch)
        response = self.client.create_instance(request)
        return response
    
    def delete(self, name):
        """Delete instance"""
        request = instances_pb2.DeleteInstanceRequest(name=name)
        response = self.client.delete_instance(request)
        return response
