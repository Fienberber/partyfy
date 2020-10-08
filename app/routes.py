from flask import request, render_template
from app import app
from app.user import User
from os import mkdir


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


@app.route('/signup', methods=['POST'])
def signup():
    data = request.form.to_dict()
    if User.query.filter_by(email=data["email"]).first() is not None:
        return "User already exists"

    user = User(username=data["username"],
                email=data["email"],
                password=data["password"])
    user.saveUser()
    return "User created"


@app.route('/setup', methods=['GET'])
def setup():
    mkdir('db')
    User.dbSetup()
    return "Setup complete"
