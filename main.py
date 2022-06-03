from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial



import configparser

url = 'CLIENT/settings/auth.ini'
conf = configparser.ConfigParser()
conf.read(url)
print(bool(conf['AUTHDATA']['username']))
conf['AUTHDATA']['username'] = 'user1'
with open(url, 'w') as cf:
    conf.write(cf)
