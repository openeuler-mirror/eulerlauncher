import functools
import json
import random
import uuid
import subprocess
import time
from threading import Thread
from lxml import etree

from google.protobuf.json_format import MessageToDict

def asyncwrapper(fn):
    def wrapper(*args, **kwargs):
        thr = Thread(target=fn, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def response2dict(fn):
    @functools.wraps(fn)
    def wrap(*args, **kwargs):
        response = fn(*args, **kwargs)
        response = MessageToDict(response)
        return response

    return wrap


def check_format(file_name, to_check):
    
    ret = False
    ret_fmt = None

    for fmt in to_check:
        if file_name.endswith(fmt):
            ret = True
            ret_fmt = fmt
            break
    
    return ret, ret_fmt


def load_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as fr:
        data = json.load(fr)
        
    return data


def xml_find_and_set(xml, xpath, attribute=None, value=None):
    namespaces = xml.getroot().nsmap
    elements = xml.xpath(xpath, namespaces=namespaces)
    if attribute is not None:
        if value is not None:
            elements[0].set(attribute, value)
        return elements[0].get(attribute)
    else:
        if value is not None:
            elements[0].text = value
        return elements[0].text
    

def save_json_data(json_file, data):
    with open(json_file, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, indent=4, ensure_ascii=False)


def load_xml_data(xml_file):
    data = etree.parse(xml_file)
    return data


def save_xml_data(xml_file, data):
    with open(xml_file, 'wb') as fw:
        fw.write(etree.tostring(data, pretty_print=True, encoding='utf-8'))


def generate_mac_address():
    local_mac = uuid.uuid1().hex[-12:]

    mac = [random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    s = [local_mac[0:2], local_mac[2:4], local_mac[4:6], local_mac[6:8]]
    for item in mac:
        s.append(str("%02x" % item))

    return (':'.join(s))


def parse_ip_address(mac_address):
    ip_address = ''
    cmd = 'arp -a'
    start_time = time.time()
    while(ip_address == '' and time.time() - start_time < 20):
        pr = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        arp_result = pr.stdout.decode('utf-8').split('\n')
        founded = False
        for str in arp_result:
            # The result for 'arp -a' in MacOS is different with Linux, it erase
            # the first 0 if the first digit is 0 for this mac section, add it
            # back before compare
            try:
                arp_ip = str.split(' ')[1].replace("(", "").replace(")", "")
                mac = str.split(' ')[3].replace("(", "").replace(")", "")
            except IndexError:
                continue
            mac_list = mac.split(':')
            for i in range(0, len(mac_list)):
                if len(mac_list[i]) == 1:
                    mac_list[i] = '0' + mac_list[i]
            mac_0 = ':'.join(mac_list)
            if mac_address == mac_0:
                ip_address = arp_ip
                founded = True
                break
        if founded:
            break
    
    return ip_address
