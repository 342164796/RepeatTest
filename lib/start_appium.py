# -*- coding utf-8 -*-
import subprocess
from adb import cmd,connect
from Logging import Logging as L
from time import sleep
import random
import platform
class startAppium:
    def __init__(self,device):
        self.device = device
    def __start_appium(self,aport,bport):
        if platform.system() == 'Windows':
            subprocess.Popen("appium -p %s -bp %s -U %s" %
                            (aport,bport,self.device),shell=True)
        else:
            appium = cmd('appium -p %s -bp %s -U %s' %
                           (aport, bpport, self.device))
            while True:
                appium_line = appium.stdout.readline().strip()
                L.Logging.debug(appium_line)
                if 'listener started' in appium_line:
                    break
    def start_appium(self):
        aport = random.randint(4700, 4900)
        bport = random.randint(4700, 4900)
        self.__start_appium(aport,bport)
        count = 20
        for i in range(count):
            appium = cmd('netstat -aon | findstr %d' % aport).stdout.readline()
            if appium:
                L.info('start appium :p %s bp %s device: %s' %
                    (aport,bport,self.device))
                return aport
            else:
                L.info('waiting start appium 3 seconds!')
                sleep(3)
    def main(self):
        return self.start_appium()

def shutdown_appium(port,device):
    line = cmd('netstat -aon | findstr %d' % port).stdout.readline()
    pid = line.strip().split(' ')[-1]
    cmd('taskkill /f /pid {}'.format(pid))
    L.success("killed appium %s" % port)
    clean_logcat(device)
    reconnect_device(device)
def clean_logcat(device):
    pid = cmd('netstat -aon | findstr %s' % device).stdout.readline().strip().split(' ')[-1]
    cmd('taskkill /f /pid %s' % pid)
    sleep(2)
    L.success('stop logcat %s' % device)
def reconnect_device(device):
    connect(device)
    sleep(2)
    L.success('reconnect device %s' % device)