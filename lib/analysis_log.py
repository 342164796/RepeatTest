# -*- coding:utf-8 -*-
import yaml
from Logging import Logging as L

class analysis_log:
    def __init__(self,logName,case_path,result_path,count):
        self.logName=logName.split('.')[0]
        self.result_path = result_path
        self.count = count
        self.case_path = case_path
    def analysis(self,filter):
        log_file = self.result_path + '\\log\\%s_%s.log' %(self.logName,self.count)
        error_file = self.result_path + '\status\%s_%s.yaml' % (self.logName, self.count)
        with open(log_file) as f:
            for line in f:
                if filter in line:
                    with open(error_file ,'w') as s:
                        yaml.dump({'error_msg': line},s)
                    s.close()
                    L.error('found log_filter %s!!!' % filter)
        f.close()
        return error_file
            # with open(error_file, 'w') as s:
            #     yaml.dump({'error_msg':'True'},s)
            # s.close()
            # return error_file
    def get_log_filter(self):
        with open(self.case_path) as f:
            cases = yaml.load(f)
            f.close()
        filter=''
        for case in cases:
            for action in case.keys():
                if action == 'log_filter':
                    filter = case[action]
        if filter:
            return self.analysis(filter)
        else:
            return
