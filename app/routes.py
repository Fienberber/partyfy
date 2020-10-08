from flask import request, render_template
from app import app
from app.user import User


@app.route('/', methods=['GET'])
def index():
    return "PARTY TIME BOYZZZZ"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.jinja2')

    elif request.method == "POST":
        data = request.form.to_dict()
        user = User.query.filter_by(email=data['email']).first()

        if user is not None:
            if user.verifyPassword(data['password']):
                return "Logged in"

        return render_template('login.jinja2')

@app.route('/setup', methods=['GET'])
def setup():
    User.dbSetup()
    return "Setup complete"
