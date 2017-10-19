import BasePage
import yaml
from Logging import Logging as L
import adb
import time
import sys
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
class BB(BasePage.Base):
    pass
class executeCase:
    def __init__(self,driver,caseName,casePath,resultPath,deviceName,count):
        self.caseName=caseName.split('.')[0]
        self.casePath=casePath
        self.deviceName=deviceName
        self.resultPath=resultPath
        self.driver = BB(driver)
        self.count = count
    def read_case(self):
        with open(self.casePath) as f:
            case = yaml.load(f)
            f.close()
        return case
    def save_result(self):
        error_file = self.resultPath + '\status\%s_%s.yaml' %(self.caseName,self.count)
        return error_file
    def screen_shot(self):
        screen = self.resultPath + '\img\%s_%s.png' %(self.caseName,self.count)
        try:
            self.driver.save_screenshot(screen)
        except:
            L.error('Appium screenshot err, now use adb screenshot')
            adb.get_screenshot(self.deviceName,screen)
        return screen
    def execute_case(self):
        cases = self.read_case()
        L.success('get cases %s' % cases)
        self.logcat()
        for case in cases:
            for action in case.keys():
                try:
                    if action == 'click_by_id':
                        id = case[action]
                        self.driver.find_element_by_id(id).click()
                    elif action == 'click_by_text':
                        text = case[action]
                        self.driver.find_element_by_android_uiautomator(text).click()
                    elif action == 'click_by_position':
                        position = case[action]
                        self.driver.tap(position)
                    elif action == 'keyevent':
                        keyevent = case[action]
                        self.driver.keyevent(keyevent)
                    elif action == 'sleep':
                        t = case[action]
                        L.info('sleep %s seconds !' % str(t))
                        time.sleep(t)
                    elif action == 'find_id':
                        id = case[action]
                        self.driver.find_element_by_id(id)
                    elif action == 'find_text':
                        text == case[action]
                        self.driver.find_element_by_android_uiautomator(text)
                    elif action == 'assert':
                        aa = []
                        assertion = str(case[action]).split(',')
                        page = self.driver.assertion()
                        for i in assertion:
                            if i:
                                aa.append(i)
                        for ve in aa:
                            assert page.find(ve) != -1
                            L.success('assert {}'.format(ve))
                    elif action == 'or_assert':
                        verifications = []
                        verification = case[action]
                        page = self.driver.assertion()
                        for v in verification.split(','):
                            if v:
                                verifications.append(v)
                        result = []
                        for ve in verifications:
                            re = page.find(ve)
                            result.append(re)
                        l = len(result)
                        if result.count('-1') == l:
                            raise Exception ("can't find any element in %s page" % verification)
                    elif action == 'current_activity':
                        current_activity = case[action]
                        print self.driver.currentActivity()
                        assert current_activity == self.driver.currentActivity()
                except Exception,e:
                    traceback.print_exc()
                    return traceback.format_exc()
        return True
    def logcat(self):
        log_file = self.resultPath + '\\log\\%s_%s.log' % (self.caseName,self.count)
        adb.adb_logcat(self.deviceName,log_file)
        L.info('begin to logcat %s !' % log_file)
    def main(self):
        result = self.execute_case()
        with open(self.save_result(),'w') as f:
            yaml.dump({'error_msg': result}, f)
            f.close()
        self.screen_shot()

if __name__ == '__main__':
    a = executeCase()
    a.read_case()