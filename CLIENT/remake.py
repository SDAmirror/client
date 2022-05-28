import configparser
import datetime
import math
import socket
import ssl
import json
import message_processor
from authwindow import *
from DBClients.fakeDB import DB,MessageModel
from  MessageCtryptor import RSACryptor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
import uuid
import time
import traceback, sys
from authwindow import *

db = DB()
_t_Listenner = None
conu = 0
RHOST="localhost"
RPORT=4430





class GeneralSygnals(QObject):
    openChat = pyqtSignal()

class WorkerSignals(QObject):

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    newChat = pyqtSignal(str)
    newMessage = pyqtSignal(str,str)
    listFriends = pyqtSignal(dict)


class AuthSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    start = pyqtSignal(dict)
class AuthWorker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(AuthWorker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = AuthSignals()
        self.kwargs['start']  = self.signals.start

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
        self.kwargs['start']  = self.signals.start

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


edits = []
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
    #
    # def mousePressEvent(self, QMouseEvent):
    #     # print("self.parent.openChat(self.username)",self.parent)
    #     self.parent.openChat(self.username)

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
        for u in userlist:
            if len(chats[u]["messages"]) != 0:
                mb = MessageBox(u,json.dumps(chats[u]["messages"][-1])[:20]+"...")
            else:
                mb = MessageBox(u,u)
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
        self.layout.addWidget(self.sendButton, 0, 5, 2, 2)
        self.searchinput = QLineEdit()
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
            print(self.parent)
            userpattern = self.searchinput.text()
            print(userpattern)
            if self.userlist != None or isinstance(self.userlist,userSearchList):
                self.parent.sideBar.layout.removeWidget(self.userlist)
                self.userlist.deleteLater()
                self.userlist = None
            self.userlist = userSearchList(self.parent)
            # self.userlist.closeb.clicked.connect(self.closeList)
            self.parent.sideBar.layout.addWidget(self.userlist, 2, 0, 8, 3)
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
        self.userSearch.parent = parent
        self.chatBar.parent = parent
        self.layout.addWidget(self.userSearch,0,0,2,3)
        self.layout.addWidget(self.chatBar, 2, 0, 8, 3)
        self.layout.setRowStretch(2,8)

        self.userSearch.setStyleSheet("""
            .SearchForUser {
                border: 20px solid black;
                border-radius: 10px;
                background-color: rgb(255, 255, 255);
            }
        """)

        self.setLayout(self.layout)




class InputWidgets(QWidget):
    def  __init__(self):
        super().__init__()
        self.parent = None
        self.layout = QGridLayout()
        self.reader = QTextEdit("READER")
        self.layout.addWidget(self.reader, 0, 0, 4, 3)
        self.messageI = QTextEdit("MESSAGE")
        self.layout.addWidget(self.messageI, 4, 0, 4, 3)
        self.usernameI = QTextEdit("USER")
        self.layout.addWidget(self.usernameI, 8, 0, 4, 3)
        self.b1 = QPushButton('Top')
        self.b1.setStyleSheet("""
        .QPushButton{
            background: red;
            height: 100%;
            border-radius: 10px;
            border: solid green 2px;
        }
        """)
        self.layout.addWidget(self.b1, 12, 0, 3, 3)
    # self.b1.clicked.connect(self.printer)
        # self.b1.clicked.connect(self.execute)
        self.setLayout(self.layout)


    def execute(self):

        self.reader.append("\n"+str(self.usernameI.toPlainText()))


class MessageItem(QWidget):
    resized = pyqtSignal()

    def __init__(self,message):
        super(MessageItem, self).__init__()
        self.message = message
        self.layout = QVBoxLayout()
        self.content = QTextEdit(message.content)
        self.content.append(message.send_date+" "+message.send_time)
        # self.adj()
        self.content.setReadOnly(True)
        self.content.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.content.setAttribute(103)
        self.content.setStyleSheet("""
            .QTextEdit {
            background: rgb(245, 222, 179);
            border-radius: 15px
            }
        """)
        self.content.setFixedHeight(math.ceil(self.content.document().size().height()) + math.ceil(self.content.contentsMargins().top() * 2))
        self.layout.addWidget(self.content)
        self.date = message.send_date
        self.time = message.send_time
        self.setLayout(self.layout)
        self.resized.connect(self.adj)


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
    def printMessages(self):
        for m in range(len(self.messages)):
            self.layout.insertWidget(m, self.messages[m])
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
        self.layout.addWidget(self.sendButton,0,5,2,2)
        self.input = QTextEdit()
        # self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.input.setFixedHeight(math.ceil(50))

        self.layout.addWidget(self.input,0,0,2,5)
        self.setLayout(self.layout)
        self.resized.connect(self.adj)
        self.textEnter.connect(self.adj)
        self.input.textChanged.connect(self.adj)

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
        self.layout = QGridLayout()
        self.usernameLabel = QLabel('username')
        self.firstnameLabel = QLabel('firstname')
        self.lastnameLabel = QLabel('lastname')
        self.usernameLabel.setStyleSheet("""
            .QLabel {
                background: black;
                color: white;
                border-radius: 10px;
            }
        """)
        self.firstnameLabel.setStyleSheet("""
            .QLabel {
                background: black;
                color: white;
                border-radius: 10px;
            }
        """)
        self.lastnameLabel.setStyleSheet("""
            .QLabel {
                background: black;
                color: white;
                border-radius: 10px;
            }
        """)
        self.layout.addWidget(self.usernameLabel,0,0,2,2)
        self.layout.addWidget(self.firstnameLabel,0,2,2,2)
        self.layout.addWidget(self.lastnameLabel,0,4,2,2)
        self.setLayout(self.layout)

class ChatWindow(QWidget):
    def __init__(self,username):
        super(ChatWindow, self).__init__()
        self.parent = None
        self.username = username
        self.layout = QGridLayout()
        self.layout.addWidget(UserBar({'username':'user1','firstname':'firstname', 'lastname':'lastname' }))
        self.messagesArea = MessagesArea(username)
        self.layout.addWidget(self.messagesArea)
        self.inputArea = MessageInputArea()
        self.layout.addWidget(self.inputArea)
        self.setLayout(self.layout)

class MainWindow(QWidget):

    def __init__(self,parent, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.parent = parent
        self.counter = 0
        self.dialogs = {}

        self.layout = QGridLayout()
        self.sideBar = SideBar(self)
        self.sideBar.chatBar.allChats()
        self.l3 = ChatWindow("nono")
        self.l3.parent = self
        self.layout.addWidget(self.sideBar, 0, 0, 1, 2)

        self.layout.addWidget(self.l3,0,3,1,1)


        self.l3.inputArea.sendButton.clicked.connect(self.printer)
        self.layout.setColumnStretch(3,3)

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
        self.threadpool = QThreadPool()


        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())



    def openChat(self,username):
        l3 = ChatWindow(username)
        l3.parent = self
        l3.messagesArea.loadMessage(username)
        self.l3.deleteLater()

        self.l3.close()
        self.l3 = None
        self.l3 = l3
        self.l3.inputArea.sendButton.clicked.connect(self.printer)
        #
        self.layout.addWidget(self.l3,0,3,1,1)
        self.layout.setColumnStretch(3,3)
    def listRemoteSearchUsers(self,users):
        for u in users['users']:
            si = searchUserItem(u['username'],u['firstname'],u['lastname'],self)
            self.sideBar.userSearch.userlist.layout.addWidget(si)
            self.sideBar.userSearch.userlist.remoteDBUsers.append(si)

    def addChat(self, username):

        # f = QTextEdit(f"we {n} {edits[-1]}")
        # f = QTextEdit(f"we {self.tempNewChats[n]['username']}")
        f = MessageBox(f"{self.tempNewChats[username]['username']}",f"{json.dumps(self.tempNewChats[username]['message'])}")
        f.parent = self
        # self.chatBar.chat_list[username]=f
        # self.chatBar.layout.addWidget(f)
        self.sideBar.chatBar.chat_list[username]=f
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
                self.sideBar.chatBar.chat_list[username].setMessage(mm.content)
            self.sideBar.chatBar.chat_list[username].setMessage(jm['message']['content'])

    def sendMessage(self,username,message):
        print(message.__dict__)
        try:
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
            if self.l3.username == username and self.l3.username != self.username:
                mi = MessageItem(message)
                self.l3.messagesArea.messages.append(mi)

                self.l3.messagesArea.layout.insertWidget(len(self.l3.messagesArea.messages), mi)

        except Exception as e:
            print(e)


        #add message to area

    def listen_for_messages(self, newChat,newMessage,listFriends):
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

                    print(db.chats)

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

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def listenPool(self):
        worker = Worker(self.listen_for_messages) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.newChat.connect(self.addChat)
        worker.signals.newMessage.connect(self.newMessage)
        worker.signals.listFriends.connect(self.listRemoteSearchUsers)
        self.threadpool.start(worker)

    #TODO вынести runserver за пределы main window
    def switchTab(self, tab):
        pass

    def runServer(self):

        #url what fron auth tabs
        self.username = "user5"

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
            print(f"client disconnected",e)
            s.close()
        try:
            key = message_sender.send_message(1, cryptor.load_Public_key()['key'].save_pkcs1())
            s.send(key)
        except ConnectionResetError as e:
            print(f"client disconnected")
            s.close()
        #socket is ready
        #here authentication

    def authenticateClient(self,data,start):

        message_sender = self.message_sender
        message_receiver = self.message_receiver
        cou = 3
        while cou > 0:
            self.socket.send(message_sender.send_message(1, json.dumps(data)))
            m = self.socket.recv()
            status = json.loads(message_receiver.recieve_message(1, m))
            if status['auth_data_exchange']:

                break
            else:
                cou -= 1
                if status['error'] == 50401:
                    print('data sent unsuccessful')

        print("sent")
        m = self.socket.recv(2048)
        m = message_receiver.recieve_message(1, m)

        print(m, 'recived')
        mess = json.loads(str(m))
        print(mess)
        if mess['auth_success']:
            print(mess['AuthenticationUser'])
            self.switcTabSygnal.emit({'tab':'main'})
            self.listenPool()
        else:
            print("failed",mess['reason'])
            self.socket.close()
            self.close()
            raise KeyboardInterrupt
class sts(QObject):
    switcTabSygnal = pyqtSignal()
class AppWindow(QWidget):
    # signals
    switcTabSygnal = sts()
    def __init__(self):
        super(AppWindow, self).__init__()
        self.layout = QGridLayout()
        self.TAB = AuthenticationTab(self)
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
        self.switcTabSygnal.switcTabSygnal.connect(self.switchTab)
        self.runServer()
        self.sbut = QPushButton('sew')
        self.sbut.clicked.connect(partial(self.switchTab,{}))
        self.layout.addWidget(self.sbut)
        self.setLayout(self.layout)
        self.threadpool = QThreadPool()



    def switchTab(self):
        mv = MainWindow(self)

        # self.TAB.tab.sendButton.disconnect()
        self.layout.removeWidget(self.TAB)
        self.TAB.deleteLater()


        self.TAB = None
        self.TAB = mv
        self.layout.addWidget(self.TAB,0,0,1,1)


        self.TAB.username = self.username
        self.TAB.socket = self.socket
        self.TAB.cryptor = self.cryptor
        self.TAB.message_sender = self.message_sender
        self.TAB.message_receiver = self.message_receiver
        self.TAB.listenPool()

        print(f'tab changed tp {type(self.TAB)}')
    # def start(self,data):
    #     worker = AuthWorker(self.authenticateClient)
    #     worker.signals.finished.connect(self.thread_complete)
    #     worker.signals.start.connect(self.switchTab)
    #     self.threadpool.start(worker)
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
        except ConnectionResetError as e:
            print("client disconnected",e)
            s.close()
        # socket is ready
        # here authentication

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
        while cou > 0:
            self.socket.send(message_sender.send_message(1, json.dumps(data)))
            m = self.socket.recv()
            status = json.loads(message_receiver.recieve_message(1, m))
            if status['auth_data_exchange']:

                break
            else:
                cou -= 1
                if status['error'] == 50401:
                    print('data sent unsuccessful')

        print("sent")
        m = self.socket.recv(2048)
        m = message_receiver.recieve_message(1, m)

        print(m, 'recived')
        mess = json.loads(str(m))
        print(mess)
        if mess['auth_success']:
            print(mess['AuthenticationUser'])
            self.switcTabSygnal.switcTabSygnal.emit()
        else:
            print("failed", mess['reason'])
            self.socket.close()
            self.close()
            raise KeyboardInterrupt

if __name__ == "__main__":
    RHOST = "192.168.1.122"
    RHOST = "localhost"
    app = QApplication([])
    window = AppWindow()

    # window.runServer()
    window.show()
    app.exec_()
    window.socket.close()


# if __name__ == "__main__":
#     app = QApplication([])
#     window = CodeVerification()
#
#     window.show()
#     app.exec_()