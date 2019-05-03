import pandas as pd
from pandas import DataFrame
import time
from  lib.DB_connection import cur,conn
from lib.Runde import Runde
from lib.Spiel import Spiel
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
from lib.Spieler import Spieler


#Get Current Dir for jinja2
path = os.path.abspath(os.path.dirname(__file__))
print("the path is " + path)
env=Environment(loader=FileSystemLoader(path),trim_blocks=True)


players = ["Vinne","Boettch","Sushi"]
runde = Runde(1, 3, 192)
spiel = Spiel()
spiel.id = 1
# print(Spiel.create_spiel())

def playerselect():
    string = "<select name='player'>"
    count = 0
    for p in players:
        string += "<option value=" + str(count) + ">" + p + "</option>"
        count +=1
    string += "</select>"
    return string

neue_runde_form = """<form method="get" action="generate_runde">
          """ + playerselect() +  """
          <input type="number" value="18" name="points" />
          <button type="submit">Eintragen</button>
        </form>"""

neues_spiel_button = """<a href="generate_spiel"> Neues Spiel</a>"""

template = env.get_template('index.html')

def create_spieler_select(select_name, spieler_liste):
    input = '<select name=' + select_name + '>'
    for i in spieler_liste:
        input += "<option value=" + str(i[0]) +">" + i[1] + "</option>"
    input += "</select>"
    return input

# Our Controller
class Skat(object):
    #@cherrypy.expose
    #def index(self):
        #render template
    #    return template.render(content=writetable(),title="Neuer Template Titel",button='<button><a href="/add">Neue Runde</a></button>')
    @cherrypy.expose
    def index(self):
        return template.render(content=spiel.get_spiele() + neues_spiel_button, title="Index")

    @cherrypy.expose
    def generate_runde(self, points=0, player=14):
        runde.createRunde(12, int(player), int(points))
        return  """<meta http-equiv="refresh" content="0; URL='/spiel'" />""" #weiterleitung auf spiel


    @cherrypy.expose
    def spiel(self):
        return template.render(content=neue_runde_form+"<br>"+spiel.create_dataframe_from_runden(12), title="Spiel")

    @cherrypy.expose
    def generate_spiel(self):
        spieler = Spieler.get_alle_spieler()

        spieler_auswahl = """<form method="get" action="create_spiel">"""
        spieler_auswahl += create_spieler_select('spieler1', spieler) + create_spieler_select('spieler2', spieler) + create_spieler_select('spieler3', spieler)
        spieler_auswahl += """<br><a href=neuer_spieler style= 'hidden'> Neuer Spieler </a><br>
        <button type="submit">Spiel erstellen</button>
      </form>"""

        return template.render(content=spieler_auswahl, title="Spielerauswahl")

    @cherrypy.expose
    def create_spiel(self, spieler1, spieler2, spieler3):
        # runde.createRunde(12, int(player), int(points))
        return  """<meta http-equiv="refresh" content="0; URL='/spiel'" />""" #weiterleitung auf spiel

#cherrypy.config.update("server.conf")

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
