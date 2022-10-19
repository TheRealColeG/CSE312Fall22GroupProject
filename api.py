import csv
import random
import database

#This initializes a player dictionary
#Each game has a list of Player objects and a Board objects which is a list of Properties
def initPlayer(username, orientation):
	player = {}
	player["username"] = username
	player["order"] = orientation
	player["money"] = 0.0
	player["properties"] = []
	player["location"] = 0
	return player

def bankruptPlayer(player):
	player["username"] = "INDEBTED INMATE"
	player["money"] = None
	player["location"] = None
	return player
ajopisjdehptioasdet
def initProperty(title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged):
	property = {}
	property["name"] = title
	property["baseCost"] = cost
	property["mortgagePrice"] = mortgage
	property["houseCost"] = house
	property["houseRent"] = rents
	property["occupying"] = occupied
	property["mortgageStatus"] = mortgaged
	property["currentOwner"] = owner
	property["houseCount"] = houses

def buyProperty(property, player):
	#self.propertyOwner = player.name
	#Just in case the property is bought while mortgaged or with houses
	#self.mortgageStatus = False
	#self.houseCount = 0
	NotImplemented

def playerEnterProperty(property, player):
	if player["username"] not in property["occupying"]:
		property["occupying"] = property["occupying"].append(player["username"])
	else:
		print("FUCKUP!!! playerEnterProperty() was ran on a property already containing that player!", flush=True)

def playerExitProperty(property, player):
	if player["username"] in property["occupying"]:
		property["occupying"] = property["occupying"].remove(player["username"])
	else:
		print("FUCKUP!!! playerExitProperty() was ran on a property not containing that player!", flush=True)

def mortgageProperty(property):
	property["mortgageStatus"] = not property["mortgageStatus"]
	

#The game object is what is stored in the database. The games Collection will hold these objects
class Game:
	def __init__(self, usernames, lobby):
		#Initializes the monopoly board.
		self.board = initBoard()
		#This will be a list of player objects in the order of their gameplay.
		self.players = []
		i = 0
		#For every username in the list, add the player objects
		for username in usernames:
			#Create a new player object (with the order (1-4) being the order of the game).
			player = Player(username, i+1)
			self.players.append(player)
			i = i + 1
		#Adds the players to the GO space.
		for player in self.players:
			self.board[0].playerEnter(player)

		#A list of player objects that have been kicked out of the game due to bankruptcy (No one because everybody starts with money).
		self.bankrupted = []
		#Sends the created Game object straight to the database to be implemented in the 'games' collection
		database.setGame(lobby, self)
		
	def bankrupt(self, player):
		player.bankruptPlayer()
		self.bankrupted.append(player)

	def move(self, player, roll):
		currentBoard = self.board
		



#Translates indices on the csv property details file to indices on the game board 1D array
#LITERALLY DONT WORRY ABOUT THIS
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
		#If the iteration is on the first property it will fill in all the property elements immediately because there will be 20/22.
		if i == 1:
			#Open the csv file and read from there.
			with open('properties.csv', mode='r') as file:
				properties = csv.reader(file)
				#1 is the first index of hte first monopoly property.
				index = 1
				#For every property
				for property in properties:
					#This maps a board array index to the NEXT board array index which points to the NEXT property piece.
					index = translate(index)
					#If there IS a next index, map the element to a newly created property object having the attributes in that csv file.
					if index != 0:
						#(self, title, cost, mortgage, house, rents, owner, houses, occupied, mortgaged)
						ret_val[index] = initProperty(property[0], float(property[1]), float(property[2]), float(property[3]), (float(property[4]), float(property[5]), float(property[6]), float(property[7]), float(property[8]), float(property[9])), None, 0, [], False)
		#If the iteration is not supposed to be a property
		elif i == 0 or i == 2 or i == 4 or i == 5 or i == 7 or i == 10 or i == 12 or i == 15 or i == 17 or i == 20 or i == 22 or i == 25 or i == 28 or i == 30 or i == 33 or i == 35 or i == 36 or i == 38:
			#If the property is GO
			if i == 0:
				ret_val[i] = initProperty("GO", None, None, None, 0, None, None, 0, None)
			#If the property is the JAIL
			elif i == 10:
				ret_val[i] = initProperty("JAIL", None, None, None, 0, 0, None, 0, None)
			#If the property is FREE PARKING
			elif i == 20:
				ret_val[i] = initProperty("FREE PARKING", None, None, None, 0, 0, None, 0, None)
			#If the POLICE have caught player
			elif i == 30:
				ret_val[i] = initProperty("ARREST", None, None, None, 0, 0, None, 0, None)
			#If the piece is a blank slate
			else:
				ret_val[i] = initProperty("BLANK", None, None, None, 0, 0, None, 0, None, None)
	#ret_val is now a starter monopoly board
	return ret_val

def diceRoll():
	#The list of possible die roll
	support = "123456"
	#Choose two die outcomes. (This ensures rolling a 7 still remains higher probability than a 12)
	firstRoll = int(random.choice(support))
	secondRoll = int(random.choice(support))

	return (firstRoll, secondRoll)