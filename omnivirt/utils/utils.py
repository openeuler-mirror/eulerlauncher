import functools
import json
import os
import random
from threading import Thread
import uuid


from google.protobuf.json_format import MessageToDict

from omnivirt.utils import exceptions
from omnivirt.utils import objs


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


def parse_config(args):
    if len(args) != 2 or args[0] != '--config-file':
        raise exceptions.NoConfigFileProvided
    if not os.path.exists(args[1]):
        raise exceptions.NoSuchFile(file=args[1])

    return objs.Conf(args[1])


def format_mac_addr(mac_str):
    ret = ''
    if len(mac_str) != 12:
        return ret
    mac_low = mac_str.lower()
    for i in range(0, 5):
        ret = ret + mac_low[2 * i] + mac_low[2 * i + 1] + '-'
    ret = ret + mac_low[-2] + mac_low[-1]
    
    return ret

def load_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as fr:
            data = json.load(fr)
        
    return data

def save_json_data(json_file, data):
    with open(json_file, 'w', encoding='utf-8') as fw:
            json.dump(data, fw, indent=4, ensure_ascii=False)

def generate_mac():
    local_mac = uuid.uuid1().hex[-12:]

    mac = [random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    s = [local_mac[0:2], local_mac[2:4], local_mac[4:6], local_mac[6:8]]
    for item in mac:
        s.append(str("%02x" % item))

    return (':'.join(s))

def catch_exception(func):

    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise exceptions.OmniVirtdNotAvailable
    
    return wrap

def check_file_tail(file_name, to_check):
    
    ret = False
    ret_fmt = None

    for fmt in to_check:
        if file_name.endswith(fmt):
            ret = True
            ret_fmt = fmt
            break
    
    return ret, ret_fmt
