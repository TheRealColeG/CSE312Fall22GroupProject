import csv
#Use this as elements for board piece objects in the 1d array of the gameboard.
class Property: 

	#The method to initalize a Property object.
	#Input: (name, baseCost, mortgagePrice, houseCost, (houseRent[0], houseRent[1], houseRent[2], houseRent[3], houseRent[4], houseRent[5]), propertyOwner, houseCount, occupying)
	def __init__(self, title, cost, mortgage, house, rents, owner, houses, occupied):

		#Property name. (String).
		self.name = title 
		#Amount to buy outright. (Float).
		self.baseCost = cost
		#The username of the current property owner. Set to None by default until bought. (String).
		self.propertyOwner = owner
		#The current number of houses on the property (0-5).
		self.houseCount = houses
		#The equity. The amount to halfway sell your house and amount to buy it back to the market. (Float).
		self.mortgagePrice = mortgage
		#The amount it takes to buy ONE house or ONE hotel. A property must have 4 houses in order to buy 1 hotel. (Float).
		self.houseCost = house
		#The amount a house can take in rent per number of houses on the property. All houses have 0 by default and 5 if there is a hotel. (Int)(0-5).
		self.houseRent = rents
		#A list of player usernames that are occupying the space at the current time.
		self.occupying = occupied
	
	#Translates indices on the csv property details file to indices on the game board 1d array
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
	for i in range(40):
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
						ret_val[index] = Property(property[0], float(property[1]), float(property[2]), float(property[3]), (float(property[4]), float(property[5]), float(property[6]), float(property[7]), float(property[8]), float(property[9])), None, 0, 0)
		#If the iteration is not supposed to be a property
		elif i == 0 or i == 2 or i == 4 or i == 5 or i == 7 or i == 10 or i == 12 or i == 15 or i == 17 or i == 20 or i == 22 or i == 25 or i == 28 or i == 30 or i == 33 or i == 35 or i ==- 36 or i == 38:
			#If the property is GO
			if i == 0:
				ret_val[i] = Property("GO", None, None, None, 0, 0, None, 0)
			#If the property is the JAIL
			elif i == 10:
				ret_val[i] = Property("JAIL", None, None, None, 0, 0, None, 0)
			#If the property is FREE PARKING
			elif i == 20:
				ret_val[i] = Property("FREE PARKING", None, None, None, 0, 0, None,0)
			#If the POLICE have caught player
			elif i == 30:
				ret_val[i] = Property("ARREST", None, None, None, 0, 0, None, 0)
			#If the piece is a blank slate
			else:
				ret_val[i] = Property("BLANK", None, None, None, 0, 0, None, 0)
	#ret_val is now a starter monopoly board
	return ret_val



#Class startCell:
 

class BoardGame:
	def __init__(self, players):
		#Starter Monopoly
		self.board = initBoard()
		#self.board.append(Property(“name”, 20, 2, 50, (5, 10, 15, 20)))
		#self.board.append(Property(“name”, 20, 2, 50, (5, 10, 15, 20)))
		#self.board.append(Property(“name”, 20, 2, 50, (5, 10, 15, 20)))


#=> BroadGame.board = [Property(...,...,..), Property(...,...,..), Property(...,...,..), Property(...,...,..)]
