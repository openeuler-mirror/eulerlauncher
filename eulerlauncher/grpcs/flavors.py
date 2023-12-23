from eulerlauncher.grpcs.eulerlauncher_grpc import flavors_pb2


class Flavor(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        """Get list of flavors"""
        request = flavors_pb2.ListFlavorsRequest()
        response = self.client.list_flavors(request)
        return response

    def create(self, name, cpu, ram, disk):
        """Create a new flavor"""
        request = flavors_pb2.CreateFlavorRequest(
            flavor_name=name, cpucores_num=cpu, ram_capacity=ram, disk_capacity=disk)
        response = self.clent.create_flavor(request)
        return response

    def delete(self, name):
        """Delete the requested flavor"""
        request = flavors_pb2.DeleteFlavorRequest(name=name)
        response = self.client.delete_image(request)
        return response
