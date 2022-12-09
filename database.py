import random
from pymongo import MongoClient
import hashlib

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
#Valid authentication cookies for the users (64 bytes each). Don't let this become too large a file if lots of people use the website
authCookies = db["auth-cookies"]
#Valid XSRF tokens for the useres (16/32 bytes each)
xsrfTokens = db["xsrf-tokens"]
#Reflects the status of the database (What can be touched/pulled?)
status = db["status"]

#Initially no players exist
if "status" not in db.list_collection_names():
    status.insert_one({"status" : False})

# Testing 
active_users = {}
list_of_players = [] 

#If there are no accounts created
if "names" not in db.list_collection_names():
    takenNames.insert_one({"names" : []})

#If no games are in progress, set the lobbies to 0 (nothing)
if "games" not in db.list_collection_names():
    games.insert_one({"id" : 1, "contents" : 0})
    games.insert_one({"id" : 2, "contents" : 0})
    games.insert_one({"id" : 3, "contents" : 0})
    games.insert_one({"id" : 4, "contents" : 0})
    games.insert_one({"id" : 5, "contents" : 0})
    games.insert_one({"id" : 6, "contents" : 0})
    games.insert_one({"id" : 7, "contents" : 0})
    games.insert_one({"id" : 8, "contents" : 0})

#If no entries have been created yet, set the first available ID to 0
if "identification" not in db.list_collection_names():
    ids.insert_one({"current" : 0})

#Returns true if accounts exist, false otherwise.
def pullStatus():
    return sanitize(list(status.find({}))[0])["status"]

def murder():
    db.dropDatabase()

#Sanitizes a LIST of dictionaries, removing the aids mongo _id from everything
def process(diseaseBoat):
    #If there ain't shit to process, return nothing
    if diseaseBoat == []:
        return diseaseBoat
    else:
        #Return a list of sanitized dictionaries
        cleanShip = []
        for diseased in diseaseBoat:
            clean = sanitize(diseased)
            cleanShip.append(clean)
        return cleanShip

#Deletes the stupid AIDS Mongo _id from ANY ONE dictionary
def sanitize(diseased):
    cured = {}
    for key in diseased.keys():
        if key != "_id":
            cured[key] = diseased[key]
    return cured

#Returns True if the username and password correspond to an entry on file
def authAccount(username, password):
    #Pulls the entry with the username
    existing = list(privatePlayers.find({"username" : username}))
    #If there is no such entry at that username
    if existing == []:
        return False
    #If an entry exists, pull the sanitized account
    account = sanitize(existing[0])
    #Hash the password-salt combo and see if it matches what is on file
    hidden = hashlib.sha256((password+account["salt"]).encode()).hexdigest()
    #If it matches, return True, authenticating the account
    if hidden == account["password"]:
        # ??? Return a token cookie?
        return True
    #If it does not match, return False as the credentials do not authenticate.
    else:
        return False

#Returns a randomized salt i characters long.
def salt(i):
    fullList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    chars = []
    for _ in range(i):
        chars.append(random.choice(fullList))
    salt = ""
    for char in chars:
        salt = salt + char
    return salt

#If the username is available, it will create a new player character and return the sanitized dictionary
#If not, it will return -1
def newAccount(username, password):
    status.update_one({"status" : False}, {"$set" : {"status" : True}})
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
        takenNames.update_one({"names" : copy}, {"$set" : {"names" : names}})
    #Pulls the next available ID number
    cur = list(ids.find({}))[0]["current"]
    #Generates a random salt to be applied to the player's profile
    mySalt = salt(16)
    #Creates an entry on the private side
    #["id", "username", "salt", "password"]
    privatePlayers.insert_one({"id" : cur, "username": username, "salt" : mySalt, "password" : hashlib.sha256((password + mySalt).encode('utf-8')).hexdigest()})
    #Creates an entry on the public side that anyone can access
    #["id", "username", "wins", "monies"]
    publicPlayers.insert_one({"id" : cur, "username" : username, "wins" : 0, "monies" : 0.0})
    #Pulls the newly created record to return from the database
    player = sanitize(list(publicPlayers.find({"id" : cur}))[0])
    #Updates the ID to the next value
    ids.update_one({"current" : cur}, {"$set" : {"current" : cur+1}})
    #Returns the newly created entry without AIDS _id
    return player

