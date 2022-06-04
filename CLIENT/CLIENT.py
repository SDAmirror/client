import configparser
import datetime
import math
import socket
import ssl
import json
import message_processor
from DBClients.fakeDB import DB,MessageModel
from  MessageCtryptor import RSACryptor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
import uuid
import traceback, sys
from authwindow import *



db = DB()
conu = 0
RHOST="localhost"
RPORT=4430

edits = []

class GeneralSygnals(QObject):
    openChat = pyqtSignal()

class WorkerSignals(QObject):

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    newChat = pyqtSignal(str)
    newMessage = pyqtSignal(str,str)
    listFriends = pyqtSignal(dict)

class Worker(QRunnable):


    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['newChat'] = self.signals.newChat
        self.kwargs['newMessage']= self.signals.newMessage
        self.kwargs['listFriends']= self.signals.listFriends


    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class MessageBox(QWidget):
    def __init__(self,username="default",message="default"):
        super().__init__()

        self.parent = None
        self.genSygnal = GeneralSygnals()
        self.username = username
        self.box = QGridLayout()
        self.userLabel = QLineEdit(username)
        self.userLabel.setReadOnly(True)

        self.userLabel.setStyleSheet("""
        .QLineEdit {
            background: green;
            border-radius: 10px;
            color: red;
        }
        """)

        self.messsageLabel = QLineEdit(message)
        self.messsageLabel.setReadOnly(True)
        self.messsageLabel.setStyleSheet("""
        .QLineEdit {
            background: green;
            border-radius: 10px;
            color: red;
        }
        """)

        self.box.addWidget(self.userLabel,0,0,3,1)
        self.box.addWidget(self.messsageLabel,3,0,3,10)
        self.setLayout(self.box)
        for w in self.findChildren(QWidget) + [self]:
            w.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() & Qt.LeftButton:
                self.parent.openChat(self.username)
        return super(MessageBox, self).eventFilter(obj, event)
    def setMessage(self,message):
        self.messsageLabel.setText(message[:20]+"...")


class scroller(QWidget):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        self.scrollArea = QScrollArea()
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.widget.setLayout(self.layout)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)

        self.scrollArea.setWidget(self.widget)
        self.vout = QVBoxLayout()
        self.vout.addWidget(self.scrollArea)
        self.setLayout(self.vout)

class ChatList(scroller):
    def __init__(self):
        super().__init__()
        self.parent = None
        self.chat_list = {}
        self.counter = 0
        self.setStyleSheet("""
            .ChatList {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border-radius: 6px;
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                font-size: 14px;
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
            }
        """)
        # self.allChats()

    def addChat(self,messagebox):

        self.chat_list[messagebox.username]=messagebox
        messagebox.parent = self.parent
        messagebox.setStyleSheet("""
        .MessageBox {
            background: orange;
            border-radius: 10px;
            color: red;
        }
        """)
        self.layout.insertWidget(self.counter,messagebox,Qt.AlignCenter)
        self.counter += 1


    def allChats(self):
        chats = db.chats
        userlist = list(chats.keys())
        self.counter = len(userlist)
        for u in userlist:
            if len(chats[u]["messages"]) != 0:
                mb = MessageBox(u,json.dumps(chats[u]["messages"][-1])[:20]+"...")
            else:
                mb = MessageBox(u,'')
            mb.parent = self.parent
            self.layout.addWidget(mb)
            self.chat_list[u] = mb

class searchUserItem(QWidget):
    def __init__(self,username,firstname,lastname,parent):
        super(searchUserItem, self).__init__()
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

        self.parent = parent
        self.box = QGridLayout()
        self.userLabel = QLineEdit(self.username)
        self.userLabel.setReadOnly(True)
        self.userLabel.setStyleSheet("""
                .QLineEdit {
                    background: yellow;
                    border-radius: 10px;
                    color: red;
                }
                """)

        self.nameLabel = QLineEdit(self.firstname+' '+self.lastname)
        self.nameLabel.setReadOnly(True)
        self.nameLabel.setStyleSheet("""
                .QLineEdit {
                    background: yellow;
                    border-radius: 10px;
                    color: red;
                }
                """)

        self.box.addWidget(self.userLabel, 0, 0, 3, 1)
        self.box.addWidget(self.nameLabel, 3, 0, 3, 10)
        self.setLayout(self.box)

        for w in self.findChildren(QWidget) + [self]:
            w.installEventFilter(self)

    # def mousePressEvent(self, searchUserItem):
    #     print(self.username,self.lastname)
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() & Qt.LeftButton:
                db.addChat(self.username)
                db.updateUserInfo(self.username,{'firstname':self.firstname,'lastname':self.lastname})
                self.parent.senders.append(self.username)

                f = MessageBox(self.username,"")
                f.parent = self.parent

                self.parent.sideBar.chatBar.chat_list[self.username] = f
                self.parent.sideBar.chatBar.layout.addWidget(f)
                self.parent.openChat(self.username)
                self.parent.sideBar.userSearch.closeList()

            if event.buttons() & Qt.RightButton:
                print(obj, "global pos:", event.globalPos(),
                      "local pos", event.pos(),
                      "position with respect to self",
                      self.mapFromGlobal(obj.mapToGlobal(event.pos())))

        return super(searchUserItem, self).eventFilter(obj, event)

