import ConfigParser
import os
import sys
class configIni():
    def __init__(self):
        self.current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
       # self.path = self.current_path + '\\data\\test_info.ini'
        self.path = 'E:\\test\\data\\test_info.ini'
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
    def get_ini(self,title,value):
        return self.cf.get(title, value)
    def set_ini(self,title,value,text):
        self.cf.set(title,value,text)
        return self.cf.write(open(self.path, 'wb'))