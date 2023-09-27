import click
import prettytable as pt

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
@click.option('--arch', default='x86', type=click.Choice(['x86', 'arm'], case_sensitive=False), help='Architecture of instance')
def launch(vm_name, image, arch):

    try:
        ret = launcher_client.create_instance(vm_name, image, arch)
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


# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name', help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)

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
    cli()

