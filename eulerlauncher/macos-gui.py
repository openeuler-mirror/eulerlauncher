import os
import PIL.Image
import pystray
import subprocess
import shutil
import signal
import sys

CONF_DIR_SHELL = '/Library/Application\ Support/org.openeuler.eulerlauncher/eulerlauncher.conf'
CONF_DIR = '/Library/Application Support/org.openeuler.eulerlauncher/eulerlauncher.conf'


if __name__ == '__main__':
    try:
        base_dir = os.path.dirname(__file__)
        logo_file = os.path.join(base_dir,'./etc/favicon.png')
        logo = PIL.Image.open(logo_file)

        def on_clicked(icon, item):
            icon.stop()
        
        icon = pystray.Icon('EulerLauncher', logo, menu=pystray.Menu(
            pystray.MenuItem('Exit EulerLauncher', on_clicked)
        ))

    except Exception as e:
        print('Error: ' + str(e))
    else:
        os.environ['PATH'] += ':/opt/homebrew/bin:/opt/homebrew/sbin'
        
        libvirtd_bin = shutil.which('libvirtd')
        libvirtd_cmd = ['sudo', libvirtd_bin]
        libvirtd = subprocess.Popen(' '.join(libvirtd_cmd), shell=True, preexec_fn=os.setsid)

        virtlogd_bin = shutil.which('virtlogd')
        virtlogd_cmd = ['sudo', virtlogd_bin]
        virtlogd = subprocess.Popen(' '.join(virtlogd_cmd), shell=True, preexec_fn=os.setsid)

        launcherd_bin = os.path.join(base_dir, './bin/eulerlauncherd')
        launcherd_cmd = ['sudo', launcherd_bin, CONF_DIR_SHELL]
        launcherd = subprocess.Popen(' '.join(launcherd_cmd), shell=True, preexec_fn=os.setsid)

        def term_handler(signum, frame):
            subprocess.check_call(['sudo', 'kill', str(launcherd.pid)])
            subprocess.check_call(['sudo', 'kill', str(virtlogd.pid)])
            subprocess.check_call(['sudo', 'kill', str(libvirtd.pid)])

        # Avoid create orphan children in MacOS and Linux
        signal.signal(signal.SIGTERM, term_handler)

        icon.run()
        
        # Shutdown eulerlauncherd, we created it with sudo, so kill it with sudo
        subprocess.check_call(['sudo', 'kill', str(launcherd.pid)])
        os.waitpid(launcherd.pid, 0)
        subprocess.check_call(['sudo', 'kill', str(virtlogd.pid)])
        os.waitpid(virtlogd.pid, 0)
        subprocess.check_call(['sudo', 'kill', str(libvirtd.pid)])
        os.waitpid(libvirtd.pid, 0)

        sys.exit(0)