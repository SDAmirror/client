def message_processor(message):
    return 44124


class Message_Recirver:
    def __init__(self, cryptor=None):
        self.cryptor = cryptor
        self.db = None

    def recieve_message(self, id, message):
        return self.cryptor.decrypt(message).rstrip()

        # return message

class Message_Sender:
    def __init__(self, cryptor=None):
        self.cryptor = cryptor

    def send_message(self, id, message):
        return self.cryptor.encrypt(message)


class Message_Processor:
    def __init__(self, client):
        self.client = client
