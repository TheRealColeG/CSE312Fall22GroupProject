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
    print("Test case:\nThe username is: "+str(username)+", the 'old' password is: "+str(password)+", and the requested new-password is: "+str(newPassword)+". ", flush=True)
    #TODO - Check if user entered any data/same password/etc.
    truth = database.changePassword(username, password, newPassword)
    if truth:
        return redirect('/login', 301)
    else:
        return "Failure!"

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
        authCookie = str(escape(request.cookies.get('auth')))
        #Auth the cookie and gain the username
        username = database.authAuthCookie(str(authCookie))
        if username != False:
            html = templator.servePrivateUserProfileHTML(username)
            return html
        else:
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
    print("This ran!!!", flush=True)
    #authenticate token here:
    try:
        lobby = int(lobby)
    except:
        print("Fraud detected.", flush=True)
        return redirect('/404', 301)

    # ??? add socket to something?
    return render_template("leaderboardTEMPLATE.html")

@app.route('/functions.js')
def send_report():
    return send_from_directory('static', 'functions.js')

@app.route('/404')
def send_error():
    return render_template("404-bitchery.html")

@sock.route('/websocket') # can be dynamically changed
def echo(ws): #final branch fix
    random_username = "User" + str(random.randint(0, 1000))
    status = json.loads(ws.receive())
    # print(status)
    if (status['socketMessage'] == "connected"):
        database.active_users[random_username] = ws

    while True:
        data = ws.receive()
        data_received = json.loads(data)
        if (data_received.get('socketMessage') and data_received['socketMessage'] == 'close'):
            del database.active_users[random_username]
            break
        data_to_send = {'messageType': 'chatMessage', 'username': random_username, 'message': data_received['comment']}
        for user in database.active_users:
            database.active_users[user].send(json.dumps(data_to_send))

# DON'T CHANGE THIS! #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)