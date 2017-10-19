# -*- coding:utf-8 -*-
import os
import yaml
class generatereport():
    def __init__(self,result_path):
        self.result_path = result_path
    def get_status(self,result,extension_name):
        file_dict = {}
        for parent,dirnames,filenames in os.walk(result):
            for filename in filenames:
                if 'filter' not in filename:
                    if filename.endswith(extension_name):
                        path = os.path.join(parent,filename)
                        file_dict[filename] = path
        return file_dict
    def open_yaml(self,path):
        if path is None:
            return None
        else:
            with open(path) as f:
                y = yaml.load(f)
            f.close()
            return y['error_msg']
    def confirm_file(self,file):
        if os.path.exists(file):
            return file
        else:
            return None
    def status(self):
        cases = self.get_status(self.result_path,'.yaml').values()
        passed = 0
        failed = 0
        for i in cases:
            if isinstance(self.open_yaml(i),bool):
                passed +=1
            else:
                failed +=1
        return len(cases), passed, failed

    def main(self):
        import getHtml
        result = self.get_status(self.result_path,'.yaml')
        lst = []
        for case_name, confirm_status in result.items():
            if not case_name.startswith('log'):
                case_name = str(case_name).split('.')[0]
                case_result = self.open_yaml(confirm_status)
                case_img = self.confirm_file(str(confirm_status).replace('status','img').replace('yaml','png'))
                case_log = self.confirm_file(str(confirm_status).replace('status', 'log').replace('yaml', 'log'))
                lst.append(
                    getHtml.get_tr(case_name,case_result,case_img,case_log)
                )
        getHtml.getHtml(''.join(lst),
                        self.status(),
                        self.result_path
                        )