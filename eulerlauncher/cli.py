import click
import prettytable as pt

from eulerlauncher.grpcs import client


launcher_client = client.Client()


@click.group(
    name="image",
    help="Command for managing images "
)
def image():
    pass


# List all usable images
@image.command()
def list():

    try:
        ret = launcher_client.list_images()
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        tb = pt.PrettyTable()

        tb.field_names = ["Images", "Location", "Status"]

        for image in ret['images']:
            tb.add_row(
                [image['name'], image['location'], image['status']])

        print(tb)


@image.command()
@click.argument('name')
def download(name):

    try:
        ret = launcher_client.download_image(name)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])


@image.command()
@click.argument('name')
@click.option('--path', help='Image file to load')
def load(name, path):

    try:
        ret = launcher_client.load_image(name, path)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])


@image.command()
@click.argument('name')
def delete(name):

    try:
        ret = launcher_client.delete_image(name)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])


@click.group(
    name="instance",
    help="Command for managing instances "
)
def instance():
    pass


# List all instances on the host
@instance.command()
def list():

    try:
        ret = launcher_client.list_instances()
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        tb = pt.PrettyTable()

        tb.field_names = ["Name", "Image", "State", "IP"]

        try:
            for instance in ret['instances']:
                tb.add_row(
                    [instance['name'],
                    instance['image'],
                    instance['vmState'],
                    instance['ipAddress']])
        except KeyError:
            pass

        print(tb)


@instance.command()
@click.argument('name')
def delete(name):

    try:
        ret = launcher_client.delete_instance(name)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])

@instance.command()
@click.argument('vm_name')
@click.option('--image', help='Image to build instance')
def launch(vm_name, image):

    try:
        ret = launcher_client.create_instance(vm_name, image)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])


@click.group()
def entrance():
    pass


if __name__ == '__main__':
    entrance.add_command(image)
    entrance.add_command(instance)
    entrance()