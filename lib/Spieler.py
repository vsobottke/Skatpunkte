from pandas import DataFrame
from  lib.DB_connection import cur,conn
import time

class Spieler(object):
    def __init__(self, name="Neuer Spieler"):
        self.name = name

    @staticmethod
    def get_spieler(spieler_id):
        return cur.execute("""SELECT * FROM spieler WHERE id = %d""" % (spieler_id)).fetchall()

    @staticmethod
    def get_alle_spieler():
        return cur.execute("""SELECT * FROM spieler""").fetchall()

    @staticmethod
    def create_spieler(name):
        cur.execute("""INSERT INTO spieler(name) VALUES(%s)""" % (name))
        conn.commit()
        return Spieler.get_spieler(cur.lastrowid)
