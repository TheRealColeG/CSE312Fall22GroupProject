import csv

#This initializes a player dictionary (object)
def initPlayer(username, orientation):
	player = {}
	#The username (str) will be whatever is passed into it
	player["username"] = username
	#The player's orientation in the game (1-4)
	player["order"] = orientation
	#Their balance #???
	player["money"] = 0.0
	#The list of owned properties
	player["properties"] = []
	#The index of the location where they reside in the board
	player["location"] = 0
	return player

def setPlayer(username, order, money, properties, location):
	player = {}
	player["username"] = username
	player["order"] = order
	player["money"] = money
	player["properties"] = properties
	player["location"] = location
	return player

#This kicks a player out of the game
def bankruptPlayer(player):
	#The username of every bankrupted player is "INDEBTED INMATE"
	player["username"] = "INDEBTED INMATE"
	#Their balance/location is set to none (you can use these to check to see if they are out of the game)
	player["money"] = None
	player["properties"] = []
	player["location"] = 10
	return player

#Initializes the property based on what is passed
def initProperty(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged):
	property = {}
	property["name"] = title
	property["baseCost"] = cost
	property["mortgagePrice"] = mortgage
	property["houseCost"] = house
	property["houseRent"] = rents
	property["currentOwner"] = owner
	property["houseCount"] = houses
	property["occupying"] = occupied
	property["mortgageStatus"] = mortgaged

	#(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
	#ret_val[i] = initProperty("FREE PARKING", None, None, None, 0, 0, None, 0, None)
	return property

#Changes the ownership of the property when it is bought
def buyProperty(property, player):
	#Changes the current owner to the player who was passed
	property["currentOwner"] = player["username"]
	#Just in case the property is bought while mortgaged or with houses
	property["mortgageStatus"] = False
	property["houseCount"] = 0
	return property

#Reverses the mortgage status of a property when called
def mortgageProperty(property):
	property["mortgageStatus"] = not property["mortgageStatus"]
	return property

#If the turn is moved to the next player, change the game's built in turn indicator
def changeTurn(game, turn, playerCount):
	#If the turn is 4 and there are 4 players, set it to 1. For any dynamic playercount
	if turn == playerCount:
		game["status"] = (1, game["status"][1])
	else:
		game["status"] = (game["status"][0]+1, game["status"][1])
	return game

def initGame(usernames):
	game = {}
	#Initializes the monopoly board
	game["board"] = initBoard()
	#This will be a list of player objects in the order of their gameplay.
	players = []
	i = 1
	#For every username in the list, create and add the player objects
	for username in usernames:
		players.append(initPlayer(username, i))
		i = i + 1
	game["players"] = players
	#Adds the players to the GO space.
	occupyList = []
	for player in players:
		occupyList.append(player["username"])
	game["board"][0]["occupying"] = occupyList
	#A list of player dictionaries that have been kicked out of the game due to bankruptcy (No one because everybody starts with money).
	game["bankrupted"] = []
	#Set the game status to "Roll", requiring the current orientation to be rolling the dice.
	game["status"] = (1, "Roll")
	#Sends the created Game object straight to the database to be implemented in the 'games' collection
	return game

def passGo(player):
	player["money"] = player["money"] + 200.00
	return player

#Called on a GAME to bankrupt the username
def bankrupt(game, player):
	#Pulls the username to examine
	playerUsername = player["username"]
	i = 0
	for playerDictionary in game["players"]:
		if playerDictionary["username"] == playerUsername:
			#Set the game["playeres"] to a bankrupted player
			game["players"][i] = bankruptPlayer(playerDictionary)
			#Append the game's bankruptcy list with the bankrupted player
			game["bankrupted"] = game["bankrupted"].append(playerDictionary)
			break
		i = i + 1

	#Get the indices of all the owned property from that player
	indices = []
	for i in range(len(game["board"])):
		if game["board"][i]["currentOwner"] == player["username"]:
			indices.append(i)

	touchBoard = game["board"]
	#For the index of all the board pieces he owns
	for i in indices:
		#Set the current owner to None
		touchBoard[i]["currentOwner"] = None
		#Un-mortgage every property
		touchBoard[i]["mortgageStatus"] = False
		#Knock the housecount to 0
		touchBoard[i]["houseCount"] = 0

	#Set the game's board to the changed board
	game["board"] = touchBoard
	#???
	return game

#Input is a game dictionary, player dictionary and roll (int)
def move(game, player, roll):
	currentBoard = game["board"]
	currentLocation = player["location"]
	newLocation = currentLocation + roll
	#If the player passed GO
	if newLocation > 39:
		overflow = newLocation - 40
		newLocation = overflow
		#Give 'em $200
		player = passGo(player)
	#The property dictionary that the player has landed on
	lodging = currentBoard[newLocation]
	#If the property is a buyable asset
	if lodging["baseCost"] != None:
		#Move the character and send the choice to 
		curOccupying = currentBoard[currentLocation]["occupying"]
		res = []
		if len(curOccupying) > 0:
			for occupier in curOccupying:
				if occupier != player["username"]:
					res.append(occupier)
		currentBoard[currentLocation]["occupying"] = res
		#
		newOccupying = currentBoard[newLocation]["occupying"]
		res = []
		if len(newOccupying) > 0:
			for occupier in newOccupying:
				res.append(occupier)
		res.append(player["username"])
		currentBoard[newLocation]["occupying"] = res

		player["location"] = newLocation
		
		#If the property is owned
		if currentBoard[newLocation]["currentOwner"] != None:
			game = rent(game, player, currentBoard[newLocation])
			game = changeTurn(game, player["order"], len(game["players"]))
		#If the property is not owned
		else:
			#Drop the choice to the user
			game["status"] = (game["status"][0], "Choice")
		#
	#If the property is a blank slate
	else:
		if lodging["name"] == "BLANK" or lodging["name"] == "GO" or lodging["name"] == "FREE PARKING" or lodging["name"] == "JAIL":
			#currentBoard[currentLocation] = playerExitProperty(currentBoard[currentLocation], player)
			#currentBoard[newLocation] = playerEnterProperty(currentBoard[newLocation], player)


			curOccupying = currentBoard[currentLocation]["occupying"]
			res = []
			if len(curOccupying) > 0:
				for occupier in curOccupying:
					if occupier != player["username"]:
						res.append(occupier)
			currentBoard[currentLocation]["occupying"] = res
			#
			newOccupying = currentBoard[newLocation]["occupying"]
			res = []
			if len(newOccupying) > 0:
				for occupier in newOccupying:
					res.append(occupier)
			res.append(player["username"])
			currentBoard[newLocation]["occupying"] = res


			player["location"] = newLocation
			#Move the turn on
			game = changeTurn(game, player["order"], len(game["players"]))
		else:
			raise Exception("!!! PROPERTY ISSUE !!!")
	game["board"] = currentBoard
	return game

