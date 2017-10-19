# -*- coding: utf-8 -*-
from util import configIni
import os
def get_case():
    ini = configIni()
    case_path = ini.get_ini('test_case','test_case')
    case_dict = {}
    for parent, dirnames, filenames in os.walk(case_path):
        for filename in filenames:
            if 'filter' not in filename:
                if filename.endswith('.yaml'):
                    path = os.path.join(parent,filename)
                    case_dict[filename] = path
    return case_dict
if __name__ =='__main__':
    get_case()