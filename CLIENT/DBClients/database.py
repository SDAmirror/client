import sqlite3


# Connection:
def get_connection_sqlite():
    return sqlite3.connect("file:clients.db?mode=rw", uri=True)
    # return sqlite3.connect('clients.db')

    # return sqlite3.connect('clients.db')


def close_connection_sqlite(con):
    con.close()
