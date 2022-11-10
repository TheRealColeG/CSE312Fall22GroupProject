#Much of the following is copied from the documentation on Flask's website:
#   https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask, request, render_template
from markupsafe import escape
import database

app = Flask(__name__)

#Default HTML
@app.route("/")
def hello_world():
    return render_template("homepage.html")

#Example of escaping user input - no injection
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    user = database.playerDetails(escape(username))
    return user

#Using GET and POST requests for same page
@app.route('/users', methods=['GET', 'POST'])
def lookup():
    #Logging in
    if request.method == 'POST':
        return do_the_login()
    #Pulling every profile
    else:
        return show_the_login_form()

#can also do this using .post() and .get()
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("loginpage.html")
    else:
        ###PARSE the username and password
        username = 0
        password = 0
        if database.authAccount(username, password):
            print("yay you logged in!")
        else:
            print("Sorry, invalid details.")
        NotImplemented

@app.post('/login')
def login_post():
    return do_the_login()

#DON'T CHANGE THIS!
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

