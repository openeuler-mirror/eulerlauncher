from eulerlauncher.grpcs.eulerlauncher_grpc import instances_pb2

class Instance(object):
    def __init__(self, client):
        self.client = client


    def list(self):
        """Get list of instance"""
        request = instances_pb2.ListInstancesRequest()
        response = self.client.list_instances(request)
        return response


    def create(self, name, image):
        """Create instance"""
        request = instances_pb2.CreateInstanceRequest(name=name, image=image)
        response = self.client.create_instance(request)
        return response
    

    def delete(self, name):
        """Delete instance"""
        request = instances_pb2.DeleteInstanceRequest(name=name)
        response = self.client.delete_instance(request)
        return response


    def suspend(self, name):
        """Suspend instance"""
        request = instances_pb2.SuspendInstanceRequest(name=name)
        response = self.client.suspend_instance(request)
        return response
    

    def resume(self, name):
        """Resume instance"""
        request = instances_pb2.ResumeInstanceRequest(name=name)
        response = self.client.resume_instance(request)
        return response
    

    def console(self, name):
        """Connect instance"""
        request = instances_pb2.ConsoleInstanceRequest(name=name)
        response = self.client.console_instance(request)
        return response