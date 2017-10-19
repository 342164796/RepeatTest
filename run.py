# -*- coding:utf-8 -*-
from lib.set_yaml import set_device_yaml,clean_device_yaml
#import lib.set_yaml
from lib.util import configIni
from lib.Logging import Logging as L
import yaml
from lib.start_test import start_test
def start():
    clean_device_yaml()
    set_device_yaml()
    appium_info=get_start_param()
    if len(appium_info) == 0:
        L.error('device is NULL !!!')
    else:
        s = start_test(appium_info)
        s.start_test()

def get_start_param():
    ini = configIni()
    appium_param = ini.get_ini('appium_info','appium_parameter')
    device_param = ini.get_ini('test_device','device')
    with open(appium_param)as f:
        appium_dict = yaml.load(f)
        f.close()
    with open(device_param) as f:
        device_dict = yaml.load(f)
        f.close
    appium_info = dict(appium_dict.items() + device_dict.items())
    return appium_info
if __name__ == '__main__':
    start()