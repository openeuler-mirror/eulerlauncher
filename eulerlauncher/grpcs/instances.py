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

    def take_snapshot(self, vm_name, snapshot_name, export_path):
        """Take snapshot"""
        request = instances_pb2.TakeSnapshotRequest(name=vm_name, snapshot=snapshot_name, dest_path=export_path)
        response = self.client.take_snapshot(request)
        return response

    def export_development_image(self, vm_name, image_name, export_path, pwd):
        """Export Python/Go/Java development image"""
        request = instances_pb2.ExportDevelopmentImageRequest(name=vm_name, image=image_name, dest_path=export_path, pwd=pwd)
        response = self.client.export_development_image(request)
        return response