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

def checkEnd(lobby):
    game = database.pullGame(lobby)
    if game == 0:
        raise Exception("The end was checked on a game that is not running.")
    playerList = game["players"]
    bankruptCount = 0
    playerUsernames = []
    for player in playerList:
        if player["username"] == "INDEBTED INMATE":
            bankruptCount = bankruptCount + 1
        else:
            playerUsernames.append((player["username"], player["money"]))
    
    #If there is a winner
    if len(playerList) - bankruptCount == 1:
        if len(playerUsernames) != 1:
            raise Exception("Code error at jack.py")
        winner = playerUsernames[0]

        database.winGame(winner[0], winner[1])
        database.endGame(lobby)
        return True
    #If something BADLY fucked up
    elif len(playerList) - bankruptCount == 0:
        raise Exception("Everyone is bankrupted. This should never ever ever ever happen.")
    #If the game is still continuing
    else:
        return False

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