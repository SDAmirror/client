import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial




class AuthAlert(QWidget):

    resized = pyqtSignal()

    def __init__(self,parent):
        super(AuthAlert, self).__init__()
        self.layout = QGridLayout()
        self.messageBox = QTextEdit()
        self.messageBox.setStyleSheet("""

                    .QTextEdit {
                      appearance: none;
                      background-color: #FAFBFC;
                      border: 1px solid rgba(27, 31, 35, 0.15);
                      border-radius: 6px;
                      border: #2EFF2E solid 1px;
                      box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                      box-sizing: border-box;
                      color: red;
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
        self.messageBox.setReadOnly(True)
        self.messageBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.messageBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.messageBox.setSizePolicy(QSizePolicy.Expanding, 0)

        self.messageBox.setAttribute(103)

        self.layout.addWidget(self.messageBox,0,0,1,1)
        self.setLayout(self.layout)

        self.resized.connect(self.adj)
        self.messageBox.textChanged.connect(self.adj)

    def adjHeight(self):
        self.messageBox.setFixedHeight(
            math.ceil(self.messageBox.document().size().height()) + math.ceil(self.messageBox.contentsMargins().top() * 2))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(AuthAlert, self).resizeEvent(event)

    # resize message items
    def adj(self):
        # self.dateWidget.setFixedHeight(math.ceil(self.dateWidget.document().size().height()) + math.ceil(self.dateWidget.contentsMargins().top() * 2))
        self.messageBox.setFixedHeight(
            math.ceil(self.messageBox.document().size().height()) + math.ceil(self.messageBox.contentsMargins().top() * 2))


class LoginTab(QWidget):
    def __init__(self,parent):
        super(LoginTab, self).__init__()
        self.parent = parent
        self.tabName = "login"
        self.layout = QGridLayout()
        self.username = QLineEdit()
        self.username.setStyleSheet("""

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
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""

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
        self.layout.addWidget(QLabel("username"),0,0,1,1)
        self.layout.addWidget(self.username,0,1,1,1)
        self.layout.addWidget(QLabel("password"),1,0,1,1)
        self.layout.addWidget(self.password,1,1,1,1)
        self.sendButton = QPushButton("LOGIN")
        self.sendButton.setStyleSheet("""
        
            .QPushButton {
              appearance: none;
              background-color: green;
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
        self.layout.addWidget(self.sendButton,2,0,1,2)
        self.sendButton.clicked.connect(self.prepareData)
        self.layout.addWidget(QLabel("Not registred yet? "), 3, 0, 1, 1)
        self.switchButton = QPushButton("REGISTER")
        self.layout.addWidget(self.switchButton, 3, 1, 1, 1)
        self.switchButton.setStyleSheet("""

                                    .QPushButton {
                                      appearance: none;
                                      background-color: #FAFBFC;
                                      border: 1px solid rgba(27, 31, 35, 0.15);
                                      border-radius: 6px;
                                      border: #2EFF2E solid 1px;
                                      box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                                      box-sizing: border-box;
                                      color: blue;
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
        self.layout.setRowStretch(1,1)
        self.layout.setRowStretch(2,1)
        self.layout.setRowStretch(3,1)
        self.layout.setRowStretch(4,1)
        self.setStyleSheet("""
                  .LoginTab {
                      background: #DCEEC8;
                  }
              """)
        self.setLayout(self.layout)
    def prepareData(self):

        data = {
            "auth_check": 1,
            "url": "authorization",
            "authorization_data": [str(self.username.text()).strip(), str(self.password.text()).strip()],
        }

        self.parent.authenticateClient(data)
    def print(self):
        print(f"{self.username.text()} {self.password.text()}")

class RegistrationTab(QWidget):
    def __init__(self,parent):

        super(RegistrationTab, self).__init__()
        self.parent = parent
        self.tabName = "register"
        self.layout = QGridLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password_repeat = QLineEdit()
        self.firstname = QLineEdit()
        self.lastname = QLineEdit()
        self.email = QLineEdit()
        self.username.setStyleSheet("""

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
        self.password.setStyleSheet("""

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
        self.password.setEchoMode(QLineEdit.Password)
        self.password_repeat.setStyleSheet("""

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
        self.password_repeat.setEchoMode(QLineEdit.Password)
        self.firstname.setStyleSheet("""

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
        self.lastname.setStyleSheet("""

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
        self.email.setStyleSheet("""

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

        self.layout.addWidget(QLabel("username"), 0, 0, 1, 1)
        self.layout.addWidget(self.username, 0, 1, 1, 1)
        self.layout.addWidget(QLabel("password"), 1, 0, 1, 1)
        self.layout.addWidget(self.password, 1, 1, 1, 1)
        self.layout.addWidget(QLabel("repeat password"), 2, 0, 1, 1)
        self.layout.addWidget(self.password_repeat, 2, 1, 1, 1)
        self.layout.addWidget(QLabel("firstname"), 3, 0, 1, 1)
        self.layout.addWidget(self.firstname, 3, 1, 1, 1)
        self.layout.addWidget(QLabel("lastname"), 4, 0, 1, 1)
        self.layout.addWidget(self.lastname, 4, 1, 1, 1)
        self.layout.addWidget(QLabel("email"), 5, 0, 1, 1)
        self.layout.addWidget(self.email, 5, 1, 1, 1)
        self.sendButton = QPushButton("Registration")
        self.sendButton.setStyleSheet("""

                    .QPushButton {
                      appearance: none;
                      background-color: green;
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
        self.layout.addWidget(self.sendButton, 6, 0, 1, 2)
        self.sendButton.clicked.connect(self.prepareData)

        self.layout.addWidget(QLabel("Allready registred?"), 7, 0, 1, 1)
        self.switchButton = QPushButton("Login")
        self.layout.addWidget(self.switchButton, 7, 1, 1, 1)
        self.switchButton.setStyleSheet("""

                                    .QPushButton {
                                      appearance: none;
                                      background-color: #FAFBFC;
                                      border: 1px solid rgba(27, 31, 35, 0.15);
                                      border-radius: 6px;
                                      border: #2EFF2E solid 1px;
                                      box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
                                      box-sizing: border-box;
                                      color: blue;
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

        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)
        self.layout.setRowStretch(3, 1)
        self.layout.setRowStretch(4, 1)
        self.layout.setRowStretch(5, 1)
        self.layout.setRowStretch(6, 1)
        self.layout.setRowStretch(7, 1)
        self.layout.setRowStretch(8, 1)
        self.setLayout(self.layout)
        self.setStyleSheet("""
            .RegistrationTab {
                background: #DCEEC8;
            }
        """)
    def prepareData(self):
        if not self.password.text().strip() == self.password_repeat.text().strip():
            print('repeat pass do not matc')
        else:
            data = {
                "auth_check": 1,
                "url": "registration",
                "registration_data": {
                    "username": str(self.username.text()).strip(),
                    "password": str(self.password.text()).strip(),
                    "first_name": str(self.firstname.text()).strip(),
                    "last_name": str(self.lastname.text()).strip(),
                    "email": str(self.email.text()).strip()
                }
            }
            self.parent.registerClient(data)

    def print(self):
        print(f"{self.username.text()} {self.password.text()}")

class CodeVerification(QWidget):

    def __init__(self,parent):
        super(CodeVerification, self).__init__()
        self.parent = parent
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("CODE"), 0, 0, 1, 1)
        self.codeInput = QLineEdit()
        self.codeInput.setStyleSheet("""

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
        self.layout.addWidget(self.codeInput,0,1,1,1)
        self.sendButton = QPushButton("SEND")
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
        self.sendButton.clicked.connect(self.prepareData)
        self.layout.addWidget(self.sendButton, 1, 0, 1, 2)
        self.setLayout(self.layout)

    def prepareData(self):
        code = self.codeInput.text().strip()
        self.parent.sendCode(code)

class AuthenticationTab(QWidget):

    def __init__(self,parent):
        super(AuthenticationTab, self).__init__()
        self.tabName = 'authTab'
        self.codeVerification = None
        self.parent = parent
        self.layout = QGridLayout()
        self.alert = AuthAlert(parent)
        self.layout.addWidget(self.alert,0,0,1,1)
        self.tab = LoginTab(parent)
        self.layout.addWidget(self.tab,1,0,1,1)
        self.tab.switchButton.clicked.connect(self.switchTab)
        self.setLayout(self.layout)

    def switchTab(self):
        if self.tab.tabName == "login":
            tab = RegistrationTab(self.parent)
            # self.parent.AuthHandlerSwitch = True
            # self.parent.registerPool()
        elif self.tab.tabName == "register":
            tab = LoginTab(self.parent)
            # self.parent.AuthHandlerSwitch = False
        # if self.codeVerification != None:
        #     self.layout.removeWidget(self.codeVerification)
        #     self.codeVerification.deleteLater()
        #     self.codeVerification.close()
        #     self.codeVerification = None

        self.layout.removeWidget(self.tab)
        self.tab.deleteLater()
        self.tab.close()
        self.tab = None
        self.tab = tab
        self.tab.switchButton.clicked.connect(self.switchTab)
        self.layout.addWidget(self.tab,1,0,1,1)


    def processAuthentication(self):
        pass
    def addCodeVerification(self):
        print('addCodeVerification')
        self.codeVerification = CodeVerification(self.parent)
        self.layout.addWidget(self.codeVerification, 2, 0, 1, 1)
        self.update()
        print('addCodeVerification2')
    def reportError(self,error):
        self.alert.messageBox.setText(error['reason'])


