import platform
import subprocess
import os

from eulerlauncher.utils import constants


class QemuDriver(object):

    def __init__(self, conf, logger) -> None:
        host_arch_raw = platform.uname().machine
        host_arch = constants.ARCH_MAP[host_arch_raw]
        self.qemu_bin = conf.conf.get('default', 'qemu_dir')
        self.qemu_img_bin = conf.conf.get('default', 'qemu_img_dir')
        self.uefi_file = os.path.join('/Library/Application\ Support/org.openeuler.eulerlauncher/','edk2-' + host_arch + '-code.fd')
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

    def take_and_export_snapshot(self, snapshot_name, vm_root_disk, export_image_name, dest_path):
        take_snapshot_cmd = [
            'sudo', self.qemu_img_bin, 'snapshot', '-c', f'{snapshot_name}', f'{vm_root_disk}'
        ]
        self.LOG.debug(' '.join(take_snapshot_cmd))
        subprocess.call(' '.join(take_snapshot_cmd), shell=True)
        export_image_cmd = [
            'sudo', self.qemu_img_bin, 'convert', '-l', f'snapshot.name={snapshot_name}', '-O',
            'qcow2', f'{vm_root_disk}', os.path.join(dest_path, f'{export_image_name}.qcow2')
        ]
        self.LOG.debug(' '.join(export_image_cmd))
        subprocess.call(' '.join(export_image_cmd), shell=True)