import os
import libvirt
import shutil
import platform

from eulerlauncher.utils import constants
from eulerlauncher.utils import utils


class MacInstanceHandler(object):
    
    def __init__(self, CONF, work_dir, instance_dir, image_dir, LOG) -> None:
        self.conf = CONF
        self.work_dir = work_dir
        self.instance_dir = instance_dir
        self.instance_record_file = os.path.join(instance_dir, 'instances.json')
        self.image_dir = image_dir
        self.image_record_file = os.path.join(image_dir, 'images.json')
        self.LOG = LOG

    def list_instances(self):
        instance_record = utils.load_json_data(self.instance_record_file)
        all_instances = list(instance_record.values())
        return all_instances

    def create_instance(self, name, image):
        image_record = utils.load_json_data(self.image_record_file)
        if image not in image_record['local'].keys():
            self.LOG.debug(f'Image: {image} is not available locally')
            return 1
        
        instance_record = utils.load_json_data(self.instance_record_file)
        if name in instance_record.keys():
            self.LOG.debug(f'Instance: {name} already exist')
            return 2
        
        instance_path = os.path.join(self.instance_dir, name)
        os.makedirs(instance_path)
        image_path = image_record['local'][image]['path']
        disk_path = shutil.copyfile(image_path, os.path.join(instance_path, image))
        host_arch_raw = platform.uname().machine
        host_arch = constants.ARCH_MAP[host_arch_raw]
        xml_file = os.path.join('/Library/Application Support/org.openeuler.eulerlauncher/','libvirt-' + host_arch + '.xml')
        xml = utils.load_xml_data(xml_file)
        vcpu = self.conf.conf.get('vm', 'cpu_num')
        ram = self.conf.conf.get('vm', 'memory')

        def xml_find_and_set(xml, xpath, attribute=None, value=None):
            elements = xml.xpath(xpath)
            if attribute is not None:
                if value is not None:
                    elements[0].set(attribute, value)
                return elements[0].get(attribute)
            else:
                if value is not None:
                    elements[0].text = value
                return elements[0].text

        xml_find_and_set(xml, 'name', value=name)
        xml_find_and_set(xml, 'vcpu', value=vcpu)
        xml_find_and_set(xml, 'memory', value=ram)
        xml_find_and_set(xml, 'devices/emulator', value=self.conf.conf.get('default', 'qemu_dir'))
        xml_find_and_set(xml, 'devices/disk/source', 'file', disk_path)
        xml_find_and_set(xml, 'devices/interface/mac', 'address', utils.generate_mac())
        utils.save_xml_data(xml_file, xml)
        
        conn = libvirt.open("qemu:///session")
        with open(xml_file, 'r') as pr:
            dom = conn.createLinux(pr.read())
        
        instance_record[name] = {
            'id': dom.ID(),
            'name': name,
            'state': constants.INSTANCE_STATE_MAP[dom.state()[0]],
            'vcpu': dom.maxVcpus(),
            'ram': dom.maxMemory() // 1024,
            'image': image,
            'mac_address': '',
            'ip_address': 'N/A',
            'path': instance_path
        }
        utils.save_json_data(self.instance_record_file, instance_record)
        conn.close()
        return 0

    def delete_instance(self, name):
        instance_record = utils.load_json_data(self.instance_record_file)

        conn = libvirt.open("qemu:///session")
        dom = conn.lookupByName(name)

        if dom is not None:
            dom.destroy()
            self.LOG.debug(f'Instance: {name} succesfully killed ...')
        else:
            self.LOG.debug(f'Instance: {name} already stopped, skip ...')

        # Cleanup files and records
        instance_path = instance_record[name]['path']
        shutil.rmtree(instance_path)
        del instance_record[name]

        utils.save_json_data(self.instance_record_file, instance_record)
        conn.close()
        return 0

