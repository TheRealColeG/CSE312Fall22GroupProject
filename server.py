# Much of the following is copied from the documentation on Flask's website:
#   https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask, request, render_template, render_template_string, send_from_directory, redirect, make_response
from flask_sock import Sock
from markupsafe import escape
import sys
import database
import templator
import jack
import time
import json
import random
import html

app = Flask(__name__, static_folder="./static/functions.js")
sock = Sock(app)

def getRoll():
    possible = "123456"
    rollOne = int(random.choice(possible))
    rollTwo = int(random.choice(possible))
    return (rollOne, rollTwo)

# Default HTML


@app.route("/", methods=['GET'])
def hello_world():
    return render_template("homepage.html")

# Example of escaping user input - no injection


#This doesn't work.
@app.route("/change-password", methods=['POST'])
def change_password():
    #Authenticate
    username = escape(request.form.get('username', ""))
    password = escape(request.form.get('cur-password', ""))
    newPassword = escape(request.form.get('new-password', ""))
    truth = database.changePassword(username, password, newPassword)
    if truth:
        return redirect('/login', 301)
    else:
        return redirect('/404', 301)

#@app.route('/user/<username>')
#def show_user_profile(username):
    # show the user profile for that user
#   username = escape(username)
#   return render_template_string(templator.servePublicUserProfileHTML(username))

# Using GET and POST requests for same page

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    html = templator.serveLeaderboardHTML()
    return html

@app.route('/users', methods=['GET', 'POST'])
def lookup():
    # Pulling one profile
    if request.method == 'POST':
        #Pull the username out of the 'form' that is the search bar
        username = escape(request.form.get('search', ""))
        #Pull the HTML for the profile 
        html = templator.servePublicUserProfileHTML(username)
        #If there are no players by that username, html will be -1
        if html == -1:
            #In which case, return the homepage's html
            return render_template("homepage.html")
        #If there is a player by that username, return the html for their page
        else:
            return html
    #if the user is looking up THEIR OWN LOGGED IN PROFILE
    else:
        #Pull the cookie
        authCookie = str(escape(request.cookies.get('auth')))
        #Auth the cookie and gain the username
        print("The cookie: "+str(authCookie), flush=True)
        username = database.authAuthCookie(str(authCookie))
        print("the username: "+str(username), flush=True)
        if username != False:
            html = templator.servePrivateUserProfileHTML(username)
            return html
        else:
            print("I'm blue!", flush=True)
            return redirect('/login', 301)

# can also do this using .post() and .get()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("loginpage.html")
    else:  # POST method
        # PARSE the username and password
        username = escape(request.form.get('username', ""))
        password = escape(request.form.get('password', ""))
        if username != "" and password != "":
            if database.authAccount(username, password):
                print("Login Successful!", flush=True)
                cookie = database.genAuthCookie(username)
                res = make_response(f"Login Successful. Cookie made.")
                res.set_cookie("auth", cookie)
                res.location = '/'
                res.status_code = 301
                return res
            else:
                print("Login failure!", flush=True)
                return render_template("loginpage.html")
        else:
            return render_template("loginpage.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    #print(request.headers, flush=True)
    if request.method == 'GET':
        return render_template("registerpage.html")
    else:
        username = escape(request.form.get('username', ""))
        password = escape(request.form.get('password', ""))
        #if the username and password are valid
        if username != "" and password != "":
            r = database.newAccount(username, password)
            if r != -1:
                return redirect('/login', 301)
            else:
                return render_template("registerpage.html")
        #If they are invalid
        else:
            return render_template("registerpage.html")

@app.route("/leaderboard", methods=['GET'])
def pullLeaderboard():
    template = templator.serveLeaderboardHTML()
    if template == -1:
        return render_template("leaderboardunavailable.html")
    else:
        return template

#For use in starting games
@app.route('/gameplay/<lobby>', methods=['GET'])
def move(lobby):

    authCookie = str(escape(request.cookies.get('auth')))
    username = database.authAuthCookie(authCookie)
    if username == False:
        print("Fraud detected.", flush=True)
        return redirect('/login', 301)
    try:
        lobby = int(lobby)
        html = templator.printer(lobby)

    # ??? add socket to something?
        return render_template("leaderboardTEMPLATE.html")
    except:
        print("Fraud detected.", flush=True)
        return redirect('/404', 301)

@app.route('/functions.js')
def send_report():
    return send_from_directory('static', 'functions.js')

@app.route('/404')
def send_error():
    return render_template("404-bitchery.html")

@app.route("/gameplayTEMPLATE", methods=["GET"])
<<<<<<< Updated upstream
def open_game():
    return render_template("gameplayTEMPLATE.html")
=======
def check_connection():
    jack.startGame(1, ["Julius", "Buu", "Anton", "Cole"])
    return json.loads(templator.printer(1))
>>>>>>> Stashed changes

@app.route("/waitingRoom", methods=["GET"])
def check_connection():
    return render_template("waitingRoom.html")

@sock.route('/websocket') # can be dynamically changed
def echo(ws): 
    random_username = "User" + str(random.randint(0, 1000))
    while ws.connected: 
        data = ws.receive(timeout=0)
        if not data:
            continue
        data_received = json.loads(data)
        data_to_send = {}
        if data_received.get('socketMessage'):
            if (data_received['socketMessage'] == "connected"):
            database.active_users[random_username] = ws
                database.list_of_players.append(random_username)
            elif (data_received['socketMessage'] == 'close'):
                print("a socket closed")
            del database.active_users[random_username]
                try:
                    database.list_of_players.remove(random_username)
                except:
                    print("already deleted")
            # data_to_send = {'messageType': 'connections', 'user_count': len(database.active_users)}
            data_to_send = {'messageType': 'connections', 'user_count': len(database.list_of_players)}
            # if len(database.active_users) <= 0:
            #     break
        else:
            if data_received.get('DisplayBoard'): # replace "BOARD UPDATED!" with the pre-rendered html file
                jack.startGame(1, database.list_of_players)
                new_board = templator.printer(1)
                data_to_send = {'messageType': 'DisplayBoard', 'board': new_board}
            elif data_received.get('messageType'):
                data_to_send = {'messageType': 'chatMessage', 'username': random_username, 'message': data_received['comment']}
        for user in database.active_users:
            try:
                database.active_users[user].send(json.dumps(data_to_send))
            except:
                try:
                    database.list_of_players.remove(random_username)
                except:
                    print("can't delete in loop")
                continue

# DON'T CHANGE THIS! #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)