import os
import codecs
import configparser

class ReadConfig:
    def __init__(self,configPath):
        self.configPath=configPath

        #fd = open(self.configPath)
        fd = open(self.configPath, encoding='utf-8')
        data = fd.read()
        
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        #self.cf.read(self.configPath)
        self.cf.read(self.configPath,encoding='utf-8')

    def get_SeymourExcel(self,name):
        value = self.cf.get("SeymourExcel", name)
        return value