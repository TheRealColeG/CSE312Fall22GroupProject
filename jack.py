from monopoly import api
import database

#A multi-use tool. It touches the database when it needs to be touched; and this communicates with server.py
#TAKES COMMANDS FROM SERVER.PY
#Rolls the dice and reads api.py status codes

def startGame(lobby, usernames):
    game = api.initGame(usernames)
    database.setGame(lobby, game)

#
def sendMove(lobby, player, roll):
    game = database.pullGame(lobby)
    game = api.move(game, player, roll)
    database.setGame(lobby, game)
    return game["status"]