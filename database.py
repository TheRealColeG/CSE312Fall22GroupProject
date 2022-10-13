import random
from pymongo import MongoClient

#This will initialize (if not already) a MongoClient, a database and several collections.
client = MongoClient("mongo", 27017)
#db is the database
db = client["monopoly"]
#Current highest ID
ids = db["identification"]
#Keeps track of current details for the ? game slots
games = db["games"]
#Public information about each player. ID, Username, Wins, Monies
publicPlayers = db["players"]
#Private login information. ID, Username, Salt, Password
privatePlayers = db["information"]
#Taken Usernames
takenNames = db["names"]

#If there are no accounts created
if "names" not in db.list_collection_names():
    takenNames.insert_one({"list" : []})

#If no games are in progress, set the lobbies to 0 (nothing)
if "games" not in db.list_collection_names():
    games.insert_many({"1" : 0}, {"2" : 0}, {"3" : 0}, {"4" : 0}, {"5" : 0}, {"6" : 0}, {"7" : 0}, {"8" : 0})

#If no entries have been created yet, set the first available ID to 0
if "identification" not in db.list_collection_names():
    ids.insert_one({"current" : 0})

#Deletes the stupid AIDS Mongo _id from ANY ONE dictionary
def sanitize(diseased):
    cured = {}
    for key in diseased.keys():
        if key != "_id":
            cured[key] = diseased[key]
    return cured

#Returns True if the username and password correspond to an entry on file
def login(username, password):
    #Pulls the entry at the 
    existing = list(privatePlayers.find({"username" : username}))
    #If there is no such entry at that ID
    if existing == []:
        return False
    existing = sanitize(existing[0])
    salt = existing["salt"]
    hidden = hash(password+"Q"+salt)
    if hidden == existing["password"]:
        return True
    else:
        return False

#Returns a randomized salt (16 chars)
def salt():
    fullList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    chars = []
    for _ in range(16):
        chars.append(random.choice(fullList))
    salt = ""
    for char in chars:
        salt = salt + char
    return salt

#If the username is available, it will create a new player character.
#If not, it will return -1
def newAccount(username, password):
    #The list of taken names
    copy = list(takenNames.find({}))[0]["names"]
    names = copy
    #If the username is already taken
    if username in names:
        return -1
    #If the username is available
    else:
        #Add the name to the list of taken names (as it will be taken in the next few lines)
        names.append(username)
        #Update the list of taken name
        takenNames.update_one({"list" : copy}, {"$set" : {"list" : names}})

    #Pulls the next available ID number
    cur = list(ids.find({}))[0]["current"]
    #Generates a random salt to be applied to the player's profile
    mySalt = salt()
    #Creates an entry on the private side
    #["id", "username", "salt", "password"]
    privatePlayers.insert_one({"id" : cur, "username": username, "salt" : mySalt, "password" : hash(password + "Q" + mySalt)})
    #Creates an entry on the public side that anyone can access
    #["id", "username", "wins", "monies"]
    publicPlayers.insert_one({"id":cur, "username" : username, "wins" : 0, "monies" : 0})
    #Pulls the newly created record to return from the database (has AIDS _id)
    player = list(publicPlayers.find({"id" : cur}))[0]
    #Updates the ID to the next value
    ids.update_one({"current" : cur}, {"$set" : {"current" : cur+1}})
    #Returns the newly created entry without AIDS _id
    return sanitize(player)

#Returns True if the account is deleted
#Returns False if the account does not exist or if the credentials are incorrect
def delAccount(username, password):
    if login(username, password):
        entry = list(privatePlayers.find({"username":username}))[0]
        #Permanently delete (no bullshit soft delete)
        privatePlayers.delete_one({"id" : entry["id"]})
        publicPlayers.delete_one({"id" : entry["id"]})
        return True
    else:
        return False

#Takes in a username of a person who just won a game, and their balance that they had for their win
#This will update their public profile's win count and balance
def win(username, balance):
    entry = list(publicPlayers.find({"username" : username}))[0]
    entry = sanitize(entry)
    bal = entry["monies"] + balance
    wins = entry["wins"] + 1
    publicPlayers.update_one({"id" : entry["id"]}, {"$set" : {"monies" : bal}}) 
    publicPlayers.update_one({"id" : entry["id"]}, {"$set" : {"wins" : wins}})