#import database
from monopoly import api

def computeBoard(board):
    #board = None#database.pullGame(lobby)["board"]
    ret_val = []
    empties = ["ARREST", "FREE PARKING", "JAIL", "GO"]
    for property in board:
        entry = None
        if property["name"] == "BLANK":
            entry = (-1, -1, -1)
        elif property["name"] not in empties:
            entry = (property["name"], property["baseCost"], property["currentOwner"])
        else:
            entry = (property["name"], -1, -1)
        ret_val.append(entry)
    return ret_val

def htmlcreator(properties):
    ret_val = ""
    html = open("cole-code/monopoly.html", 'r')
    for line in html:
        for char in line:
            ret_val = ret_val + str(char)
    html.close

    copy = ret_val
    
    for i in range(len(ret_val)):
        if ret_val[i] == '{' and i != 0 and (ret_val[i] == ret_val[i-1]):
            j = i + 1
            if ret_val[j+1] == '}':
                index = int(ret_val[j])
            else:
                index = int(ret_val[slice(j, j+2)])
            string = "{"+"{"+str(index)+"}"+"}"
            #(property["name"], property["baseCost"], property["currentOwner"])
            property = properties[index]
            if property[0] == -1:
                copy = copy.replace(string, "")
            elif property[2] == -1:
                copy = copy.replace(string, property[0])
            else:
                copy = copy.replace(string, (str(property[0])+'\n'+str(property[1])+'\n'+str(property[2])))

    for i in range(len(ret_val)):
        if ret_val[i] == '[' and i != 0 and (ret_val[i] == ret_val[i-1]):
            j = i + 1
            if ret_val[j+1] == ']':
                index = int(ret_val[j])
            else:
                index = int(ret_val[slice(j, j+2)])
            string = "["+"["+str(index)+"]"+"]"
            #(property["name"], property["baseCost"], property["currentOwner"])
            property = properties[index]
            if property[0] == -1:
                copy = copy.replace(string, "")
            elif property[2] == -1:
                copy = copy.replace(string, property[0])
            else:
                copy = copy.replace(string, (str(property[0])+'\n'+str(property[1])+'\n'+str(property[2])))
    
    return copy
