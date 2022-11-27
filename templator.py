import database

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
    template = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>ALL OR NOTHING</title>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js">\n</script>\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n<body>\n<nav class="navbar navbar-inverse">\n<div class="container-fluid">\n<div class="navbar-header">\n<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n</button>\n<a class="navbar-brand" href="#">Logo</a>\n</div>\n<div class="collapse navbar-collapse" id="myNavbar">\n<ul class="nav navbar-nav">\n<li class="active"><a href="#">Home</a></li>\n<li><a href="#">Messages</a></li>\n</ul>\n<form class="navbar-form navbar-right" role="search">\n<div class="form-group input-group">\n<input type="text" class="form-control" placeholder="Search..">\n<span class="input-group-btn">\n<button class="btn btn-default" type="button">\n<span class="glyphicon glyphicon-search"></span>\n</button>\n</span>\n</div>\n</form>\n<ul class="nav navbar-nav navbar-right">\n<li><a href="#"><span class="glyphicon glyphicon-user"></span> My Account</a></li>\n</ul>\n</div>\n</div>\n</nav>\n<div class="container text-center">\n<div class="row">\n<div class="col-sm-3 well">\n<div class="well">\n<p><a href="#">My Profile</a></p>\n<img src="bird.jpg" class="img-circle" height="65" width="65" alt="Avatar">\n</div>\n<div class="well">\n<p><a href="#">Interests</a></p>\n<p>\n<span class="label label-default">News</span>\n<span class="label label-primary">W3Schools</span>\n<span class="label label-success">Labels</span>\n<span class="label label-info">Football</span>\n<span class="label label-warning">Gaming</span>\n<span class="label label-danger">Friends</span>\n</p>\n</div>\n<div class="alert alert-success fade in">\n<a href="#" class="close" data-dismiss="alert" aria-label="close"></a>\n<p><strong>Who Is That Chatting In The Corner?</strong></p>\nGo strike up a conversation and try and make some new friends!\n</div>\n<p><a href="#">Member one</a></p>\n<p><a href="#">Member two</a></p>\n<p><a href="#">Member three</a></p>\n</div>\n<div class="col-sm-7">\n<!--Replace this with the score/grades. Kick out avatar unless you want the icon there. Maybe a good spot for the icon of the player if we want to implement it.-->\n<div class="row">\n<div class="col-sm-9">\n<div class="well">\n<h3>All or Nothing is a fast, monopoly-derivative game. The goal is to win the game, but as late as possible in order to rack up as much money in the game.</h3>\n</div>\n<h1>'+str(username)+'</h1>\n<br>\n<h2>'+str(wins)+' Win'+s+'      #'+str(winRank)+'</h2>\n<br>\n<h2>$'+str(balance)+' Balance     #'+str(balanceRank)+'</h2>\n</div>\n</div>\n</div>\n</div>\n</div>\n<footer class="container-fluid text-center">\n<p>Developed by Julius Merlino, Cole Grabenstatter, Buu Lam, Ziqian Yang, Songzhu Li for the Final Project in CSE312 with Dr. Jesse Hartloff</p>\n</footer>\n</body>\n</html>'
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
    template = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>ALL OR NOTHING</title>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js">\n</script>\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n<body>\n<nav class="navbar navbar-inverse">\n<div class="container-fluid">\n<div class="navbar-header">\n<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n</button>\n<a class="navbar-brand" href="#">Logo</a>\n</div>\n<div class="collapse navbar-collapse" id="myNavbar">\n<ul class="nav navbar-nav">\n<li class="active"><a href="#">Home</a></li>\n<li><a href="#">Messages</a></li>\n</ul>\n<form class="navbar-form navbar-right" role="search">\n<div class="form-group input-group">\n<input type="text" class="form-control" placeholder="Search..">\n<span class="input-group-btn">\n<button class="btn btn-default" type="button">\n<span class="glyphicon glyphicon-search"></span>\n</button>\n</span>\n</div>\n</form>\n<ul class="nav navbar-nav navbar-right">\n<li><a href="#"><span class="glyphicon glyphicon-user"></span> My Account</a></li>\n</ul>\n</div>\n</div>\n</nav>\n<div class="container text-center">\n<div class="row">\n<div class="col-sm-3 well">\n<div class="well">\n<p><a href="#">My Profile</a></p>\n<img src="bird.jpg" class="img-circle" height="65" width="65" alt="Avatar">\n</div>\n<div class="well">\n<p><a href="#">Interests</a></p>\n<p>\n<span class="label label-default">News</span>\n<span class="label label-primary">W3Schools</span>\n<span class="label label-success">Labels</span>\n<span class="label label-info">Football</span>\n<span class="label label-warning">Gaming</span>\n<span class="label label-danger">Friends</span>\n</p>\n</div>\n<div class="alert alert-success fade in">\n<a href="#" class="close" data-dismiss="alert" aria-label="close"></a>\n<p><strong>Who Is That Chatting In The Corner?</strong></p>\nGo strike up a conversation and try and make some new friends!\n</div>\n<p><a href="#">Member one</a></p>\n<p><a href="#">Member two</a></p>\n<p><a href="#">Member three</a></p>\n</div>\n<div class="col-sm-7">\n<!--Replace this with the score/grades. Kick out avatar unless you want the icon there. Maybe a good spot for the icon of the player if we want to implement it.-->\n<div class="row">\n<div class="col-sm-9">\n<div class="well">\n<h3>All or Nothing is a fast, monopoly-derivative game. The goal is to win the game, but as late as possible in order to rack up as much money in the game.</h3>\n</div>\n<h1>'+str(username)+'</h1>\n<br>\n<h2>'+str(wins)+' Win'+s+'      #'+str(winRank)+'</h2>\n<br>\n<h2>$'+str(balance)+' Balance     #'+str(balanceRank)+'</h2>\n<br>\n<br>\n<form action="/change-password" id="password-change-form" method="post" enctype="multipart/form-data">\n<p>Change Password:</p>\n<label for="for-username">Current Username: </label>\n<input id="for-username" type="text" name="username">\n<br/>\n<label for="for-password">Current Password: </label>\n<input id="for-password" type="password" name="cur-password">\n<br/>\n<label for="for-new-password">New Password: </label>\n<input id="for-new-password" type="password" name="new-password">\n<br/>\n<input type="submit" value="Submit">\n</form>\n<br>\n<br>\n<br>\n</div>\n</div>\n</div>\n</div>\n</div>\n<footer class="container-fluid text-center">\n<p>Developed by Julius Merlino, Cole Grabenstatter, Buu Lam, Ziqian Yang, Songzhu Li for the Final Project in CSE312 with Dr. Jesse Hartloff</p>\n</footer>\n</body>\n</html>'
    return template

