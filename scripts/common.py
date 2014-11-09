import os

class env_info():
    def __init__(self):
        self.brPath = os.getcwd()
	self.packagePath = self.brPath + '/../../package/'
        self.pkgmodPath = self.brPath + '/../pkgmods/'
	self.configsPath = self.brPath + '/../configs/'
