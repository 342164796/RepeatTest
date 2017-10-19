# -*- coding:utf-8 -*-
import os
import subprocess
def cmd(args):
    return subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
def adb_devices():
    print cmd('adb devices')
def adb_logcat_c(deviceName):
    return cmd('adb -s %s logcat -c' % deviceName)
def adb_logcat(deviceName,log_path):
    adb_logcat_c(deviceName)
    return cmd('adb -s %s logcat -v time > %s&' % (deviceName,log_path))
def get_screenshot(deviceName,file_path):
    os.system('adb -s %s shell screencap -p /data/local/tmp/screencap.png' % deviceName)
    os.system('adb -s %s pull /data/local/tmp/screencap.png %s' % (deviceName, file_path))
    return file_path
def connect(deviceName):
    device = deviceName.split(':')[0]
    return cmd('adb connect %s' % device)
if __name__ == "__main__":
    adb_devices()