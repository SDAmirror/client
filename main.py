from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial




class AppWindow(QWidget):
    # signals
    # switcTabSygnal = sts()
    def __init__(self):
        super(AppWindow, self).__init__()
        self.layout = QGridLayout()
        self.TAB = QPushButton("Send")
        self.layout.addWidget(self.TAB,0,0,1,1)
        # conf = configparser.ConfigParser()
        # conf.read('settings/auth.ini')
        # if bool(conf['AUTHDATA']['authenticated']):
        #     # window.setLayout(window.authTab.layout)
        #     pass

        self.username = ""
        self.socket = None
        self.cryptor = None
        self.message_sender = None
        self.message_receiver = None
        self.senders = []
        self.counter = 0
        self.newmessages = {}
        self.mbox = []
        self.tempNewChats = {}
        # self.switcTabSygnal.switcTabSygnal.connect(self.switchTab)
        # self.runServer()
        self.sbut = QPushButton('sew')
        self.sbut.clicked.connect(self.switchTab)
        self.layout.addWidget(self.sbut)
        self.setLayout(self.layout)




    def switchTab(self):
        mv = QTextEdit("jw")

        self.layout.removeWidget(self.TAB)
        self.TAB.deleteLater()


        self.TAB = None
        self.TAB = mv
        self.layout.addWidget(self.TAB,0,0,1,1)


        # self.TAB.username = self.username
        # self.TAB.socket = self.socket
        # self.TAB.cryptor = self.cryptor
        # self.TAB.message_sender = self.message_sender
        # self.TAB.message_receiver = self.message_receiver
        # self.TAB.listenPool()

        # print(f'tab changed tp {type(self.TAB)}')

if __name__ == "__main__":
    RHOST = "192.168.1.122"
    RHOST = "localhost"
    app = QApplication([])
    window = AppWindow()

    # window.runServer()
    window.show()
    app.exec_()
    # window.socket.close()