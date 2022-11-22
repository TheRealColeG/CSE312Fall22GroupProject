# Much of the following is copied from the documentation on Flask's website:
#   https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask, request, render_template
from markupsafe import escape
import database

app = Flask(__name__)

# Default HTML


@app.route("/", methods=['GET'])
def hello_world():
    return render_template("homepage.html")

# Example of escaping user input - no injection


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    user = database.playerDetails(escape(username))
    return user

# Using GET and POST requests for same page


@app.route('/users', methods=['GET', 'POST'])
def lookup():
    # Logging in
    if request.method == 'POST':
        return do_the_login()
    # Pulling every profile
    else:
        return show_the_login_form()

# can also do this using .post() and .get()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("loginpage.html")
    else:  # POST method
        # PARSE the username and password
        print(request.headers)
        username = request.headers.get('Username')
        password = request.headers.get('Password')
        if database.authAccount(username, password):
            print("Login Successful!")
            return render_template("homepage.html")
        else:
            print("Login failure!")
            return render_template("loginpage.html")

#
@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.headers, flush=True)
    if request.method == 'GET':
        return render_template("registerpage.html")
    else:
        username = request.headers.get('username')
        password = request.headers.get('password')
        createdAccount = database.newAccount(username, password)
        return render_template("loginpage.html")

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