import pandas as pd
from pandas import DataFrame
import time
from lib.DB_connection import cur, conn
from lib.Runde import Runde
from lib.Spiel import Spiel
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
from lib.Spieler import Spieler

# Get Current Dir for jinja2
path = os.path.abspath(os.path.dirname(__file__))
print("the path is " + path)
env = Environment(loader=FileSystemLoader(path), trim_blocks=True)

players = ["Player1", "Player2", "Player3"]
spiel = Spiel()


def create_player_select_tag(players):
    """
    Returns an html-select-tag with the options based on passed in players (list).
    """

    select = "<select name='player'>"
    for count, player in enumerate(players):
        select += f"<option value={count}>{player}</option>"
    select += "</select>"
    return select


neue_runde_form = """<form method="get" action="generate_runde">
          """ + create_player_select_tag(players) + """
          <input type="number" value="18" name="points" />
          <button type="submit">Eintragen</button>
        </form>"""

neues_spiel_button = """<a href="generate_spiel"> Neues Spiel</a>"""

template = env.get_template('index.html')


def create_spieler_select(select_name, spieler_liste):
    input = '<select name=' + select_name + '>'
    for i in spieler_liste:
        input += "<option value=" + str(i[0]) + ">" + i[1] + "</option>"
    input += "</select>"
    return input


# Our Controller
class Skat:

    @cherrypy.expose
    def index(self):
        return template.render(content=spiel.get_spiele() + neues_spiel_button, title="Index")

    @cherrypy.expose
    def generate_runde(self, points=0, player=14):
        Runde.createRunde(spiel.id, player, points)
        return """<meta http-equiv="refresh" content="0; URL='/spiel'" />"""  # Weiterleitung auf Spiel

    @cherrypy.expose
    def spiel(self):
        return template.render(content=neue_runde_form + "<br>" + spiel.create_dataframe_from_runden(), title="Spiel")

    @cherrypy.expose
    def generate_spiel(self):
        spieler_liste = Spieler.get_alle_spieler()

        spieler_auswahl = """<form method="get" action="create_spiel">"""
        spieler_auswahl += "Vorhand    " + create_spieler_select('vorhand', spieler_liste) + "<br>" \
                           + "Mittelhand " + create_spieler_select('mittelhand', spieler_liste) + "<br>" \
                           + "Hinterhand " + create_spieler_select('hinterhand', spieler_liste) + "<br>" + "<br>" \
                           + "Re-Partei   " + create_spieler_select("re_partei",
                                                                   spieler_liste) + "<input type='number' value='18' name='punkte' />"
        spieler_auswahl += """<br><a href=neuer_spieler style= 'hidden'> Neuer Spieler </a><br>

        <button type="submit">Spiel erstellen</button>
      </form>"""

        return template.render(content=spieler_auswahl, title="Spielerauswahl")

    @cherrypy.expose
    def create_spiel(self, vorhand, mittelhand, hinterhand, re_partei, punkte):
        spiel.id = Spiel.create_spiel()[0][0]
        # Easy: Spieler + Re-Partei + Punkte werden hier übergeben
        # Als nächstes muss der ein Eintrag in der DB-Tablle spielerpositionen erstellt werden
        # danach muss die Runde angelegt werden: runde.createRunde(spiel.id, int(player), int(points))
        return """<meta http-equiv="refresh" content="0; URL='/spiel'" />"""  # weiterleitung auf spiel


# cherrypy.config.update("server.conf")

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    }
    cherrypy.quickstart(Skat(), '/', conf)
