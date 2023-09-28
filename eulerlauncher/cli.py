import click
import prettytable as pt
import getpass

from eulerlauncher.grpcs import client


launcher_client = client.Client()

# List all instances on the host
@click.command()
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


# List all usable images
@click.command()
def images():

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


@click.command()
@click.argument('name')
def download_image(name):

    try:
        ret = launcher_client.download_image(name)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])


@click.command()
@click.argument('name')
@click.option('--path', help='Image file to load')
def load_image(name, path):

    try:
        ret = launcher_client.load_image(name, path)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])


@click.command()
@click.argument('name')
def delete_image(name):

    try:
        ret = launcher_client.delete_image(name)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])


@click.command()
@click.argument('name')
def delete_instance(name):

    try:
        ret = launcher_client.delete_instance(name)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])

@click.command()
@click.argument('vm_name')
@click.option('--image', help='Image to build vm')
def launch(vm_name, image):

    try:
        ret = launcher_client.create_instance(vm_name, image)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:

        if ret['ret'] == 1:
            tb = pt.PrettyTable()
            tb.field_names = ["Name", "Image", "State", "IP"]
            tb.add_row(
                [ret['instance']['name'],
                ret['instance']['image'],
                ret['instance']['vmState'],
                ret['instance']['ipAddress']])

            print(tb)
    
        else:
            print(ret['msg'])

@click.command()
@click.argument('vm_name')
@click.option('--snapshot_name', help='name for the snapshot image')
@click.option('--export_path', help='path for the exported snapshot image')
def take_snapshot(vm_name, snapshot_name, export_path):

    try:
        ret = launcher_client.take_snapshot(vm_name, snapshot_name, export_path)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])

@click.command()
@click.argument('vm_name')
@click.option('--image_name', help='name for the Python/Go/Java development image')
@click.option('--export_path', help='path for the exported Python/Go/Java development image')
def export_development_image(vm_name, image_name, export_path):

    try:
        pwd = getpass.getpass(f"Password for vm[{vm_name}] as root: ")
        ret = launcher_client.export_development_image(vm_name, image_name, export_path, pwd)
    except Exception:
        print('Calling to EulerLauncherd daemon failed, please check EulerLauncherd daemon status ...')
    else:
        print(ret['msg'])

@click.group()
def cli():
    pass


if __name__ == '__main__':
    cli.add_command(list)
    cli.add_command(images)
    cli.add_command(download_image)
    cli.add_command(load_image)
    cli.add_command(launch)
    cli.add_command(delete_image)
    cli.add_command(delete_instance)
    cli.add_command(take_snapshot)
    cli.add_command(export_development_image)
    cli()