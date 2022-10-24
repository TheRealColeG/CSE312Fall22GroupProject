#Something to execute HTML templating. May be replaced/better utilized by WebSockets
#Develop this if you have a lot of time for blank mindedly coding (slightly elementary and artistic)


#Write the HTML of the player's info taking in the statistics and forming the HTML from it.
#This can be done wayyyy down the road.
#Should return the HTML template (string) to be encoded and served by the server.
def writeAccountHTML(username, wins, monies):
    NotImplemented

#Serve the HTML for the "Create Account" screen. 
#SHOULD take in no parameters but we'll see.
#Should return the HTML template (string) to be encoded and served by the server.
def writeCreateAccountHTML():
    NotImplemented

#Poster HTML board. Very simple.
#Should return the HTML template (string) to be encoded and served by the server.
def writeAccountCreatedHTML():
    NotImplemented

#The gorgeous bloviating home screen of the website. This would be a prime place to put some images or even videos and certainly a logo or two with all our buttons.
#NOT WHILE LOGGED IN!!! NEW USERS ONLY!!!
#Should return the large HTML template (string) with images/logos to be encoded and served by the server.
def writeLoginScreenHTML():
    NotImplemented

#Home screen of logged in users. Should get right down to the point with little bloviation and certainly no ads. Logos are fine.
#ONLY AFTER LOGIN! Maybe integrate a token or two here. Must have logged in.
#Should return the large HTML template (string) with images/logos to be encoded and served by the server.
def writeHomeScreenHTML():
    NotImplemented