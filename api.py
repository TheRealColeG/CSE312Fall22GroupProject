Class Property:
name,
	baseCost, 
baseRent, 
houseCost, 
houseRent

Class startCell:
 

Class BoardGame:
	Def init(self, players):
		Self.board = []
		self.board.append(Property(“name”, 20, 2, 50, (5, 10, 15, 20)))
		self.board.append(Property(“name”, 20, 2, 50, (5, 10, 15, 20)))
		self.board.append(Property(“name”, 20, 2, 50, (5, 10, 15, 20)))


=> BroadGame.board = [Property(...,...,..), Property(...,...,..), Property(...,...,..), Property(...,...,..)]
