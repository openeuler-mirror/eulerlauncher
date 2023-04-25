from omnivirt.grpcs.omnivirt_grpc import images_pb2


class Image(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        """Get list of images"""
        request = images_pb2.ListImageRequest()
        response = self.client.list_images(request)
        return response
    
    def download(self, name):
        """Download the requested image"""
        request = images_pb2.DownloadImageRequest(name=name)
        response = self.client.download_image(request)
        return response

    def load(self, name, path):
        """Load local image file"""
        request = images_pb2.LoadImageRequest(name=name, path=path)
        response = self.client.load_image(request)
        return response

    def delete(self, name):
        """Delete the requested image"""
        request = images_pb2.DeleteImageRequest(name=name)
        response = self.client.delete_image(request)
        return response