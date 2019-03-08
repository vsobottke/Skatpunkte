import sqlite3

conn = False

def create_connection():
    global conn, cur
    if  not conn:
        conn = sqlite3.connect("skat.db", check_same_thread=False)
        cur = conn.cursor()
#datenbankverbindung
create_connection()
