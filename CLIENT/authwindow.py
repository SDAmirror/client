from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial




class AuthAlert(QWidget):
    def __init__(self,parent):
        super(AuthAlert, self).__init__()
        self.layout = QGridLayout()
        self.messageBox = QTextEdit("alert")
        self.layout.addWidget(self.messageBox,0,0,1,1)
        self.setLayout(self.layout)

class LoginTab(QWidget):
    def __init__(self,parent):
        super(LoginTab, self).__init__()
        self.parent = parent
        self.tabName = "login"
        self.layout = QGridLayout()
        self.username = QLineEdit("user1")
        self.password = QLineEdit("password1")
        self.layout.addWidget(QLabel("username"),0,0,1,1)
        self.layout.addWidget(self.username,0,1,1,1)
        self.layout.addWidget(QLabel("password"),1,0,1,1)
        self.layout.addWidget(self.password,1,1,1,1)
        self.sendButton = QPushButton("LOGIN")
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
        self.layout.setRowStretch(1,1)
        self.layout.setRowStretch(2,1)
        self.layout.setRowStretch(3,1)
        self.layout.setRowStretch(4,1)
        self.setLayout(self.layout)
        self.setStyleSheet("""
                  .LoginTab {
                      background: #DCEEC8;
                  }
              """)
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
        {
            "auth_check": 1,
            "url": "authorization",
            # "authentification_check": False,
            "authentification_token": "d3a5f6cb-01a8-4bff-b076-64550ff85921",
            # "authorization_check": False,
            "authorization_data": ["user5", "password3"],
            "registration_data": {
                "username": "555666",
                "password": "passwordww3",
                "first_name": "first_name3",
                "last_name": "last_name3",
                # "email": "myvideoboxdsa@gmail.com"
                "email": "d.sadykov@astanait.edu.kz"
                # "email": "gulnur.kst@gmail.com"
            }
        }
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
        self.sendButton = QPushButton("REGISTRATION")
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
        self.layout.addWidget(self.sendButton, 6, 0, 1, 2)
        self.sendButton.clicked.connect(self.print)

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
        if self.password.text().strip() == self.password_repeat.text().strip():
            print('repeat pass do not matc')
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
        return data

    def print(self):
        print(f"{self.username.text()} {self.password.text()}")

class CodeVerification(QWidget):

    def __init__(self,parent):
        super(CodeVerification, self).__init__()
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("CODE"), 0, 0, 1, 1)
        self.layout.addWidget(self.password, 0, 1, 1, 1)
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
        self.layout.addWidget(self.sendButton, 1, 0, 1, 2)
class AuthenticationTab(QWidget):
    def __init__(self,parent):
        super(AuthenticationTab, self).__init__()
        self.parent = parent
        self.layout = QGridLayout()
        self.alert = AuthAlert(parent)
        self.layout.addWidget(self.alert,0,0,1,1)
        self.tab = LoginTab(parent)
        self.layout.addWidget(self.tab,1,0,1,1)
        self.setLayout(self.layout)

    def processAuthentication(self):
        pass

    def reportError(self,error):
        self.alert.messageBox.setText(error['reason'])

