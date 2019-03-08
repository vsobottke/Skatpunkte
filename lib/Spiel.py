from pandas import DataFrame
from  lib.DB_connection import cur,conn
import time

class Spiel(object):
    def __init__(self, anzahl_runden=12, anzahl_punkte=1000):
        self.id = id
        self.datum = int(time.time())
        self.anzahl_runden = anzahl_runden
        self.anzahl_punkte = anzahl_punkte

    def get_runden(self, spiel_id):
        return cur.execute("SELECT * FROM runde WHERE spiel_id = %d" % (spiel_id)).fetchall()

    def create_dataframe_from_runden(self, spiel_id):
        runden = self.get_runden(spiel_id)
        id_spieler1, id_spieler2, id_spieler3 = 0,1,2 # TODO: hartes hardcoding beseitigen (hart)
        # zeile[2] ist re-partei zeile[-1] entspricht Punktes
        spieler_1 = [(zeile[-1] if zeile[2] == id_spieler1 else 0) for zeile in runden]
        spieler_2 = [(zeile[-1] if zeile[2] == id_spieler2 else 0) for zeile in runden]
        spieler_3 = [(zeile[-1] if zeile[2] == id_spieler3 else 0) for zeile in runden]

        punkte_tabelle = DataFrame({'Vinne': spieler_1, 'Böttch': spieler_2, 'Sushi': spieler_3}, dtype=int)
        return punkte_tabelle.append(punkte_tabelle.sum(), ignore_index=True).to_html()

    def get_spiele(self):
        return DataFrame(cur.execute("SELECT * FROM spiel").fetchall()).to_html()

    @staticmethod
    def create_spiel(anzahl_runden=12, anzahl_punkte=1000):
        zeitstempel = int(time.time())
        anzahl_runden, anzahl_punkte = anzahl_runden, anzahl_punkte
        cur.execute("""INSERT INTO spiel(datum, anzahl_runden, anzahl_punkte) VALUES(%s, %s, %s)""" % (zeitstempel, anzahl_runden, anzahl_punkte))
        conn.commit()
        return Spiel.get_spiel(cur.lastrowid)

    @staticmethod
    def get_spiel(spiel_id):
        return cur.execute("""SELECT * FROM spiel WHERE id = %d""" % (spiel_id)).fetchall()