#Returns True if the account is deleted
#Returns False if the account does not exist or if the credentials are incorrect
def delAccount(username, password):
    #If the username and password correspond to an acount
    if authAccount(username, password):
        entry = list(privatePlayers.find({"username":username}))[0]
        #Permanently delete (no bullshit soft delete)
        privatePlayers.delete_one({"id" : entry["id"]})
        publicPlayers.delete_one({"id" : entry["id"]})
        return True
    #If the username and password do not correspond to an account
    else:
        return False

#Takes in a username of a person who just won a game, and their balance that they had for their win
#This will update their public profile's win count and balance
def winGame(username, balance):
    #Pull the entry with the matching username
    entry = sanitize(list(publicPlayers.find({"username" : username}))[0])
    #Update their winning balance with what they won with
    bal = entry["monies"] + balance
    #Update the win count
    wins = entry["wins"] + 1
    #Push both to the database
    publicPlayers.update_one({"id" : entry["id"]}, {"$set" : {"monies" : bal}}) 
    publicPlayers.update_one({"id" : entry["id"]}, {"$set" : {"wins" : wins}})

#Pulls the public information for a username in the form of a dictionary with the details
#Returns a -1 if no username exists
def playerDetails(username):
    entry = list(publicPlayers.find({"username" : username}))
    if entry == []:
        return -1
    else: 
        return sanitize(entry[0])

#Changes the password (with a new salt)
#Returns true if the username & password correspond to an account
#Returns false if they do not
def changePassword(username, password, newPassword):
    #If the username and password correspond to an account
    print("From database: the username is: "+str(username), flush=True)
    if authAccount(username, password):
        print("Account authenticated with current login info in database.py", flush=True)
        #Pull the entry for that username
        entry = list(privatePlayers.find({"username" : username}))[0]
        entry = sanitize(entry)
        #Generate a new salt to go along with the new password
        newSalt = salt(16)
        #Update the file with the new salt
        privatePlayers.update_one({"id" : entry["id"]}, {"$set" : {"salt" : newSalt}})
        #Hash the password along with the new salt
        newPassword = hashlib.sha256((newPassword+newSalt).encode('utf-8')).hexdigest()
        #Change the password
        privatePlayers.update_one({"id" : entry["id"]}, {"$set" : {"password" : newPassword}})
        return True
    else:
        return False

#Returns a number 1-8 if there is a lobby available
#Return -1 if all the games are full
def findAvailableGame():
    #Pull a snapshot of the current lobbies
    lobbies = list(games.find({}))
    #For every lobby see if it is available
    for lobby in lobbies:
        #Pull the keys (should be '1-8' or AIDS _id)
        lobby = sanitize(lobby)
        if lobby["contents"] == 0:
            return lobby["id"]
    #If no lobby has a "contents" of 0, return -1 to indicate all games are full.
    return -1

#Set the value of a lobby's game contents to the updated content/game
def setGame(lobby, game):
    games.update_one({"id" : lobby}, {"$set" : {"contents" : game}})

#Reverts a game to being ended in the database
def endGame(lobby):
    games.update_one({"id" : lobby}, {"$set" : {"contents" : 0}})

#Pulls the game dictionary from the lobby
def pullGame(lobby):
    lobbies = [1,2,3,4,5,6,7,8]
    if lobby not in lobbies:
        raise Exception("Lobby pulled that does not exist.")
    game = list(games.find({"id" : lobby}))
    game = sanitize(game[0])
    game = game["contents"]
    #Send this to the printer
    return game

#This creates and serves a brand new authentication XSRF token for a player's username
#Not at all stored on their player entries.
def genAuthCookie(username):
    #The cookie that will be assigned to the player's browser
    cookie = salt(64)
    #Inserts the just created cookie into the authCookies collection with its corresponding username
    authCookies.insert_one({"username" : username, "cookie" : hashlib.sha256(cookie.encode('utf-8')).hexdigest()})
    #Return the authenticated plaintext cookie
    return cookie