class userSearchList(scroller):
    def __init__(self,parent):
        super(userSearchList, self).__init__()
        self.parent = parent
        self.localDBUsers = []
        self.remoteDBUsers = []

class SearchForUser(QWidget):
    resized = pyqtSignal()
    textEnter = pyqtSignal()
    def __init__(self):

        super(SearchForUser, self).__init__()
        self.parent = None
        self.layout = QGridLayout()
        self.layout.setColumnStretch(1, 2)

        self.sendButton = QPushButton("SEARCH")
        self.sendButton.setStyleSheet("""
            .QPushButton {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border-radius: 6px;
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                font-size: 14px;
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
            }
        """)
        self.layout.addWidget(self.sendButton, 0, 5, 2, 2)
        self.searchinput = QLineEdit()
        self.searchinput.setStyleSheet("""
            .QLineEdit {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border-radius: 6px;
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                font-size: 14px;
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
                
            }
        """)
        self.layout.addWidget(self.searchinput, 0, 0, 2, 5)
        self.setLayout(self.layout)
        self.sendButton.clicked.connect(self.listUsers)
        self.userlist = None
        self.active = False

    def listUsers(self):
        if self.active:
            self.closeList()
        else:
            self.active = True

            userpattern = self.searchinput.text()
            print(userpattern)
            if self.userlist != None or isinstance(self.userlist,userSearchList):
                self.parent.sideBar.layout.removeWidget(self.userlist)
                self.userlist.deleteLater()
                self.userlist = None
            self.userlist = userSearchList(self.parent)
            # self.userlist.closeb.clicked.connect(self.closeList)
            self.parent.sideBar.layout.addWidget(self.userlist, 1, 0, 8, 3)
            ulistlocal = db.getChatByUserPattern(userpattern)
            for u in ulistlocal:
                si = searchUserItem(u['username'],u['firstname'],u['lastname'],self.parent)

                self.userlist.layout.addWidget(si)

            self.parent.add_friend(str(userpattern))

    def closeList(self):
        self.active = False
        self.parent.sideBar.layout.removeWidget(self.userlist)
        self.userlist.deleteLater()
        self.userlist = None



    # def resizeEvent(self, event):
    #     self.resized.emit()
    #     return super(SearchForUser,self).resizeEvent(event)
    # def adj(self):
    # self.input.setFixedHeight(math.ceil(self.input.document().size().height()) + math.ceil(self.input.contentsMargins().top() * 2))
    # self.m2.setFixedHeight(math.ceil(self.input.document().size().height()) + math.ceil(self.input.contentsMargins().top() * 2))
    # self.input.setFixedWidth(math.ceil(self.input.document().size().width()) + math.ceil(self.input.contentsMargins().top() * 2))

class SideBar(QWidget):

    def __init__(self,parent):
        super(SideBar, self).__init__()
        self.parent = parent
        self.layout = QGridLayout()

        self.userSearch = SearchForUser()
        self.chatBar = ChatList()
        self.chatBar.layout.setSpacing(0)
        self.chatBar.layout.setContentsMargins(0, 0, 0, 0)
        self.userSearch.parent = parent
        self.chatBar.parent = parent
        self.layout.addWidget(self.userSearch,0,0,1,3)
        self.layout.addWidget(self.chatBar, 1, 0, 8, 3)
        self.layout.setRowStretch(1,8)
        self.userSearch.setStyleSheet("""
            .SearchForUser {
                border: 20px solid black;
                border-radius: 10px;
                background-color: rgb(255, 255, 255);
            }
        """)
        self.setStyleSheet("""
            SideBar {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border-radius: 6px;
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                font-size: 14px;
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
            }
        """)
        self.setLayout(self.layout)

class MessageItem(QWidget):
    resized = pyqtSignal()

    def __init__(self,message):
        super(MessageItem, self).__init__()
        self.message = message
        # self.layout = QVBoxLayout()
        self.layout = QGridLayout()
        self.content = QTextEdit(message.content)
        self.content.append(message.send_date+" "+message.send_time)
        self.content.setReadOnly(True)
        self.content.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content.setSizePolicy(QSizePolicy.Expanding, 0)

        self.content.setAttribute(103)
        self.content.setStyleSheet("""
            .QTextEdit {
            background: rgb(245, 222, 179);
            border-radius: 15px
            }
        """)
        self.layout.addWidget(self.content)

        self.date = message.send_date
        self.time = message.send_time
        self.setLayout(self.layout)
        self.resized.connect(self.adj)

    def adjHeight(self):
        self.content.setFixedHeight(math.ceil(self.content.document().size().height()) + math.ceil(self.content.contentsMargins().top() * 2))
    def resizeEvent(self, event):
        self.resized.emit()
        return super(MessageItem, self).resizeEvent(event)

    #resize message items
    def adj(self):
        # self.dateWidget.setFixedHeight(math.ceil(self.dateWidget.document().size().height()) + math.ceil(self.dateWidget.contentsMargins().top() * 2))
        self.content.setFixedHeight(math.ceil(self.content.document().size().height()) + math.ceil(self.content.contentsMargins().top() * 2))

