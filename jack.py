from monopoly import api
import database

#A multi-use tool. It touches the database when it needs to be touched; and this communicates with server.py
#TAKES COMMANDS FROM SERVER.PY
#Rolls the dice and reads api.py status codes

def getRoll():
    roll = api.diceRoll()
    return roll