#Returns a True if the authentication XSRF cookie is authenticated, a False if it is not.
def authAuthCookie(cookie):
    retrieveCookie = list(authCookies.find({"cookie" : hashlib.sha256(cookie.encode('utf-8')).hexdigest()}))
    #If there is not existing cookie by that id:
    if retrieveCookie == []:
        #Return false as the authentication failed.
        return False
    #Return the username associated with the cookie
    return sanitize(retrieveCookie[0])["username"]

#Return True if the cookie was deleted, return False otherwise
def delAuthCookie(cookie):
    #If the ID and the cookie match:
    if authAuthCookie(cookie) == False:
        return False
    authCookies.delete_one({"cookie" : hashlib.sha256(cookie.encode('utf-8')).hexdigest()})
    return True

#Generate an XSRF token, put it in the database along with the username and return the token
def genXSRFToken(username):
    #Generate a 32-length token
    token = salt(32)
    #Store the xsrf token along with the username
    xsrfTokens.insert_one({"username" : username, "token" : token})
    #Pull the token
    pullToken = list(xsrfTokens.find({"token" : token}))
    if pullToken == []:
        raise Exception("Database error in genXSRFToken")
    #Return the newly created/pulled token 
    return sanitize(pullToken[0])["token"]

#Check to see if there are any xsrf tokens assigned to a username
def touchXSRFToken(username):
    #Pull all associated with the username
    query = list(xsrfTokens.find({"username" : username}))
    #If there are none, return -1
    if query == []:
        return -1
    #If one exists, return the token
    return sanitize(query[0])["token"]

#Try and authenticate the token with the username  and plaintext token
def authXSRFToken(username, token):
    #Pull any and all entries by that token
    query = list(xsrfTokens.find({"token" : token}))
    #If none exist, return False
    if query == []:
        return False
    #If one exists, pull the username
    name = sanitize(query[0])["username"]
    #If the usernames match, return True
    if name == username:
        return True
    #Otherwise, deny the authentication.
    return False

#Delete any xsrf tokens associated with a username
def delXSRFToken(username):
    tokens = list(xsrfTokens.find({"username" : username}))
    #If there are no tokens associated iwth a username, return False as no deletion occured
    if tokens == []:
        return False
    #Remove the _aids id
    tokens = process(tokens)
    #For every token associated with the username
    for token in tokens:
        #Delete the token
        xsrfTokens.delete_one({"token" : token["token"]})
    #Return true as deletion occured.
    return True

#Returns win rank for the username
def rankByWins(username):
    #Pulls the user profile for that username
    userProfile = list(publicPlayers.find({"username" : username}))
    #If there is no profile by that name, return -1 indicating an error.
    if userProfile == []:
        return -1
    userProfile = sanitize(userProfile[0])
    #Otherwise, pull all profiles and process them, removing the aids _id in the process
    allProfiles = process(list(publicPlayers.find({})))
    #Initialize a "Set" containing one value for the number of game wins for every user in the database.
    winRanking = [0]
    #For every profile, add the win count into the win ranking "Set"
    for profile in allProfiles:
        if profile["wins"] not in winRanking:
            winRanking.append(profile["wins"])
    #Sort the "Set" in decreasing order so that the highest win count is at winRanking[0]
    winRanking.sort()
    winRanking.reverse()
    #For every index in the winranking
    for i in range(len(winRanking)):
        #Check to see if the win count of the user matches the iterated win count
        if winRanking[i] == userProfile["wins"]:
        #If it does, return the index+1 to indicate the rank being 1 at index 0 and so on
            return i+1
    #This should never run because userProfile is in allProfiles. If it does, raise an exception.
    raise Exception("database error!")

