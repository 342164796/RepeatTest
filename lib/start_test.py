# -*- coding:utf-8 -*-
import time
from util import configIni
from start_appium import startAppium,shutdown_appium
from Logging import Logging as L
from time import sleep
from get_case import get_case
from executecase import executeCase
from appium import webdriver
import os
from analysis_log import analysis_log
from generagereport import generatereport
class start_test:
    def __init__(self,device):
        self.device_dict = device
        self.deviceName = self.device_dict['deviceName']
        self.time = time.strftime(
            "%Y-%m-%d_%H_%M_%S",
            time.localtime(time.time())
        )
        self.result_path = self.mkdir_file()
        #self.ini = configIni()
    def mkdir_file(self):
        ini = configIni()
        rpath = ini.get_ini('test_result','log_file')
        result_path = rpath + '\\' + self.time
        file_list = [
            result_path,
            result_path + '\log',
            result_path + '\img',
            result_path + '\status'
        ]
        if not os.path.exists(rpath):
            os.mkdir(rpath)
        for file_path in file_list:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        return result_path
    def start_appium(self):
        sp = startAppium(self.deviceName)
        self.appium_port = sp.main()
        count = 10
        for i in range(count):
            try:
                self.driver = self.get_driver(self.appium_port)
           # if self.driver:
                L.success('appium start % success' % self.deviceName)
                return self.driver
            #else:
            except:

                L.error('Faild to start appium %s !' % self.appium_port)
                continue
            # try:
            #     self.get_driver(self.appium_port)
            # except Exception as e:
            #     L.error('Faild to start appium : {}'.format(e))
    def get_driver(self,appium_p):
        driver = webdriver.Remote(
            'http://127.0.0.1:%s/wd/hub' %
            appium_p, self.device_dict
        )
        sleep(10)
        return driver
    def run_case(self,caseName,casePath,count):
        run = executeCase(
            self.start_appium(),
            caseName,
            casePath,
            self.result_path,
            self.deviceName,
            count
        )
        run.main()
    def start_test(self):
        ini = configIni()
        count = ini.get_ini('test_count','count')
        for i in range(int(count)):
            L.info('this is %s test' % str(i+1))
            test_case = get_case().items()
            if not test_case:
                L.error('testcase not found!!!')
            else:
                for case_name, case_path in test_case:
                    L.info('get testcase %s' % case_path)
                    self.run_case(case_name, case_path, i+1)
                    try:
                        self.driver.quit()
                        L.success('quit driver %s' % self.appium_port)

                    except:
                        L.error('quit driver error %s ' % self.appium_port)
                    shutdown_appium(self.appium_port,self.deviceName)
                    analysisLog = analysis_log(case_name,case_path,self.result_path,i+1)
                    analysisLog.get_log_filter()
        gen = generatereport(self.result_path)
        gen.main()