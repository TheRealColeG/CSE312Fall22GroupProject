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

def authTurn(lobby, orientation):
    game = database.pullGame(lobby)
    turn = game["status"][0]
    if turn == orientation:
        return True
    return False

def pullTurn(lobby):
    game = database.pullGame(lobby)
    if game == 0:
        raise Exception("bad game in pullTurn([...])")
    return game["status"][0]

def purchase(lobby, username):
    game = database.pullGame(lobby)
    board = game["board"]
    if game == 0:
        raise Exception("no game available in purchase([...])")
    snatch = None
    players = game["players"]
    for i in range(len(players)):
        p = players[i]
        if p["username"] == username:
            snatch = i
            break
    player = players[snatch]

    location = player["location"]
    property = board[location]
    property = api.buyProperty(property, player)

    player = api.transferOwnership(property, player)

    playerList = []
    for i in range(len(players)):
        if i != snatch:
            playerList.append(players[i])
        else:
            playerList.append(player)
    
    game["players"] = playerList

    gameBoard = []
    for i in range(len(board)):
        if board[i]["name"] != property["name"]:
            gameBoard.append(board[i])
        else:
            gameBoard.append(property)
    game["board"] = gameBoard

    database.setGame(lobby, game)
    return game["status"]
#
def sendMove(lobby, player, roll):
    game = database.pullGame(lobby)
    if game == 0:
        raise Exception("No game available in sendMove([...]).")
    #
    snatch = None
    players = game["players"]
    for p in players:
        if p["username"] == player:
            snatch = p
            break
    player = snatch
    #
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
    return json.dumps(game["board"])

def pullPlayerList(lobby):
    game = database.pullGame(lobby)
    playerList = game["players"]
    return json.dumps(playerList)