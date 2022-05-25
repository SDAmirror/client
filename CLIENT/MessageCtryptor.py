import os

import rsa
#TODO client sends public key not server
class RSACryptor:
    def __init__(self,id):
        self.id = id
    def load_Private_key(self):
        with open(f'private{self.id}.pem', 'r') as privatefile:
            priv = rsa.PrivateKey.load_pkcs1(privatefile.read(), 'PEM')
            return {'key':priv,'errors':[]}
    def load_Public_key(self):
        with open(f'public{self.id}.pem', 'r') as publicfile:
            pub = rsa.PublicKey.load_pkcs1(publicfile.read())
            return {'key':pub,'errors':[]}

    def load_server_Public_key(self):
        with open(f'server_public{self.id}.pem', 'r') as cl_publicfile:
            pub = rsa.PublicKey.load_pkcs1(cl_publicfile.read())
            return {'key':pub,'errors':[]}

    def decrypt(self,message):
        ress = self.load_Private_key()
        try:
            m = ''
            for i in range(0, len(message), 128):
                m += rsa.decrypt(message[i:i + 128], ress['key']).decode()
            return m
        except Exception as e:
            print(e)
        return message

    def encrypt(self,message):
        ress = self.load_server_Public_key()
        key = ress['key']
        try:
            l = len(message)

            if l % 64 != 0:
                message += ' ' * (l % 64)
            temp = []
            for i in range(0, len(message), 64):
                temp.append(rsa.encrypt(message[i:i + 64].encode('ISO-8859-1'), key))

            return b''.join(temp)


        except Exception as e:
            print(e)
        return message


    def delete_RSA_keys(self,id):
        path = '{}'
        try:
            os.remove(path.format(f'private{id}.pem'))
        except FileNotFoundError as e:
            print('file: {} not found'.format(path.format(f'private{id}.pem')), e)
        except OSError as error:
            print("There was an error.", error)
        try:
            os.remove(path.format(f'public{id}.pem'))
        except FileNotFoundError as e:
            print('file: {} not found'.format(path.format(f'public{self.id}.pem')), e)
        except OSError as error:
            print("There was an error.", error)
        try:
            os.remove(path.format(f'client_public{self.id}.pem'))
        except FileNotFoundError as e:
            print('file: {} not found'.format(path.format(f'server_public{self.id}.pem')), e)
        except OSError as error:
            print("There was an error.", error)

    def generate_RSA_keys(self):
        (pub, priv) = rsa.newkeys(1024)


        with open(f'private{self.id}.pem', 'w') as priv_key_file:
            priv_key_file.write(priv.save_pkcs1().decode('utf-8'))

        with open(f'public{self.id}.pem', 'w') as pub_key_file:
            pub_key_file.write(pub.save_pkcs1().decode('utf-8'))

    def set_server_public_key(self,key):
        with open(f'server_public{self.id}.pem', 'w') as cl_publicfile:
            cl_publicfile.write(key)



