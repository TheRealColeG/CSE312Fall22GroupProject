# Much of the following is copied from the documentation on Flask's website:
#   https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask, request, render_template, render_template_string
from markupsafe import escape
import sys
import database
import templator

app = Flask(__name__)

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

@app.route('/user/username')
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
    # Logging in
    if request.method == 'POST':
        return NotImplemented
    # Pulling every profile
    else:
        return NotImplemented

# can also do this using .post() and .get()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("loginpage.html")
    else:  # POST method
        # PARSE the username and password
        username = escape(request.form.get('username', ""))
        password = escape(request.form.get('password', ""))
        #TODO - maybe check if there was no username/password before checking DB
        #TODO: authAccount does check (line 69 (nice) of database.py returns False if no username exists)
        if database.authAccount(username, password):
            print("Login Successful!", file=sys.stderr)
            return render_template("homepage.html")
        else:
            print("Login failure!", file=sys.stderr)
            #TODO - Maybe edit the HTML here? Some sort of error message?
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
@app.route('/gameplay', methods=['POST'])
def move():
    if request.method == 'POST':
        with app.test_request_context('/gameplay', 'POST'):
            assert request.path == '/gameplay'
    else:
        raise Exception("Bad Request Method!")

# DON'T CHANGE THIS!
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)