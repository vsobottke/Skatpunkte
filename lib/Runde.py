from  lib.DB_connection import cur,conn

class Runde(object):

    # TODO: spielart, bock, re, kontra, mit, ohne, gewonnen, hand, ouvert, schneider, schneider_angesagt, schwarz, schwarz_angesagt,
    def __init__(self, spiel_id, re_partei, punkte):
#         self.id = id
        self.spiel_id = spiel_id
        self.re_partei = re_partei
        self.punkte = punkte
#         self.spielart = spielart
#         self.bock = bock
#         self.re = re
#         self.kontra = kontra
#         self.mit = mit
#         self.ohne = ohne
#         self.gewonnen = gewonnen
#         self.hand = hand
#         self.ouvert = ouvert
#         self.schneider = schneider
#         self.schneider_angesagt = schneider_angesagt
#         self.schwarz = schwarz
#         self.schwarz_angesagt = schwarz_angesagt

    # TODO erweitern im weitere Eigenschaften wie Farbe, Spiel, verloren etc.
    def createRunde(self, spiel_id, re_partei, punkte):
        cur.execute("""INSERT INTO runde(spiel_id, re_partei, punkte) VALUES(%s, %s, %s)""" % (spiel_id, re_partei, punkte))
        conn.commit()