class MessagesArea(scroller):
    def __init__(self,username):
        super(MessagesArea, self).__init__()

        self.parent = None
        self.messages = []
        self.username = username
        # self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().height())
        self.loadMessage(username)
        self.printMessages()
        # self.setAutoFillBackground(True)
    def printMessages(self):
        for m in range(len(self.messages)):
            self.layout.insertWidget(m+1, self.messages[m])
    def loadMessage(self,username):
        chat = db.getChat(username)
        for i in range(len(chat.messages)):
            self.messages.append(MessageItem(chat.messages[i]))

class MessageInputArea(QWidget):
    resized = pyqtSignal()
    textEnter =  pyqtSignal()

    def __init__(self):

        super(MessageInputArea, self).__init__()

        self.parent = None
        self.layout = QGridLayout()
        self.layout.setColumnStretch(1,2)
        self.sendButton = QPushButton("send")
        self.sendButton.setStyleSheet("""
            .QPushButton {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border-radius: 6px;
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                font-size: 14px;
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
                height: 28px;
            }

        """)

        self.layout.addWidget(self.sendButton,0,5,2,2)
        self.input = QTextEdit()
        self.input.setStyleSheet("""
            .QTextEdit {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border-radius: 6px;
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                font-size: 14px;
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
                height: 100%;
            }

        """)
        # self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.input.setFixedHeight(math.ceil(50))

        self.layout.addWidget(self.input,0,0,2,5)
        self.setLayout(self.layout)
        self.resized.connect(self.adj)
        self.textEnter.connect(self.adj)
        self.input.textChanged.connect(self.adj)
        self.setStyleSheet("""
            .QWidget{
                background: #8babd8;
                border: solid 2px red;
            }
        """)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MessageInputArea,self).resizeEvent(event)
    def adj(self):
        self.input.setFixedHeight(math.ceil(self.input.document().size().height()) + math.ceil(self.input.contentsMargins().top() * 2))
        # self.input.setFixedWidth(math.ceil(self.input.document().size().width()) + math.ceil(self.input.contentsMargins().top() * 2))

class UserBar(QWidget):
    def __init__(self,user):
        super(UserBar, self).__init__()
        self.parent = None
        self.username = user['username']
        self.firstname = user['firstname']
        self.lastname = user['lastname']
        self.mcount = user['messagecount']
        self.layout = QGridLayout()
        # self.layout.setSpacing(0)
        # self.layout.setContentsMargins(0,0,0,0)
        self.usernameLabel = QLabel("{}".format("{} {}: {}  ({})".format(self.firstname, self.lastname, self.username, self.mcount)))
        self.firstnameLabel = QLabel(self.firstname)
        self.lastnameLabel = QLabel(self.lastname)
        self.usernameLabel.setStyleSheet("""
            .QLabel {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border-radius: 6px;
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                font-size: 14px;
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
            }
        """)
        self.firstnameLabel.setStyleSheet("""
            .QLabel {
                background: black;
                color: white;
                border-radius: 10px;
                font-size: 20px;
                height: 25px;
      
            }
        """)
        self.lastnameLabel.setStyleSheet("""
            .QLabel {
                background: black;
                color: white;
                border-radius: 10px;
                font-size: 20px;
                height: 100%; 
            }
        """)
        self.layout.addWidget(self.usernameLabel,0,0,1,1)
        # self.layout.addWidget(self.usernameLabel,0,0,2,2)
        # self.layout.addWidget(self.firstnameLabel,0,2,2,2)
        # self.layout.addWidget(self.lastnameLabel,0,4,2,2)
        self.setLayout(self.layout)

class ChatWindow(QWidget):
    def __init__(self,username):
        super(ChatWindow, self).__init__()
        self.parent = None
        self.username = username
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        if username != None:
            self.userdata = db.getUserInfo(self.username)
            self.userBar = UserBar({'username':username,'firstname':self.userdata.firstname, 'lastname':self.userdata.lastname ,'messagecount':self.userdata.messagecount})
            # self.userBar.setAutoFillBackground(True)
            self.userBar.setStyleSheet("""
            .QWidget {
                background: black;
                border: none;
                height: 100%;
            }
        """)

            self.layout.addWidget(self.userBar)
        self.messagesArea = MessagesArea(username)
        self.messagesArea.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.messagesArea.setStyleSheet("""
            .QWidget {
                background: #0090ab;
                border: none;
                height: 100%;
                widht: 100%;
            
            }
            .QScrollBar:vertical {
                border: 2px solid grey;
                background: #32CC99;
                height: 15px;
                padding: 0 0 0 0;
                border-spacing: 0px 0px;
                margin: 0px;
            }
        """)
        self.layout.addWidget(self.messagesArea)
        self.inputArea = MessageInputArea()


        # self.inputArea.setStyleSheet("""
        #     .QWidget{
        #         background: #8babd8;
        #         border: solid 2px red;
        #     }
        # """)
        if username != None:

            self.layout.addWidget(self.inputArea)
        self.setLayout(self.layout)

