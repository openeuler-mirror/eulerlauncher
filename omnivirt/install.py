import os
import subprocess


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)

    print('Welcome to use OmniVirt, a tool allows users to develop openEuler on favourate desktop.')
    print('Creating folder for supporting files ...')

    folder_cmd = ['sudo', 'mkdir', '-p', '/Library/Application\ Support/org.openeuler.omnivirt']
    subprocess.run(' '.join(folder_cmd), shell=True)

    print('Copy all supporting files to the folder ...')
    cp_cmd = ['sudo', 'cp -r', os.path.join(base_dir,'./etc/*'), '/Library/Application\ Support/org.openeuler.omnivirt/']
    subprocess.run(' '.join(cp_cmd), shell=True)

    print('Change supporting file rights ...')
    chmod_cmd = ['sudo', 'chmod -R', '775', '/Library/Application\ Support/org.openeuler.omnivirt/']
    subprocess.run(' '.join(chmod_cmd), shell=True)

    print('Create softlink for the CLI binary ...')
    ln_cmd = ['sudo', 'ln', '-s', '/Library/Application\ Support/org.openeuler.omnivirt/omnivirt', '/usr/local/bin/']
    subprocess.run(' '.join(ln_cmd), shell=True)

    print('Done ...')
    print('Please update omnivirt.conf according to your own environment, enjoy your openEuler trip ...')