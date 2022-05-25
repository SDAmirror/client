import datetime
import sqlite3

import messenger.CLIENT.DBClients.database as db

class MessagesSchema:
    def __init__(self):
        self.db = db

    def send_message(self, message, sender_id, sent):
        try:
            con = self.db.get_connection_sqlite()
            try:
                cursor = con.cursor()
                date_time = datetime.datetime.now()
                # sent check ?
                cursor.execute("insert into messages values(?, ?, ?, ?, ?)", (message, date_time.strftime("%Y-%m-%d %H:%M:%S"), sent, 'sent', sender_id))
                con.commit()
            except Exception as e:
                print("error in sending message", e)
        except Exception as e:
            print("Connection error", e)
        finally:
            self.db.close_connection_sqlite(con)

    def receive_message(self, message, sender_id):
        try:
            con = self.db.get_connection_sqlite()
            try:
                cursor = con.cursor()
                date_time = datetime.datetime.now()
                sent = False
                # sent check ?
                cursor.execute("insert into messages values(?, ?, ?, ?, ?)", (message, date_time.strftime("%Y-%m-%d %H:%M:%S"), sent, 'received', sender_id))
                con.commit()
            except Exception as e:
                print("connection error", e)
        except Exception as e:
            print("error in receiving message", e)
        finally:
            db.close_connection_sqlite(con)




