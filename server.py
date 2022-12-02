# Much of the following is copied from the documentation on Flask's website:
#   https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask, request, render_template, render_template_string, send_from_directory
from flask_sock import Sock
from markupsafe import escape
import sys
import database
import templator
import jack
import time
import json
import random

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
    username = request.form.get('username', "")
    password = request.form.get('cur-password', "")
    newPassword = request.form.get('new-password', "")
    print("Test case:\nThe username is: "+str(username)+", the 'old' password is: "+str(password)+", and the requested new-password is: "+str(newPassword)+". ", flush=True)
    #TODO - Check if user entered any data/same password/etc.
    #truth = database.changePassword(username, password, newPassword)
    #if truth:
    #    return render_template("homepage.html")
    #else:
    #    return "Failure!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
   username = escape(username)
   return render_template_string(templator.servePublicUserProfileHTML(username))

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
        authcookie = NotImplemented
        #Auth the cookie
        authStatus = NotImplemented
        #pull the username from the cookie???
        username = NotImplemented
        if authStatus:
            html = templator.servePrivateUserProfileHTML(username)
            return html
        else:
            return render_template("loginpage.html")

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
                print("Login Successful!", file=sys.stderr)
                return render_template("homepage.html")
            else:
                print("Login failure!", file=sys.stderr)
                #TODO - Maybe edit the HTML here? Some sort of error message?
                return render_template("loginpage.html")
        else:
            return render_template("loginpage.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    #print(request.headers, flush=True)
    if request.method == 'GET':
        return render_template("registerpage.html")
    else:
        username = escape(request.headers.get('username'))
        password = escape(request.headers.get('password'))
        #if the username and password are valid
        if username != "" and password != "":
            database.newAccount(username, password)
            return render_template("loginpage.html")
        #If they are invalid
        else:
            return render_template("registerpage.html")

# For use for authentication+player move in the game
@app.route('/gameplay/<lobby>', methods=['POST'])
def move(lobby):

    #authenticate token here:

    try:
        lobby = int(lobby)
    except:
        print("Fraud detected.", flush=True)
    if request.method == 'POST':
        #I don't know what this is:
        with app.test_request_context('/gameplay', 'POST'):
            assert request.path == '/gameplay'


        command = NotImplemented #???
        player = NotImplemented #??? Identify the username of the player that is sending the command
        #Maybe do this ^^^ with authenticated XSRF token...? Sounds like a good idea.

        if command == 'Roll':
            roll = getRoll()
            #websockets.pushTemplate() #Push the dice result
            time.sleep(2) #Let the player read it before moving pieces

            status = jack.sendMove(lobby, player, roll)
            #If the player has to choose to buy/rent/etc.

            #Not sure what's going on down here.
            #if status == "Choice":
                #websockets.pushTemplate() #Push the board to the same player and wait for a response

        time.sleep(2)

        gameTemplate = NotImplemented #???
        return gameTemplate
        
    else:
        raise Exception("Bad Request Method!")

@app.route('/functions.js')
def send_report():
    return send_from_directory('static', 'functions.js')

@sock.route('/websocket') # can be dynamically changed
def echo(ws): #final branch fix
    random_username = "User" + str(random.randint(0, 1000))
    status = json.loads(ws.receive())
    # print(status)
    if (status['socketMessage'] == "connected"):
        database.active_users[random_username] = ws
    elif (status['socketMessage'] == "close"):
        del database.active_users[random_username]

    while ws.connected:
        data = ws.receive()
        data_received = json.loads(data)
        data_to_send = {'messageType': 'chatMessage', 'username': random_username, 'message': data_received['comment']}
        # ws.send(json.dumps(data_to_send))
        for user in database.active_users:
            try:
                database.active_users[user].send(json.dumps(data_to_send))
            except:
                continue

# DON'T CHANGE THIS!
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)