"""   
#Will return a String containing the html for a user profile under the input username (string)
def servePublicUserProfileHTML(username):
    information = database.playerDetails(username)
    if information == -1:
        return information
    wins = information["wins"]
    balance = information["monies"]
    winRank = database.rankByWins(username)
    balanceRank = database.rankByCash(username)
    s = "s"
    if wins == 1:
        s = ""
    template = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>ALL OR NOTHING</title>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js">\n</script>\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n<body>\n<nav class="navbar navbar-inverse">\n<div class="container-fluid">\n<div class="navbar-header">\n<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n</button>\n<img src="https://i.imgur.com/3Go0b9Z.png" alt="unavailable" style="width:65px;height:50px;">\n</div>\n<div class="collapse navbar-collapse" id="myNavbar">\n<ul class="nav navbar-nav">\n<li class="active"><a href="#">Home</a></li>\n<li><a href="#">Messages</a></li>\n</ul>\n<ul class="nav navbar-nav navbar-right">\n<li><a href="http://localhost:8080/users"><span class="glyphicon glyphicon-user"></span> My Account</a></li>\n</ul>\n</div>\n</div>\n</nav>\n<div class="container text-center">\n<div class="row">\n<div class="col-sm-3 well">\n<div class="well">\n<p><a href="http://localhost:8080/">Welcome to All or Nothing</a></p>\n<p>\nThis is a game closely modeled after the Hasbro board game Monopoly.\nThis is the Final Project for CSE312 at University at Buffalo\nThe Wily 5\n</p>\n</div>\n<div class="alert alert-success fade in">\n<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>\n<p><strong>Who is That Chatting In The Corner?</strong></p>\nGo strike up a conversation and try and make some new friends!\n</div>\n<p><a href="http://localhost:8080/leaderboard">View Leaderboard</a></p>\n<p><a href="http://localhost:8080/login">Login</a></p>\n<p><a href="http://localhost:8080/register">Create Account</a></p>\n</div><div class="col-sm-7">\n<!--Replace this with the score/grades. Kick out avatar unless you want the icon there. Maybe a good spot for the icon of the player if we want to implement it.-->\n<div class="row">\n<div class="col-sm-9">\n<div class="well">\n<h3>All or Nothing is a fast, monopoly-derivative game. The goal is to win the game, but as late as possible in order to rack up as much money in the game.</h3>\n</div>\n<h1>'+str(username)+'</h1>\n<br>\n<h2>'+str(wins)+' Win'+s+'      #'+str(winRank)+'</h2>\n<br>\n<h2>$'+str(balance)+' Balance     #'+str(balanceRank)+'</h2>\n</div>\n</div>\n</div>\n</div>\n</div>\n<footer class="container-fluid text-center">\n<p>Developed by Julius Merlino, Cole Grabenstatter, Buu Lam, Ziqian Yang, Songzhu Li for the Final Project in CSE312 with Dr. Jesse Hartloff</p>\n</footer>\n</body>\n</html>'
    return template

def servePrivateUserProfileHTML(username):
    information = database.playerDetails(username)
    if information == -1:
        return information
    wins = information["wins"]
    balance = information["monies"]
    winRank = database.rankByWins(username)
    balanceRank = database.rankByCash(username)
    s = "s"
    if wins == 1:
        s = ""
    template = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>ALL OR NOTHING</title>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js">\n</script>\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n<body>\n<nav class="navbar navbar-inverse">\n<div class="container-fluid">\n<div class="navbar-header">\n<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n</button>\n<img src="https://i.imgur.com/3Go0b9Z.png" alt="unavailable" style="width:65px;height:50px;">\n</div>\n<div class="collapse navbar-collapse" id="myNavbar">\n<ul class="nav navbar-nav">\n<li class="active"><a href="#">Home</a></li>\n<li><a href="#">Messages</a></li>\n</ul>\n<ul class="nav navbar-nav navbar-right">\n<li><a href="http://localhost:8080/users"><span class="glyphicon glyphicon-user"></span> My Account</a></li>\n</ul>\n</div>\n</div>\n</nav>\n<div class="container text-center">\n<div class="row">\n<div class="col-sm-3 well">\n<div class="well">\n<p><a href="http://localhost:8080/">Welcome to All or Nothing</a></p>\n<p>\nThis is a game closely modeled after the Hasbro board game Monopoly.\nThis is the Final Project for CSE312 at University at Buffalo\nThe Wily 5\n</p>\n</div>\n<div class="alert alert-success fade in">\n<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>\n<p><strong>Who is That Chatting In The Corner?</strong></p>\nGo strike up a conversation and try and make some new friends!\n</div>\n<p><a href="http://localhost:8080/leaderboard">View Leaderboard</a></p>\n<p><a href="http://localhost:8080/login">Login</a></p>\n<p><a href="http://localhost:8080/register">Create Account</a></p>\n</div><div class="col-sm-7">\n<!--Replace this with the score/grades. Kick out avatar unless you want the icon there. Maybe a good spot for the icon of the player if we want to implement it.-->\n<div class="row">\n<div class="col-sm-9">\n<div class="well">\n<h3>All or Nothing is a fast, monopoly-derivative game. The goal is to win the game, but as late as possible in order to rack up as much money in the game.</h3>\n</div>\n<h1>'+str(username)+'</h1>\n<br>\n<h2>'+str(wins)+' Win'+s+'      #'+str(winRank)+'</h2>\n<br>\n<h2>$'+str(balance)+' Balance     #'+str(balanceRank)+'</h2>\n<br>\n<br>\n<form action="/change-password" id="password-change-form" method="post" enctype="multipart/form-data">\n<p>Change Password:</p>\n<label for="for-username">Current Username: </label>\n<input id="for-username" type="text" name="username">\n<br/>\n<label for="for-password">Current Password: </label>\n<input id="for-password" type="password" name="cur-password">\n<br/>\n<label for="for-new-password">New Password: </label>\n<input id="for-new-password" type="password" name="new-password">\n<br/>\n<input type="submit" value="Submit">\n</form>\n<br>\n<br>\n<br>\n</div>\n</div>\n</div>\n</div>\n</div>\n<footer class="container-fluid text-center">\n<p>Developed by Julius Merlino, Cole Grabenstatter, Buu Lam, Ziqian Yang, Songzhu Li for the Final Project in CSE312 with Dr. Jesse Hartloff</p>\n</footer>\n</body>\n</html>'
    return template

def serveLeaderboardHTML():
    # ??? If no leaderboards exist for the win/bal columns...?
    if not database.pullStatus():
        return -1

    winLeaderboard = database.pullWinsLeaderboard()
    balanceLeaderboard = database.pullBalLeaderboard()
    
    ret_val = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>ALL OR NOTHING</title>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n<body>\n<nav class="navbar navbar-inverse">\n<div class="container-fluid">\n<div class="navbar-header">\n<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n<span class="icon-bar"></span></button>\n<img src="https://i.imgur.com/3Go0b9Z.png" alt="unavailable" style="width:65px;height:50px;">\n</div>\n<div class="collapse navbar-collapse" id="myNavbar">\n<ul class="nav navbar-nav">\n<li class="active"><a href="#">Home</a></li>\n<li><a href="#">Messages</a></li>\n</ul>\n<ul class="nav navbar-nav navbar-right">\n<li><a href="http://localhost:8080/users"><span class="glyphicon glyphicon-user"></span> My Account</a></li>\n</ul>\n</div>\n</div>\n</nav>\n<div class="container text-center">\n<div class="row">\n<div class="col-sm-3 well">\n<div class="well">\n<p><a href="http://localhost:8080/">Welcome to All or Nothing</a></p>\n<p>\nThis is a game closely modeled after the Hasbro board game Monopoly.\nThis is the Final Project for CSE312 at University at Buffalo\nThe Wily 5\n</p>\n</div>\n<div class="alert alert-success fade in">\n<a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>\n<p><strong>Who is That Chatting In The Corner?</strong></p>\nGo strike up a conversation and try and make some new friends!\n</div>\n<p><a href="http://localhost:8080/leaderboard">View Leaderboard</a></p>\n<p><a href="http://localhost:8080/login">Login</a></p>\n<p><a href="http://localhost:8080/register">Create Account</a></p>\n</div><div class="col-sm-7">\n<!--Replace this with the score/grades. Kick out avatar unless you want the icon there. Maybe a good spot for the icon of the player if we want to implement it.-->\n<div class="row">\n<div class="col-sm-9">\n<div class="well">\n<h3>All or Nothing is a fast, monopoly-derivative game. The goal is to win the game, but as late as possible in order to rack up as much money in the game.</h3>\n</div>\n<br>\n<table style="width:100%">\n<tr>\n<td style="text-align:right">Rank</td>\n<td style="text-align:right">Username</td>\n<td style="text-align:right">Wins</td>\n</tr>\n'

    for i in range(len(winLeaderboard)):
        if i < 10:
            rank = i + 1
            username = winLeaderboard[i]
            wins = database.playerDetails(username)["wins"]
            entry = '<tr>\n<td style="text-align:right">#'+str(rank)+'</td>\n<td style="text-align:right">'+str(username)+'</td>\n<td style="text-align:right">'+str(wins)+'</td>\n</tr>\n'
            ret_val = ret_val + entry
        else:
            break

    ret_val = ret_val + '</table>\n<br>\n<br>\n<table style="width:100%">\n<tr>\n<td style="text-align:right">Rank</td>\n<td style="text-align:right">Username</td>\n<td style="text-align:right">Balance</td>\n</tr>\n'

    for i in range(len(balanceLeaderboard)):
        if i < 10:
            rank = i + 1
            username = balanceLeaderboard[i]
            balance = database.playerDetails(username)["monies"]
            entry = '<tr>\n<td style="text-align:right">#'+str(rank)+'</td>\n<td style="text-align:right">'+str(username)+'</td>\n<td style="text-align:right">'+str(balance)+'</td>\n</tr>\n'
            ret_val = ret_val + entry
        else:
            break

    ret_val = ret_val + '</table>\n<br>\n<br>\n</div>\n</div>\n</div>\n</div>\n</div>\n<footer class="container-fluid text-center">\n<p>Developed by Julius Merlino, Cole Grabenstatter, Buu Lam, Ziqian Yang, Songzhu Li for the Final Project in CSE312 with Dr. Jesse Hartloff</p>\n</footer>\n</body>\n</html>'
    return ret_val 
"""  
if __name__ == "__main__":
    obj = api.initBoard()
    obj = computeBoard(obj)
    html = htmlcreator(obj)
    file = open("delete.html", 'w')
    file.write(html)
    file.close()