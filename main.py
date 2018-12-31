import cherrypy
import os
from jinja2 import Environment, FileSystemLoader

#Get Current Dir for jinja2
path = os.path.abspath(os.path.dirname(__file__))
print("the path is " + path)
env=Environment(loader=FileSystemLoader(path),trim_blocks=True)
#players_names = ["vinne", "böttch", "qualle"]
#players_points = [[], [], []]
points = [[],[],[]]
players = ["Vinne","Boettch","Sushi"]

def writetable():
    string = '<table style="width:100%"> <tr>'
    for i in range(0,len(points)):
        string += "<th>" + players[i] + "</th>"
    string += '</tr>'
    #for all columns -> add point
    for g in range(0,len(points[0])):
        string += '<tr>'
        for p in range(0,len(players)):
            string += "<th>" + str(points[p][g]) + "</th>"
        string += '</tr>'
    string += '<tr>'
    for i in range(0,len(players)):
        string += "<th>" + str(listsum(points[i])) + "</th>"
    string += '</tr>'
    string += '</table>'
    return string

def playerselect():
    string = "<select name='player'>"
    count = 0
    for p in players:
        string += "<option value=" + str(count) + ">" + p + "</option>"
        count +=1
    string += "</select>"
    return string

def addpoints(p,player):
    global points
    for i in range(0,len(points)):
        if i == player:
            points[i].append(p)
        else:
            points[i].append(0)
def listsum(numList):
    theSum = 0
    for i in numList:
        theSum = theSum + i
    return theSum

form = """<form method="get" action="generate">
          """ + playerselect() +  """
          <input type="number" value="18" name="points" />
          <button type="submit" value="Submit">Eintragen</button>
        </form>"""
template = env.get_template('index.html')

# Our Controller
class Skat(object):
    @cherrypy.expose
    def index(self):
        #render template
        return template.render(content=writetable(),title="Neuer Template Titel",button='<button><a href="/add">Neue Runde</a></button>')

    @cherrypy.expose
    def generate(self, points=0, player=14):
        addpoints(int(points),int(player))
        return  """<meta http-equiv="refresh" content="0; URL='/index'" />""" #weiterleitung auf index

    @cherrypy.expose
    def add(self):
        return template.render(content=form, title="Arsch")

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