#Returns money rank for the username
def rankByCash(username):
    #Pulls the user profile for that username
    userProfile = list(publicPlayers.find({"username" : username}))
    #If there is no profile by that name, return -1 indicating an error.
    if userProfile == []:
        return -1
    userProfile = sanitize(userProfile[0])
    #Otherwise, pull all profiles and process them, removing the aids _id in the process
    allProfiles = process(list(publicPlayers.find({})))
    #Initialize a "Set" containing one value for the money for every user in the database.
    moneyRanking = [0.0]
    #For every profile, add the balance into the money ranking "Set"
    for profile in allProfiles:
        if profile["monies"] not in moneyRanking:
            moneyRanking.append(profile["monies"])
    #Sort the "Set" in decreasing order so that the highest money count is at moneyRanking[0]
    moneyRanking.sort()
    moneyRanking.reverse()
    #For every index in the moneyRanking
    for i in range(len(moneyRanking)):
        #Check to see if the money count of the user matches the iterated balance count
        if moneyRanking[i] == userProfile["monies"]:
        #If it does, return the index+1 to indicate the rank being 1 at index 0 and so on
            return i+1
    #This should never run because userProfile is in allProfiles. If it does, raise an exception.
    raise Exception("database error!")

def pullWinsLeaderboard():
    #Pull and sanitize every public profile
    allProfiles = process(list(publicPlayers.find({}))) 
    #If there are no profiles, return -1 as an error indicator
    if allProfiles == []:
        return -1
    #Initialize a dict that will pair a win number to a LIST of INDICES of players that have that (key) win count
    ranking = {}
    #For every profile index in all profiles
    for i in range(len(allProfiles)):
        #Pull the actual profile
        profile = allProfiles[i]
        #If that profile's win count is already in the ranking
        if profile["wins"] in list(ranking.keys()):
            #Append the index of the profile to the list of profiles that have the (key) win count
            li = ranking[profile["wins"]]
            res = []
            for entry in li:
                res.append(entry)
            res.append(i)
            ranking[profile["wins"]] = res
        #If we are ranking the first profile with that win count (win count is unique so far)
        else:
            #Initialize the list to be solely that index
            ranking[profile["wins"]] = [i]
    #winCounts should be a LIST of all noticed scores
    winCounts = list(ranking.keys())
    #Sort the list of scores in reverse order so that the greatest win count is at index 0 (if a greatest win count exists)
    winCounts.sort()
    winCounts.reverse()
    #Initialize the leaderboard which will be an ordered list of usernames
    leaderboard = []
    #For every win score
    for key in winCounts:
        #Pull the list of indices in the allProfiles list of dicts that have that score
        valList = ranking[key]
        #For every index of a user with that score
        for index in valList:
            #Append the username into the leaderboard (tied scores should have random-ish order)
            curProfile = allProfiles[index]
            leaderboard.append(curProfile["username"])
    #Return the ordered list
    return leaderboard

def pullBalLeaderboard():
    #Pull and sanitize every public profile
    allProfiles = process(list(publicPlayers.find({}))) 
    #If there are no profiles, return -1 as an error indicator
    if allProfiles == []:
        return -1
    #Initialize a dict that will pair a win number to a LIST of INDICES of players that have that (key) balance
    ranking = {}
    #For every profile index in all profiles
    for i in range(len(allProfiles)):
        #Pull the actual profile
        profile = allProfiles[i]
        #If that profile's balance is already in the ranking
        if profile["monies"] in list(ranking.keys()):
            #Append the index of the profile to the list of profiles that have the (key) balance
            li = ranking[profile["monies"]]
            res = []
            for entry in li:
                res.append(entry)
            res.append(i)
            ranking[profile["monies"]] = res
        #If we are ranking the first profile with that balance (the balance is unique so far)
        else:
            #Initialize the list to be solely that index
            ranking[profile["monies"]] = [i]
    #balances should be a LIST of all noticed scores
    balances = list(ranking.keys())
    #Sort the list of balances in reverse order so that the greatest balance is at index 0 (if a greatest balance exists)
    balances.sort()
    balances.reverse()
    #Initialize the leaderboard which will be an ordered list of usernames
    leaderboard = []
    #For every balance
    for key in balances:
        #Pull the list of indices in the allProfiles list of dicts that have that balance
        valList = ranking[key]
        #For every index of a user with that balance
        for index in valList:
            #Append the username into the leaderboard (tied balance should have random-ish order)
            curProfile = allProfiles[index]
            leaderboard.append(curProfile["username"])
    #Return the ordered list
    return leaderboard