def serveLeaderboardHTML():
    winLeaderboard = database.pullWinsLeaderboard()
    balanceLeaderboard = database.pullBalLeaderboard()

    if winLeaderboard == -1:
        NotImplemented
    if balanceLeaderboard == -1:
        NotImplemented
    
    ret_val = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>ALL OR NOTHING</title>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\n<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n<body>\n<nav class="navbar navbar-inverse">\n<div class="container-fluid">\n<div class="navbar-header">\n<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">\n<span class="icon-bar"></span>\n<span class="icon-bar"></span>\n<span class="icon-bar"></span></button>\n<a class="navbar-brand" href="#">Logo</a>\n</div>\n<div class="collapse navbar-collapse" id="myNavbar">\n<ul class="nav navbar-nav">\n<li class="active"><a href="#">Home</a></li>\n<li><a href="#">Messages</a></li>\n</ul>\n<form class="navbar-form navbar-right" role="search">\n<div class="form-group input-group">\n<input type="text" class="form-control" placeholder="Search..">\n<span class="input-group-btn">\n<button class="btn btn-default" type="button">\n<span class="glyphicon glyphicon-search"></span>\n</button>\n</span>\n</div>\n</form>\n<ul class="nav navbar-nav navbar-right">\n<li><a href="#"><span class="glyphicon glyphicon-user"></span> My Account</a></li>\n</ul>\n</div>\n</div>\n</nav>\n<div class="container text-center">\n<div class="row">\n<div class="col-sm-3 well">\n<div class="well">\n<p><a href="#">My Profile</a></p>\n<img src="bird.jpg" class="img-circle" height="65" width="65" alt="Avatar">\n</div>\n<div class="well">\n<p><a href="#">Interests</a></p>\n<p>\n<span class="label label-default">News</span>\n<span class="label label-primary">W3Schools</span>\n<span class="label label-success">Labels</span>\n<span class="label label-info">Football</span>\n<span class="label label-warning">Gaming</span>\n<span class="label label-danger">Friends</span>\n</p>\n</div>\n<div class="alert alert-success fade in">\n<a href="#" class="close" data-dismiss="alert" aria-label="close"></a>\n<p><strong>Who Is That Chatting In The Corner?</strong></p>\nGo strike up a conversation and try and make some new friends!\n</div>\n<p><a href="#">Member one</a></p>\n<p><a href="#">Member two</a></p>\n<p><a href="#">Member three</a></p>\n</div>\n<div class="col-sm-7">\n<!--Replace this with the score/grades. Kick out avatar unless you want the icon there. Maybe a good spot for the icon of the player if we want to implement it.-->\n<div class="row">\n<div class="col-sm-9">\n<div class="well">\n<h3>All or Nothing is a fast, monopoly-derivative game. The goal is to win the game, but as late as possible in order to rack up as much money in the game.</h3>\n</div>\n<br>\n<table style="width:100%">\n<tr>\n<td style="text-align:right">Rank</td>\n<td style="text-align:right">Username</td>\n<td style="text-align:right">Wins</td>\n</tr>\n'

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