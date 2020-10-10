from flask import request, render_template, jsonify, session, redirect
from app import app
from app.user import User
from app.party import Party
from app.inputType import InputType
from os import mkdir
import json


@app.route('/', methods=['GET'])
def index():
    if not session.get('user_id'):
        return render_template('index.jinja2')
    elif request.method == "GET":
        return render_template('homePage.html')


@app.route('/createInput', methods=['GET'])
def createInput():
    par1 = Party(1,"Great Party")
    par1.save()
    par2 = Party(1,"Nice Party")
    par2.save()
    par3 = Party(1,"New year")
    par3.save()
    par4 = Party(1,"John birthday")
    par4.save()
    return "Done"


@app.route('/partyList', methods=['POST'])
def partyList():
    parties = Party.query.filter_by(creator_id=session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@app.route('/removeParty', methods=['POST'])
def removeParty():
    data = int(request.data.decode("utf-8"))
    d = Party.query.filter_by(id=data).first()
    if session.get("user_id") == d.creator_id:
        d.delete()
        return "ok"
    else:
        return "ko"

@app.route('/partyCreator', methods=['GET', 'POST'])
def partyCreator():
    if request.method == "GET":
        return render_template('partyCreator.html')

    elif request.method == "POST":
        content = request.data.decode("utf-8")
        print(content)
        dict_cntnt = json.loads(content)

        if(dict_cntnt["isUpdate"]=="True"):
            _id = dict_cntnt["id"]
            partie = Party.query.filter_by(creator_id=1,id=_id).first()
            partie.setTitle(dict_cntnt["partyTitle"])
            partie.deleteInputTypes()
            partyID = _id

        else:
            title = dict_cntnt["partyTitle"]
            newParty = Party(1, title)
            newParty.save()
            partyID = newParty.getId()

        inputTypes = dict_cntnt["inputTypes"]
        for inputType in inputTypes:

            name = inputType["typeName"]
            url = inputType["url"]
            InputType(partyID, name, url).save()
        return "/"


@app.route('/partyInfo', methods=['POST'])
def partyInfo():
    _id = int(request.data.decode("utf-8"))
    partie = Party.query.filter_by(creator_id=1,id=_id).first()
    inputTypes = InputType.query.filter_by(party_id=_id).all()

    returnJson = jsonify(party=[partie.serialize], inputTypes=[i.serialize for i in inputTypes])
    return returnJson


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect('/', 302)

    if request.method == "GET":
        return render_template('login.jinja2')

    elif request.method == "POST":
        data = request.form.to_dict()
        user = User.query.filter_by(email=data['email']).first()

        if user is not None:
            if user.verifyPassword(data['password']):
                session['user_id'] = user.id
                return jsonify(success=True,
                               msg=f"Heureux de te revoir {user.username}!")

        return jsonify(success=False,
                       msg="Email ou mot de passe invalide.")


@app.route('/signup', methods=['POST'])
def signup():
    data = request.form.to_dict()
    if User.query.filter_by(email=data["email"]).first() is not None:
        return jsonify(success=False,
                       msg="Cet email est déjà enregistré!")

    user = User(username=data["username"],
                email=data["email"],
                password=data["password"])
    user.saveUser()
    return jsonify(success=True,
                   msg="Compte créé! Plus qu'à se connecter 🥳")


@app.route('/setup', methods=['GET'])
def setup():
    try:
        mkdir('app/db')
    except FileExistsError:
        pass
    User.dbSetup()
    Party.dbSetup()
    InputType.dbSetup()
    return "Setup complete"
