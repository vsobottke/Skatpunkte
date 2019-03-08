import pandas as pd
from pandas import DataFrame
import time
from  lib.DB_connection import cur,conn
from lib.Runde import Runde
from lib.Spiel import Spiel
import cherrypy
import os
from jinja2 import Environment, FileSystemLoader

#Get Current Dir for jinja2
path = os.path.abspath(os.path.dirname(__file__))
print("the path is " + path)
env=Environment(loader=FileSystemLoader(path),trim_blocks=True)
#Datenbank

#SPIEL HINZUFÜGEN:
spiel = int(time.time())
anzahl_runden, anzahl_punkte = 12,1000
cur.execute("""INSERT INTO spiel(datum, anzahl_runden, anzahl_punkte) VALUES(%s, %s, %s)""" % (spiel, anzahl_runden, anzahl_punkte))

conn.commit()


players = ["Vinne","Boettch","Sushi"]
runde = Runde(1, 3, 192)
spiel = Spiel(12,100)


def playerselect():
    string = "<select name='player'>"
    count = 0
    for p in players:
        string += "<option value=" + str(count) + ">" + p + "</option>"
        count +=1
    string += "</select>"
    return string

form = """<form method="get" action="generate">
          """ + playerselect() +  """
          <input type="number" value="18" name="points" />
          <button type="submit" value="Submit">Eintragen</button>
        </form>"""
template = env.get_template('index.html')

# Our Controller
class Skat(object):
    #@cherrypy.expose
    #def index(self):
        #render template
    #    return template.render(content=writetable(),title="Neuer Template Titel",button='<button><a href="/add">Neue Runde</a></button>')

    @cherrypy.expose
    def generate(self, points=0, player=14):
        runde.createRunde(12, int(player), int(points))
        return  """<meta http-equiv="refresh" content="0; URL='/index'" />""" #weiterleitung auf index

    @cherrypy.expose
    def index(self):

        return template.render(content=form+"<br>"+spiel.create_dataframe_from_runden(12), title="Arsch")

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
