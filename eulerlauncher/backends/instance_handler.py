import os
import libvirt
import shutil
import platform
import subprocess

from eulerlauncher.utils import constants
from eulerlauncher.utils import utils

class MacInstanceHandler(object):
    
    def __init__(self, CONF, work_dir, instance_dir, image_dir, LOG) -> None:
        self.CONF = CONF
        self.work_dir = work_dir
        self.instance_dir = instance_dir
        self.instance_record_path = os.path.join(instance_dir, 'instances.json')
        self.image_dir = image_dir
        self.image_record_path = os.path.join(image_dir, 'images.json')
        self.LOG = LOG


    def list_instances(self):
        instance_record = utils.load_json_data(self.instance_record_path)
        all_instances = list(instance_record.values())
        return all_instances


    def create_instance(self, name, image):
        image_record = utils.load_json_data(self.image_record_path)
        if image not in image_record['local'].keys():
            self.LOG.debug(f'Image: {image} is not available locally')
            return 1
        
        instance_record = utils.load_json_data(self.instance_record_path)
        if name in instance_record.keys():
            self.LOG.debug(f'Instance: {name} already exist')
            return 2
        
        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        image_path = image_record['local'][image]['path']
        disk_path = shutil.copyfile(image_path, os.path.join(instance_path, image))
        host_arch_raw = platform.uname().machine
        host_arch = constants.ARCH_MAP[host_arch_raw]
        xml_path = os.path.join('/Library/Application Support/org.openeuler.eulerlauncher/','libvirt-' + host_arch + '.xml')
        xml = utils.load_xml_data(xml_path)
        vcpu = self.CONF.get('vm', 'cpu_num')
        ram = self.CONF.get('vm', 'memory')
        qemu_bin = self.CONF.get('default', 'qemu_bin')
        mac_address = utils.generate_mac_address()

        utils.xml_find_and_set(xml, 'name', value=name)
        utils.xml_find_and_set(xml, 'vcpu', value=vcpu)
        utils.xml_find_and_set(xml, 'memory', value=ram)
        utils.xml_find_and_set(xml, 'devices/emulator', value=qemu_bin)
        utils.xml_find_and_set(xml, 'devices/disk/source', 'file', disk_path)
        qemu_arg = 'driver=virtio-net-pci,netdev=eth0,mac=' + mac_address
        utils.xml_find_and_set(xml, 'qemu:commandline/qemu:arg[2]', 'value', qemu_arg)
        utils.save_xml_data(xml_path, xml)
        
        conn = libvirt.open("qemu:///system")
        with open(xml_path, 'r') as pr:
            dom = conn.createLinux(pr.read())

        with open(os.path.join(instance_path, name), 'w') as pw:
            xml_dec = dom.XMLDesc()
            pw.write(xml_dec)

        ip_address = utils.parse_ip_address(mac_address)
    
        instance_record[name] = {
            'id': dom.ID(),
            'name': name,
            'state': constants.INSTANCE_STATE_MAP[dom.state()[0]],
            'vcpu': vcpu,
            'ram': ram,
            'image': image,
            'mac_address': mac_address,
            'ip_address': ip_address,
            'path': instance_path
        }
        utils.save_json_data(self.instance_record_path, instance_record)
        conn.close()
        self.LOG.debug(f'Instance: {name} succesfully created ...')
        return 0


    def delete_instance(self, name):
        instance_record = utils.load_json_data(self.instance_record_path)
        if name not in instance_record.keys():
            self.LOG.debug(f'Instance: {name} does not exist')
            return 1

        conn = libvirt.open("qemu:///system")
        dom = conn.lookupByName(name)
        dom.destroy()
        # Cleanup files and records
        instance_path = instance_record[name]['path']
        shutil.rmtree(instance_path)
        del instance_record[name]

        utils.save_json_data(self.instance_record_path, instance_record)
        conn.close()
        self.LOG.debug(f'Instance: {name} succesfully killed ...')
        return 0
    

    def suspend_instance(self, name):
        instance_record = utils.load_json_data(self.instance_record_path)
        if name not in instance_record.keys():
            self.LOG.debug(f'Instance: {name} does not exist')
            return 1
        
        conn = libvirt.open("qemu:///system")
        dom = conn.lookupByName(name)
        dom.suspend()
        
        instance_record[name]['state'] = constants.INSTANCE_STATE_MAP[dom.state()[0]]

        utils.save_json_data(self.instance_record_path, instance_record)
        conn.close()
        self.LOG.debug(f'Instance: {name} succesfully suspended ...')
        return 0


    def resume_instance(self, name):
        instance_record = utils.load_json_data(self.instance_record_path)
        if name not in instance_record.keys():
            self.LOG.debug(f'Instance: {name} does not exist')
            return 1
        
        conn = libvirt.open("qemu:///system")
        dom = conn.lookupByName(name)
        dom.resume()
        
        instance_record[name]['state'] = constants.INSTANCE_STATE_MAP[dom.state()[0]]

        utils.save_json_data(self.instance_record_path, instance_record)
        conn.close()
        self.LOG.debug(f'Instance: {name} succesfully resumed ...')
        return 0
    

    def console_instance(self, name):
        instance_record = utils.load_json_data(self.instance_record_path)
        if name not in instance_record.keys():
            self.LOG.debug(f'Instance: {name} does not exist')
            return 1
        
    #    instance_path = instance_record[name]['path']
    #    xml_path = os.path.join(instance_path, name)
    #    xml = utils.load_xml_data(xml_path)
    #    address = utils.xml_find_and_set(xml, 'devices/graphics[@type="vnc"]/listen', "address")
    #    port = utils.xml_find_and_set(xml, 'devices/graphics[@type="vnc"]', "port")
        
        virt_viewer_bin = self.CONF.get('default', 'virt-viewer_bin')
        virt_viewer_cmd = ['sudo', virt_viewer_bin, name]
        subprocess.Popen(' '.join(virt_viewer_cmd), shell=True, preexec_fn=os.setsid)
        
        return 0