class AuthBar(QWidget):
    def __init__(self,parent):
        super(AuthBar, self).__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.layout.setDirection(QBoxLayout.Up)
        self.logoutButton = QPushButton("LOGOUT")
        # self.logoutButton.setStyleSheet("height: 100%;")
        self.layout.addWidget(self.logoutButton)
        url = 'settings/auth.ini'
        conf = configparser.ConfigParser()
        conf.read(url)

        self.username = conf['AUTHDATA']['username']
        self.firstname = conf['AUTHDATA']['firstname']
        self.lastname = conf['AUTHDATA']['lastname']
        self.email = conf['AUTHDATA']['email']
        self.firstnameLabel = QLabel(self.firstname)
        self.lastnameLabel = QLabel(self.lastname)
        self.emailLabel = QLabel(self.email)
        self.usernameLabel = QLabel(self.username)
        # self.usernameLabel.setStyleSheet("height: 100%,background: white")
        self.layout.addWidget(self.emailLabel)
        self.layout.addWidget(self.lastnameLabel)
        self.layout.addWidget(self.firstnameLabel)
        self.layout.addWidget(self.usernameLabel)
        self.setLayout(self.layout)
        self.t = True
        self.hide()

class MainWindow(QWidget):

    def __init__(self,username,messagesender,messagereceiver,cryptor,socket, parent,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.tabName = 'mainWindow'
        self.parent = parent
        self.counter = 0
        self.dialogs = {}
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.setStyleSheet("""
            .MainWindow {
                background: #0090ab;
            }
        """)
        self.sideBar = SideBar(self)
        self.sideBar.layout.setSpacing(0)
        self.sideBar.layout.setContentsMargins(0,0,0,0)
        self.sideBar.setStyleSheet("""
        .QWidget {
            background: white;
            border: none;

        }
        .QScrollBar:vertical {
                border: 2px solid grey;
                background: #32CC99;
                height: 15px;
                margin: 0px 0px 0px 0px;
            }
        """)
        self.sideBar.chatBar.allChats()
        self.l3 = ChatWindow(None)
        self.l3.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # self.l3.setStyleSheet("""
        #     .QWidget {
        #         background: white;
        #         border: none;
        #         hight: 100%;
        #         widht: 100%;
        #
        #     }
        # """)

        self.userBarButton = QPushButton("X")
        self.userBarButton.clicked.connect(self.openCloseWidgetBar)
        self.userBarButton.setStyleSheet("""
            .QPushButton {
                appearance: none;
                background-color: #FAFBFC;
                border: 1px solid rgba(27, 31, 35, 0.15);
                border: #2EFF2E solid 1px;
                box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                box-sizing: border-box;
                color: #24292E;
                cursor: pointer;
                display: inline-block;
                font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
              
                font-weight: 500;
                line-height: 20px;
                list-style: none;
                padding: 6px 16px;
                position: relative;
                transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                vertical-align: middle;
                white-space: nowrap;
                word-wrap: break-word;
                height: 100%;
            }
        """)

        self.userBarButton.setMaximumWidth(40)
        self.userBarButton.setSizePolicy(0,QSizePolicy.Expanding)
        self.layout.addWidget(self.userBarButton,0,0,1,1)
        self.widgetBar = AuthBar(self)

        self.widgetBar.setStyleSheet("background: #6497b1;height: 100%")
        self.widgetBar.logoutButton.clicked.connect(self.logout)
        # self.widgetBar.setSizePolicy(0,0)
        self.widgetBar.setMaximumWidth(300)
        self.widgetStatus = False

        self.layout.addWidget(self.widgetBar, 0, 2, 1, 4)
        self.layout.addWidget(self.userBarButton, 0, 0, 1, 1)
        self.layout.addWidget(self.sideBar, 0, 2, 1, 4)
        self.layout.addWidget(self.l3, 0, 6, 1, 8)
        self.layout.setColumnStretch(6, 3)
        self.l3.inputArea.sendButton.clicked.connect(self.printer)
        self.setLayout(self.layout)
        self.username = username
        self.socket = socket
        self.cryptor = cryptor
        self.message_sender = messagesender
        self.message_receiver = messagereceiver
        self.senders = list(db.chats.keys())
        self.counter = 0
        self.newmessages = {}
        self.mbox = []
        self.tempNewChats = {}
        self.threadpool = QThreadPool()
        self.worker = None
        self.listenPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def openCloseWidgetBar(self):
        if self.widgetStatus:self.widgetBar.hide()
        else:
            self.widgetBar.show()
            self.widgetBar.activateWindow()
            self.widgetBar.raise_()
        self.widgetStatus = not self.widgetStatus
    def openChat(self,username):
        l3 = ChatWindow(username)
        l3.parent = self
        self.l3.deleteLater()

        self.l3.close()
        self.l3 = None
        self.l3 = l3
        self.l3.inputArea.sendButton.clicked.connect(self.printer)
        #
        self.layout.addWidget(self.l3, 0, 6, 1, 8)
        self.layout.setColumnStretch(6, 3)
    def listRemoteSearchUsers(self,users):
        for u in users['users']:
            si = searchUserItem(u['username'],u['firstname'],u['lastname'],self)
            self.sideBar.userSearch.userlist.layout.addWidget(si)
            self.sideBar.userSearch.userlist.remoteDBUsers.append(si)

    def addChat(self, user):


        f = MessageBox(f"{self.tempNewChats[user]['username']}", f"{json.dumps(self.tempNewChats[user]['message'])}")
        f.parent = self

        self.sideBar.chatBar.chat_list[user]=f
        self.sideBar.chatBar.layout.addWidget(f)

    def newMessage(self,username,message):
        if username in list(self.sideBar.chatBar.chat_list.keys()):
            jm = json.loads(str(message))
            if self.l3.username == username:

                mm = MessageModel(jm['message']['id'], jm['message']['content'], jm['message']['sender'],
                             jm['message']['receiver'], jm['message']['send_date'], jm['message']['send_time'],
                             jm['message']['sent'])
                mi = MessageItem(mm)
                self.l3.messagesArea.messages.append(mi)
                self.l3.messagesArea.layout.insertWidget(len(self.l3.messagesArea.messages),mi)
                # self.l3.messagesArea.layout.addWidget(mi)
                self.sideBar.chatBar.chat_list[username].setMessage(mm.content)

            self.sideBar.chatBar.chat_list[username].setMessage(jm['message']['content'])

    def sendMessage(self,username,message):
        print(message.__dict__)
        try:

            self.sideBar.chatBar.chat_list[username].setMessage(message.content)
            if self.l3.username == username and self.l3.username != self.username:
                db.newMessage(username, {
                    'url': 'message',
                    'message': {
                        'sender': self.username,
                        'receiver': message.receiver,
                        'sent': False,
                        'id': message.id,
                        'content': message.content,
                        'send_date': message.send_date,
                        'send_time': message.send_time
                    }
                })
                mi = MessageItem(message)
                if self.username == message.sender:
                    mi.setStyleSheet("background: #08F26E")
                self.l3.messagesArea.messages.append(mi)

                self.l3.messagesArea.layout.insertWidget(len(self.l3.messagesArea.messages), mi)

        except Exception as e:
            print(e)


        #add message to area

    def listen_for_messages(self, newChat,newMessage,listFriends):
        print("i am listening")
        global db
        message_receiver = self.message_receiver
        while True:
            # DB, UI, response.
            try:
                message = self.socket.recv(2048)
                message = message_receiver.recieve_message(1, message)

                try:
                    jm = json.loads(str(message))

                    if "url" in list(jm.keys()):
                        if jm["url"] == "status":
                            print(jm)
                        elif jm["url"] == "addfriendresponse":
                            print(jm)

                            listFriends.emit(jm)
                        elif jm["url"] == "message":

                            if jm['message']["sender"] == self.username:
                                chatUsername = jm['message']["receiver"]
                            elif jm['message']["sender"] == self.username and jm['message']["receiver"] == self.username:
                                chatUsername = self.username
                            else:
                                chatUsername = jm['message']["sender"]
                            print(chatUsername)
                            if chatUsername in self.senders:

                                db.newMessage(chatUsername, jm)
                                newMessage.emit(str(chatUsername),str(message))



                            else:
                                self.senders.append(chatUsername)
                                db.addChat(chatUsername)
                                db.newMessage(chatUsername, jm)

                                self.tempNewChats[chatUsername] = {"username": chatUsername, "message": jm}
                                # self.addChat(chatUsername)
                                newChat.emit(str(chatUsername))
                        elif jm['url'] == 'logout':
                            print(jm,'logout')
                            url = 'settings/auth.ini'
                            conf = configparser.ConfigParser()
                            conf.read(url)

                            conf['AUTHDATA']['username'] = ''
                            conf['AUTHDATA']['authenticated'] = ''
                            conf['AUTHDATA']['auth_token'] = ''
                            conf['AUTHDATA']['email'] = ''
                            conf['AUTHDATA']['firstname'] = ''
                            conf['AUTHDATA']['lastname'] = ''
                            with open(url, 'w') as cf:
                                conf.write(cf)
                            # m = self.socket.recv(2048)
                            # m = self.message_receiver.recieve_message(1, m)
                            # print(m, 'logout m')
                            break



                except Exception as e:
                    print(e)
                if not message:
                    print("closed")
                    break
                print(message)
                # self.l2.reader.append("\n" + str(message))
            except Exception as e:
                print(e)
                self.socket.close()
                break
        print('listening is end')

    def add_friend(self,userpattern):
        message_sender = self.message_sender
        message = {'url': 'addfriendrequest', 'userpattern':userpattern}
        self.socket.send(message_sender.send_message(1, json.dumps(message)))

    def printer(self):
        print("printer")
        message_sender = self.message_sender

        to_send = str(self.l3.inputArea.input.toPlainText())

        # database check if user exist
        # check keys
        # if keys ok:
        #   send message
        # else:
        #   renew keys
        if to_send == '':
            to_send = '1'
        if to_send.lower() == 'q':
            self.socket.close()

        username = str(self.l3.username)
        message = {'url':'message','reciever': username, 'body': to_send, 'send_date': str(datetime.date.today()),
                   'send_time': datetime.datetime.now().strftime("%H:%M:%S")}

        mm = MessageModel(str(uuid.uuid4()), to_send, self.username, username,message['send_date'], message['send_time'],False)
        self.sendMessage(username,mm)
        self.l3.inputArea.input.clear()
        self.socket.send(message_sender.send_message(1, json.dumps(message)))

    def logout(self):
        message_sender = self.message_sender

        to_send = str(self.l3.inputArea.input.toPlainText())

        if to_send == '':
            to_send = '1'
        if to_send.lower() == 'q':
            self.socket.close()


        message = {'url': 'logout'}

        self.socket.send(message_sender.send_message(1, json.dumps(message)))
        # self.threadpool.cancel(self.worker)
        # url = 'settings/auth.ini'
        # conf = configparser.ConfigParser()
        # conf.read(url)
        #
        # conf['AUTHDATA']['username'] = ''
        # conf['AUTHDATA']['authenticated'] = ''
        # conf['AUTHDATA']['auth_token'] = ''
        # with open(url, 'w') as cf:
        #     conf.write(cf)
        # m = self.socket.recv(2048)
        # m = self.message_receiver.recieve_message(1, m)
        # print(m,'logout m')
        #


    def print_output(self, s):
        print(s,'output')

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.parent.switchTab()
        # self.socket.close()
        # sys.exit()

    def listenPool(self):
        worker = Worker(self.listen_for_messages) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.newChat.connect(self.addChat)
        worker.signals.newMessage.connect(self.newMessage)
        worker.signals.listFriends.connect(self.listRemoteSearchUsers)
        self.worker = worker
        self.threadpool.start(worker)


class sts(QObject):
    switchTab = pyqtSignal()
    openCodeTab = pyqtSignal()
    loginError = pyqtSignal(dict)
class AuthSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    start = pyqtSignal(dict)
    opencodetab = pyqtSignal()
    loginError = pyqtSignal(dict)
    switchTab = pyqtSignal()
class AuthWorker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(AuthWorker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = AuthSignals()
        self.kwargs['opencodetab']  = self.signals.opencodetab
        self.kwargs['loginError']  = self.signals.loginError
        self.kwargs['switchTab']  = self.signals.switchTab



    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class AppWindow(QWidget):
    # signals
    signals = sts()
    def __init__(self):
        super(AppWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.TAB = AuthenticationTab(self)
        self.layout.addWidget(self.TAB)

        self.username = ""
        self.socket = None
        self.cryptor = None
        self.message_sender = None
        self.message_receiver = None

        self.signals.switchTab.connect(self.switchTab)
        self.signals.loginError.connect(self.TAB.reportError)
        self.signals.openCodeTab.connect(self.TAB.addCodeVerification)

        self.runServer()
        self.setLayout(self.layout)
        conf = configparser.ConfigParser()
        conf.read('settings/auth.ini')
        if bool(conf['AUTHDATA']['authenticated']):
            self.authenticateClient({
                "auth_check": 1,
                "url": "authentication",
                "authentification_token": conf['AUTHDATA']['auth_token'],
                "authorization_data": [conf['AUTHDATA']['username'], ''],
            })
        self.threadpool = QThreadPool()
        self.AuthHandlerSwitch = False
    def switchTab(self):
        if self.TAB.tabName =='authTab':
            mv = MainWindow(self.username,self.message_sender,self.message_receiver,self.cryptor,self.socket,self)
            self.layout.removeWidget(self.TAB)
            self.TAB.deleteLater()
            self.TAB.close()
            self.TAB = None
            self.TAB = mv
            self.layout.addWidget(self.TAB)
        else:
            mv = AuthenticationTab(self)
            self.layout.removeWidget(self.TAB)
            self.TAB.deleteLater()
            self.TAB.close()
            self.TAB = None
            self.TAB = mv
            self.layout.addWidget(self.TAB)
            self.signals.loginError.connect(self.TAB.reportError)
            self.signals.openCodeTab.connect(self.TAB.addCodeVerification)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def runServer(self):

        # url what fron auth tabs


        SERVER_HOST = RHOST

        SERVER_PORT = RPORT

        cryptor = RSACryptor(1)
        cryptor.generate_RSA_keys()
        self.cryptor = cryptor

        message_sender = message_processor.Message_Sender(cryptor)
        message_receiver = message_processor.Message_Recirver(cryptor)
        self.message_sender = message_sender
        self.message_receiver = message_receiver
        s = ssl.wrap_socket(socket.socket())
        s.connect((SERVER_HOST, SERVER_PORT))
        self.socket = s
        print("[+] Connected.")
        try:
            server_public_key = s.recv(2048).decode()
            cryptor.set_server_public_key(server_public_key)
        except ConnectionResetError as e:
            print("client disconnected", e)
            s.close()
        try:
            key = message_sender.send_message(1, cryptor.load_Public_key()['key'].save_pkcs1())
            s.send(key)
            print(self.socket)
        except ConnectionResetError as e:
            print("client disconnected",e)
            s.close()
        print("key excahnge cuccess")
        # socket is ready
        # here authentication
    def registrationHandler(self,opencodetab,loginError,switchTab):
        print("i am listening registrationHandler")
        global db
        message_receiver = self.message_receiver
        while self.AuthHandlerSwitch:
            # DB, UI, response.
            try:
                message = self.socket.recv(2048)
                message = message_receiver.recieve_message(1, message)

                try:
                    jm = json.loads(str(message))
                    if "auth_data_exchange" in jm.keys():
                        if jm["auth_data_exchange"]:
                            continue
                        else:
                            print("data not sent")

                    {
                        "50200": "status OK",
                        "50242": "verification code sent",
                        "50243": "verification code valid",
                        "50244": "registration success",
                        "50245": "authentication success",

                        "50441": "username taken",
                        "50442": "failure wrong email format",
                        "50443": "failure code validation",
                        "50444": "failure code receive",
                        "50445": "failure email",

                        "50541": "server error"
                    }
                    if "url" in list(jm.keys()):
                        if jm["url"] == "registration":
                            if not jm["auth_success"]:
                                if jm["statusCode"] == 50441:
                                    loginError.emit({"reason":jm["message"]})
                                elif jm["statusCode"] == 50442:
                                    loginError.emit({"reason":jm["message"]})
                                elif jm["statusCode"] == 50443:
                                    loginError.emit({"reason":jm["message"]})
                                elif jm["statusCode"] == 50444:
                                    loginError.emit({"reason":jm["message"]})
                                elif jm["statusCode"] == 50445:
                                    loginError.emit({"reason":jm["message"]})

                            else:
                                if jm["statusCode"] == 50242:
                                    loginError.emit({"reason": jm["message"]})
                                    opencodetab.emit()
                                elif jm["statusCode"] == 50245:
                                    conf = configparser.ConfigParser()
                                    conf.read('settings/auth.ini')
                                    conf['AUTHDATA']['authenticated'] = 'yes'
                                    conf['AUTHDATA']['auth_token'] = jm['AuthenticationUser']['authentication_token']
                                    conf['AUTHDATA']['username'] = jm['AuthenticationUser']['user']['username']
                                    conf['AUTHDATA']['email'] = jm['AuthenticationUser']['user']['email']
                                    conf['AUTHDATA']['firstname'] = jm['AuthenticationUser']['user']['first_name']
                                    conf['AUTHDATA']['lastname'] = jm['AuthenticationUser']['user']['last_name']
                                    with open('settings/auth.ini', 'w') as configfile:
                                        conf.write(configfile)
                                    self.AuthHandlerSwitch = False
                                    switchTab.emit()
                                    break
                                elif jm["statusCode"] == 50541:
                                    loginError.emit({"reason":jm["message"]})




                except Exception as e:
                    print(e)
                if not message:
                    print("closed")
                    break
                print(message)

            except Exception as e:
                print(e)

                break
        print('listening registrationHandler is end')

    def registerPool(self):
        worker = AuthWorker(self.registrationHandler)
        worker.signals.opencodetab.connect(self.TAB.addCodeVerification)
        worker.signals.loginError.connect(self.TAB.reportError)
        worker.signals.switchTab.connect(self.switchTab)

        self.threadpool.start(worker)

    def registerClientCode(self):
        message_sender = self.message_sender
        message_receiver = self.message_receiver
        while True:
            code = input('code')
            if code == "q": break
            self.socket.send(message_sender.send_message(1, code))
            print("sent")
            m = self.socket.recv(2048)
            m = message_receiver.recieve_message(1, m)
            print(m)

        print("sent")
        m = self.socket.recv(2048)
        m = message_receiver.recieve_message(1, m)

        print(m, 'recived')
        mess = json.loads(str(m))
        print(mess)
        # if mess['auth_success']:
        #     print(mess['AuthenticationUser'])
        #     self.signals.switchTab.emit()
        # else:
        #     print("failed", mess['reason'])
        #     self.signals.loginError.emit(mess)
        #     # raise KeyboardInterrupt
    def sendCode(self,code):
        message_sender = self.message_sender
        # message_receiver = self.message_receiver

        self.socket.send(message_sender.send_message(1, json.dumps({'code':code})))
        print("sent")
        # m = self.socket.recv(2048)
        # m = message_receiver.recieve_message(1, m)
        # try:
        #     m = json.loads(str(m))
        #     if m['url'] == 'registration':
        #         if 'auth_success' in m.keys():
        #             print(m)
        #             if m['auth_success']:
        #                 print(m['AuthenticationUser'])
        #                 conf = configparser.ConfigParser()
        #                 conf.read('settings/auth.ini')
        #                 conf['AUTHDATA']['authenticated'] = 'yes'
        #                 conf['AUTHDATA']['auth_token'] = m['AuthenticationUser']['authentication_token']
        #                 conf['AUTHDATA']['username'] = m['AuthenticationUser']['user']['username']
        #                 conf['AUTHDATA']['email'] = m['AuthenticationUser']['user']['email']
        #                 conf['AUTHDATA']['firstname'] = m['AuthenticationUser']['user']['first_name']
        #                 conf['AUTHDATA']['lastname'] = m['AuthenticationUser']['user']['last_name']
        #                 with open('settings/auth.ini', 'w') as configfile:
        #                     conf.write(configfile)
        #                 self.switchTab()
        #             else:
        #                 if 'AuthenticationUser' in m.keys():
        #
        #                     print("failed, but registred")
        #                 else:
        #                     print(m)
        #                 # self.signals.loginError.emit(m)
        #
        #         if not m['auth_data_exchange']:
        #             print(m['error'])
        #
        # except json.JSONDecodeError as e:
        #     print(e)
        # except Exception as e:
        #     print(e,1350)
        # print(m)
    def registerClient(self,data):
        self.username = data['registration_data']['username']
        message_sender = self.message_sender
        message_receiver = self.message_receiver
        self.socket.send(message_sender.send_message(1, json.dumps(data)))
        # cou = 3
        # m = self.socket.recv()
        # status = json.loads(message_receiver.recieve_message(1, m))
        # print(status)
        # if status['auth_data_exchange']:
        #     print('data sent sucsessfully')
        #
        # else:
        #     cou -= 1
        #     if status['error'] == 50400:
        #         print('data sent unsuccessful')
        #
        # print("sent")
        # self.TAB.addCodeVerification()

        # while True:
        #     code = input('code')
        #     if code == "q":
        #         break
        #     self.socket.send(message_sender.send_message(1, code))
        #     print("sent")
        #     m = self.socket.recv(2048)
        #     m = message_receiver.recieve_message(1, m)
        #     print(m)
        #
        # m = self.socket.recv(2048)
        # m = message_receiver.recieve_message(1, m)
        #
        # print(m, 'recived')
        # mess = json.loads(str(m))
        # print(mess)
        # if mess['auth_success']:
        #     print(mess['AuthenticationUser'])
        #     self.signals.switchTab.emit()
        # else:
        #     print("failed", mess['reason'])
        #     self.signals.loginError.emit(mess)
        # self.TAB.addCodeVerification()
    def authenticateClient(self, data):
        # data = {
        #     "auth_check": 1,
        #     "url": "authorization",
        #     "authorization_data":['user1', "password1"],
        # }
        self.username = data['authorization_data'][0]
        message_sender = self.message_sender
        message_receiver = self.message_receiver
        cou = 3

        self.socket.send(message_sender.send_message(1, json.dumps(data)))
        m = self.socket.recv()
        status = json.loads(message_receiver.recieve_message(1, m))
        if status['auth_data_exchange']:
            print("sent")
            m = self.socket.recv(2048)
            m = message_receiver.recieve_message(1, m)

            print(m, 'recived')
            mess = json.loads(str(m))
            print(mess)
            if mess['auth_success']:
                print(mess['AuthenticationUser'])
                conf = configparser.ConfigParser()
                conf.read('settings/auth.ini')
                conf['AUTHDATA']['authenticated'] = 'yes'
                conf['AUTHDATA']['auth_token'] = mess['AuthenticationUser']['authentication_token']
                conf['AUTHDATA']['username'] = mess['AuthenticationUser']['user']['username']
                conf['AUTHDATA']['email'] = mess['AuthenticationUser']['user']['email']
                conf['AUTHDATA']['firstname'] = mess['AuthenticationUser']['user']['first_name']
                conf['AUTHDATA']['lastname'] = mess['AuthenticationUser']['user']['last_name']
                with open('settings/auth.ini', 'w') as configfile:
                    conf.write(configfile)

                self.switchTab()
            else:
                print("failed", mess['reason'])
                self.signals.loginError.emit(mess)
                # raise KeyboardInterrupt

        else:
            cou -= 1
            if status['error'] == 50400:
                print('data sent unsuccessful')

        # print("sent")
        # m = self.socket.recv(2048)
        # m = message_receiver.recieve_message(1, m)
        #
        # print(m, 'recived')
        # mess = json.loads(str(m))
        # print(mess)
        # if mess['auth_success']:
        #     print(mess['AuthenticationUser'])
        #     conf = configparser.ConfigParser()
        #     conf.read('settings/auth.ini')
        #     conf['AUTHDATA']['authenticated'] = 'yes'
        #     conf['AUTHDATA']['auth_token'] = mess['AuthenticationUser']['authentication_token']
        #     conf['AUTHDATA']['username'] = mess['AuthenticationUser']['user']['username']
        #     with open('settings/auth.ini', 'w') as configfile:
        #         conf.write(configfile)
        #
        #
        #     self.switchTab()
        # else:
        #     print("failed", mess['reason'])
        #     self.signals.loginError.emit(mess)
        #     # raise KeyboardInterrupt

if __name__ == "__main__":
    RHOST = "192.168.1.122"
    RHOST = "localhost"
    app = QApplication([])
    window = AppWindow()

    # window.runServer()
    window.show()
    app.exec_()
    window.socket.close()
    sys.exit()


# if __name__ == "__main__":
#     app = QApplication([])
#
#     # window = AuthBar("usernma",'fname','lname','e@mal.ru',None)
#     window = MainWindow('username',None,None,None,None,None)
#
#     window.show()
#     app.exec_()