import random
import string

import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">
              <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def generate(self, length=8):
        return length


if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())

                <label for="player">Spieler</label>
                <select class="selectplayer" name="player" id="player">
                    <option value="0">Vinne</option>
                    <option value="1">Boettcher</option>
                    <option value="2">Ole</option>
                </select><br>
                <label for="points">Punkte</label>
                <input type="number" name="points" value="" name="points"><br>
                <label for="won">Gewonnen?</label>
                <input type="checkbox" name="won" value="" id="won"><br>
