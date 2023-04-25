import platform
import subprocess
import os

from omnivirt.utils import constants


class QemuDriver(object):

    def __init__(self, conf, logger) -> None:
        host_arch_raw = platform.uname().machine
        host_arch = constants.ARCH_MAP[host_arch_raw]
        self.qemu_bin = conf.conf.get('default', 'qemu_dir')
        self.uefi_file = os.path.join('/Library/Application\ Support/org.openeuler.omnivirt/','edk2-' + host_arch + '-code.fd')
        self.uefi_params = ',if=pflash,format=raw,readonly=on'
        self.vm_cpu = conf.conf.get('vm', 'cpu_num')
        self.vm_ram = conf.conf.get('vm', 'memory')
        self.LOG = logger
    
    def create_vm(self, vm_name, vm_uuid, vm_mac, vm_root_disk):
        qemu_cmd = [
            self.qemu_bin,  '-machine', 'virt,highmem=off', '-name', vm_name, '-uuid', vm_uuid,
            '-accel hvf', '-drive', 'file=' + self.uefi_file + self.uefi_params, '-cpu host',
            '-nic', 'vmnet-shared,model=virtio-net-pci,mac=' + vm_mac,
            '-drive', 'file=' + vm_root_disk, '-device', 'virtio-scsi-pci,id=scsi0',
            '-smp', self.vm_cpu, '-m', self.vm_ram + 'M', '-monitor none -chardev null,id=char0',
            '-serial chardev:char0 -nographic']
        self.LOG.debug(' '.join(qemu_cmd))
        instance_process = subprocess.Popen(' '.join(qemu_cmd), shell=True)
        return instance_process
