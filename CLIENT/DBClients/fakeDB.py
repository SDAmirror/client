import json
{'user3':
     {'messages': [
            {
                'url': 'message',
                'message': {
                    'sender': 'user3',
                    'receiver': 'user5',
                    'sent': True,
                    'id': '184f5916-ab38-4fe9-9615-72d79a4a5f0c',
                    'content': 'dwdawddwdw',
                    'send_date': '2022-05-21',
                    'send_time': '14:51:26'
                }
            }
        ]
     }
}
class MessageModel:
    def __init__(self,id,content,sender,receiver,send_date,send_time,sent):
        self.__class__.__name__ = "message"
        self.id = id
        self.content = content
        self.sender = sender
        self.receiver = receiver
        self.send_date = send_date
        self.send_time = send_time
        self.sent = sent


class Chat:
    def __init__(self,username):
        self.username = username
        self.messages = []
class DB:
    def __init__(self):
        # self.chats = {'user1': {'messages': [],'firstname':'firstname','lastname':'lastname'}}
        self.chats = {}

        self.users = {'user1': {'firstname':'firstname','lastname':'lastname'}}
    def addChat(self,username):

        self.chats[username] = {"messages":[]}


    def newMessage(self,username,message):
        self.chats[username]["messages"].append(message)

    def getChat(self,username):
        if not username in list(self.chats.keys()):
            return Chat(username)
        chat = Chat(username)
        for i in self.chats[username]["messages"]:
            chat.messages.append(MessageModel(i['message']['id'], i['message']['content'], i['message']['sender'], i['message']['receiver'], i['message']['send_date'], i['message']['send_time'], i['message']['sent']))

        return chat


    def getAllChats(self):
        return self.chats

    def getChatByUserPattern(self,pattern):
        #pattern search function
        if pattern in list(self.chats.keys()):
            return [{"username":pattern,'firstname':'firstname','lastname':'lastname'}]
        else:
            return []


