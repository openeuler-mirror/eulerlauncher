import os
import PIL.Image
import platform
import pystray
import subprocess
import signal
import sys

from omnivirt.utils import constants
from omnivirt.utils import objs


CONF_DIR_SHELL = '/Library/Application\ Support/org.openeuler.omnivirt/omnivirt.conf'
CONF_DIR = '/Library/Application Support/org.openeuler.omnivirt/omnivirt.conf'

# Avoid create zombie children in MacOS and Linux
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

if __name__ == '__main__':
    try:
        host_arch_raw = platform.uname().machine
        host_arch = constants.ARCH_MAP[host_arch_raw]
        base_dir = os.path.dirname(__file__)


        conf_file = CONF_DIR
        logo_file = os.path.join(base_dir,'./etc/favicon.png')

        CONF = objs.Conf(conf_file)

        logo = PIL.Image.open(logo_file)

        def on_clicked(icon, item):
            
            icon.stop()
        
        icon = pystray.Icon('OmniVirt', logo, menu=pystray.Menu(
            pystray.MenuItem('Exit OmniVirt', on_clicked)
        ))

    except Exception as e:
        print('Error: ' + str(e))
    else:
        omnivirtd_cmd = ['sudo', os.path.join(base_dir,'./bin/OmniVirtd'), CONF_DIR_SHELL, base_dir]
        omnivirtd = subprocess.Popen(' '.join(omnivirtd_cmd), shell=True, preexec_fn=os.setsid)

        def term_handler(signum, frame):
            subprocess.check_call(['sudo', 'kill', str(omnivirtd.pid)])

        # Avoid create orphan children in MacOS and Linux
        signal.signal(signal.SIGTERM, term_handler)

        icon.run()
        
        # Shutdown omnivirtd, we created it with sudo, so kill it with sudo
        subprocess.check_call(['sudo', 'kill', str(omnivirtd.pid)])
        os.waitpid(omnivirtd.pid, 0)
        sys.exit(0)