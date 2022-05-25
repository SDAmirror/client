import database as db
import datetime
import sqlite3

con = sqlite3.connect('clients.db')

#
cursor = con.cursor()
#
# date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute('select * from users')
for row in cursor.fetchall():
    print(row)
#
# cursor.execute('''INSERT INTO messages VALUES ('This is my message, HEllO!', (?), '1', '1',
# 'sent')''', (date_time))
# con.commit()
cursor.close()
con.close()
# db.close_connection_sqlite(con)

# import schemaMessages as sM
# messagesSchema = sM.MessagesSchema()
# messagesSchema.send_message("HI there! its me", 1, 1)

