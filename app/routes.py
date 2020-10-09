from flask import request, render_template, jsonify
from app import app
from app.user import User
from app.party import Party
from os import mkdir


@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        return render_template('homePage.html')

    elif request.method == "POST":
        return "ok"


@app.route('/createInput', methods=['GET'])
def createInput():
    par1 = Party(1, 1, "Great Party")
    par1.save()
    par2 = Party(2, 1, "Nice Party")
    par2.save()
    par3 = Party(3, 1, "New year")
    par3.save()
    par4 = Party(4, 1, "John birthday")
    par4.save()
    return "Done"


@app.route('/partyList', methods=['POST'])
def partyList():
    parties = Party.query.filter_by(creator_id=1).all()
    print(parties)
    return jsonify(json_list=[i.serialize for i in parties])


@app.route('/removeParty', methods=['POST'])
def removeParty():
    data = int(request.data.decode("utf-8"))
    d = Party.query.filter_by(id=data).first()
    d.delete()
    return "ok"


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

        return "Invalid email/password"


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
    try:
        mkdir('app/db')
    except FileExistsError:
        pass

    User.dbSetup()
    Party.dbSetup()
    return "Setup complete"
