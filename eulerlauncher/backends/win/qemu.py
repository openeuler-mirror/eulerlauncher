import platform
import subprocess
import os

from eulerlauncher.utils import constants


class QemuDriver(object):

    def __init__(self, conf, logger) -> None:
        host_arch_raw = platform.uname().machine
        host_arch = constants.ARCH_MAP[host_arch_raw]
        self.qemu_bin = conf.conf.get('default', 'qemu_dir')
        self.uefi_file = os.path.join('C:/Users\WSJ\Desktop\eulerlauncher-v0.3/resources\qemu/',
                                      'edk2-' + host_arch + '-code.fd')
        self.uefi_params = ',if=pflash,format=raw,readonly=on'
        self.vm_cpu = conf.conf.get('vm', 'cpu_num')
        self.vm_ram = conf.conf.get('vm', 'memory')
        self.path = os.getcwd()
        self.LOG = logger

    def create_vm(self, vm_name, vm_uuid, vm_mac, vm_root_disk, arch='x86'):
        if arch == 'x86':
            qemu_cmd = [self.qemu_bin+'\qemu-system-x86_64',
                '-name', vm_name, '-uuid', vm_uuid,
                '-net nic,macaddr=' + vm_mac,
                '-net tap,ifname=tap0,script=no,downscript=no',
                '-drive', 'file=' + vm_root_disk+',id=hd0,format=qcow2,media=disk',
                '-smp', self.vm_cpu, '-m', self.vm_ram, '-monitor none -chardev null,id=char0',
                '-serial chardev:char0 -nographic']
        else:
            qemu_cmd = [self.qemu_bin+'\qemu-system-aarch64',
                '-name', vm_name, '-uuid', vm_uuid,
                '-net nic,macaddr=' + vm_mac,
                '-net tap,ifname=tap0,script=no,downscript=no',
                '-drive if=virtio,file='+vm_root_disk+',id=hd0,format=qcow2,media=disk',
                '-smp', self.vm_cpu, '-m', self.vm_ram, '-cpu cortex-a72 --accel tcg,thread=multi -M virt',
                '-device VGA', '-bios', self.path+'\qemu\QEMU_EFI.fd',
                '-device nec-usb-xhci -device usb-tablet -device usb-kbd -nographic']
        #qemu_cmd = ' '.join(qemu_cmd)
        #powershell_cmd = ['powershell.exe','Start-Process -WindowStyle hidden -FilePath', '"'+self.qemu_bin+'"', '-ArgumentList', '{'+qemu_cmd+'}']
        #self.LOG.debug(' '.join(powershell_cmd))
        #instance_process = subprocess.run(' '.join(powershell_cmd), shell=True)

        #self.LOG.debug(instance_process.Id)
        # si = subprocess.STARTUPINFO()
        # si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        instance_process = subprocess.Popen(' '.join(qemu_cmd), shell=True)
        self.LOG.debug(' '.join(qemu_cmd))
        # self.LOG.debug(self.path)
        return instance_process
