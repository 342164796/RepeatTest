# -*- coding:utf-8 -*-
from adb import adb_devices,cmd
from util import configIni
import Logging as L
import yaml
import os
def get_device_name():
    devices = cmd('adb devices').stdout.readlines()
    device_list=[]
    for device in devices:
        if 'device' in device and 'devices' not in device:
            device = device.split('\t')[0]
            device_list.append(device)
    return device_list
def get_android_version():
    for version in cmd('adb shell getprop').stdout.readlines():
        if 'ro.build.version.release' in version:
            version = version.split(':')[1].strip().strip('[]')
            return version
def get_device_detail():
    for device in get_device_name():
        device_detail={}
        device_detail['deviceName'] = device
        device_detail['platformVersion'] = get_android_version()
    L.Logging.info('get device details: %s' % device_detail)
    return device_detail
def set_device_yaml():
    device_lst = get_device_detail()
    ini = configIni()
    with open(ini.get_ini('test_device','device'), 'w') as f:
        yaml.dump(device_lst, f)
        f.close()
def clean_device_yaml():
    ini = configIni()
    device_yaml = ini.get_ini('test_device','device')
    if os.path.getsize(device_yaml):
        with open(device_yaml, 'w') as f:
            f.truncate()
            f.close()
        return
    return
if __name__ == '__main__':
    set_device_yaml()