#move around the money
def rent(game, player, property):
	players = game["players"]
	currentOwner = property["currentOwner"]
	payeeIndex = -1
	ownerIndex = -1
	rent = property["houseRent"][property["houseCount"]]
	for i in range(len(players)):
		if players[i] == player:
			payeeIndex = i
		if players[i]["username"] == currentOwner:
			ownerIndex = i
	if ownerIndex != payeeIndex:
		curOwner = players[ownerIndex]
		players[ownerIndex] = setPlayer(curOwner["username"], curOwner["order"], curOwner["money"] + rent, curOwner["properties"], curOwner["location"])
		curRenter = players[payeeIndex]
		players[payeeIndex] = setPlayer(curRenter["username"], curRenter["order"], curRenter["money"] - rent, curRenter["properties"], curRenter["location"])
		if players[payeeIndex]["money"] < 0:
			game = bankrupt(game, player)
	game["players"] = players
	game["status"] = (game["status"][0], "Roll") 
	game = changeTurn(game, player["order"], len(game["players"]))
	return game

#Translates indices on the csv property details file to indices on the game board 1D array
#LITERALLY DONT WORRY ABOUT THIS. If this is touched I will eat your face.
def translate(i):
	if i == 1:
		return i + 2
	elif i == 3:
		return i + 3
	elif i == 6:
		return i + 2
	elif i == 8:
		return i + 1
	elif i == 9:
		return i + 2
	elif i == 11:
		return i + 2
	elif i == 13:
		return i + 1
	elif i == 14:
		return i + 2
	elif i == 16:
		return i + 2
	elif i == 18:
		return i + 1
	elif i == 19:
		return i + 2
	elif i == 21:
		return i + 2
	elif i == 23:
		return i + 1
	elif i == 24:
		return i + 2
	elif i == 26:
		return i + 1
	elif i == 27:
		return i + 2
	elif i == 29:
		return i + 2
	elif i == 31:
		return i + 1
	elif i == 32:
		return i + 2
	elif i == 34:
		return i + 3
	elif i == 37:
		return i + 2
	return 0

#Returns a board with the set in stone properties.

def initBoard():
	#A 1D List is contained with each element being a Property. Index 0 points to Go, index 10 points to JAIL, index 20 points to FREE PARKING, index 30 point to ARREST.
	ret_val = []

	#Set the list to the appropriate size, (remove if we initialize a 40-slot Array beforehand).
	for _ in range(40):
		ret_val.append(0)
	
	#For every index 0-39 of the 1D array, this will set the property object.
	for i in range(40):
		#[0   0    0    0    0    0   ...    0]
		#If the iteration is on the first property it will fill in all the property elements immediately because there will be 20/22.
		if i == 1:
			#Open the csv file and read from there.
			with open('monopoly/properties.csv', mode='r') as file:
				properties = csv.reader(file)
				#1 is the first index of hte first monopoly property.
				index = 0
				#For every property
				for property in properties:
					#If there IS a next index, map the element to a newly created property object having the attributes in that csv file.
					if index != 0:
						#(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
						ret_val[index] = initProperty(str(property[0]), float(property[1]), float(property[2]), float(property[3]), (float(property[4]), float(property[5]), float(property[6]), float(property[7]), float(property[8]), float(property[9])), None, 0, [], False)
						index = translate(index)
					else:
						index = 1
					#This maps a board array index to the NEXT board array index which points to the NEXT property piece.
					
		#If the iteration is not supposed to be a property
		elif i == 0 or i == 2 or i == 4 or i == 5 or i == 7 or i == 10 or i == 12 or i == 15 or i == 17 or i == 20 or i == 22 or i == 25 or i == 28 or i == 30 or i == 33 or i == 35 or i == 36 or i == 38:
			#If the property is GO
			if i == 0:
				#(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
				ret_val[i] = initProperty("GO", None, None, None, 0, None, None, [], None)
			#If the property is the JAIL
			elif i == 10:
				#(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
				ret_val[i] = initProperty("JAIL", None, None, None, 0, 0, None, [], None)
			#If the property is FREE PARKING
			elif i == 20:
				#(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
				ret_val[i] = initProperty("FREE PARKING", None, None, None, 0, 0, None, [], None)
			#If the POLICE have caught player
			elif i == 30:
				#(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
				ret_val[i] = initProperty("ARREST", None, None, None, 0, 0, None, [], None)
			#If the piece is a blank slate
			else:
				#(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
				ret_val[i] = initProperty("BLANK", None, None, None, 0, 0, None, [], None)
				#initProperty(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
	#ret_val is now a starter monopoly board
	return ret_val