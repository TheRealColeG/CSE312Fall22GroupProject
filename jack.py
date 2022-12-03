from monopoly import api
import database
import json

#A multi-use tool. It touches the database when it needs to be touched; and this communicates with server.py
#TAKES COMMANDS FROM SERVER.PY
#Rolls the dice and reads api.py status codes

def startGame(lobby, usernames):
    game = api.initGame(usernames)
    database.setGame(lobby, game)
    return game["status"]

#
def sendMove(lobby, player, roll):
    game = database.pullGame(lobby)
    if game == 0:
        raise Exception("No game available.")
    game = api.move(game, player, roll)
    database.setGame(lobby, game)
    return game["status"]

def pullBoard(lobby):
    game = database.pullGame(lobby)
    if game == 0:
        raise Exception("No game available.")
    board = game["board"]
    return json.dumps(board)

def pullPlayerList(lobby):
    game = database.pullGame(lobby)
    playerList = game["players"]
    return json.dumps(playerList)