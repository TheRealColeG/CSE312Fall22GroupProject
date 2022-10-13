#Much of the following is copied from the documentation on Flask's website:
#   https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

#Default HTML
@app.route("/")
def hello_world():
    return render_template("index.html")

#Example of escaping user input - no injection
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

#Using GET and POST requests for same page
@app.route('/users', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

#can also do this using .post() and .get()
@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/login')
def login_post():
    return do_the_login()

#DON'T CHANGE THIS!
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

