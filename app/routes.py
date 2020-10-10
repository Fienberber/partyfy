from flask import request, render_template, jsonify, session, redirect
from app import app
from app.user import User
from app.party import Party
from app.userParty import UserParty
from app.inputType import InputType
from os import mkdir
import json

def addUserToTokenParty(_user_id, _token):
    PartyToJoin = Party.query.filter_by(token=_token).first()

    entryTest = UserParty.query.filter_by(user_id=_user_id,party_id = PartyToJoin.id).first()
    if(entryTest == None):
        UserParty(user_id = _user_id, party_id = PartyToJoin.id).save()
    else: 
        print("saved double entry")

@app.route('/', methods=['GET'])
def index():
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        joinToken = request.args.get('token')#check if user want to join a party
        if(joinToken):
            addUserToTokenParty(session.get('user_id'), joinToken)
        return render_template('homePage.html') 
    

@app.route('/partyList', methods=['POST'])
def partyList():
    if not session.get('user_id'): return

    parties = Party.query.filter_by(creator_id=session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@app.route('/invPartyList', methods=['POST'])
def invPartyList():
    if not session.get('user_id'): return
    parties = UserParty.query.filter_by(user_id=session.get("user_id")).all()

    output = [ Party.query.filter_by(id=i.party_id).first() for i in parties ]
    #parties = Party.query.filter_by(creator_id=session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in output])

@app.route('/getShareLink', methods=['POST'])
def getShareLink():
    if not session.get('user_id'): return

    data = int(request.data.decode("utf-8"))
    d = Party.query.filter_by(id=data).first()
    if session.get("user_id") == d.creator_id:
        url = "http://localhost:8000/login?token=" + d.token
        return url
    else:
        return "ko"

@app.route('/joinParty', methods=['POST'])
def joinParty():
    data = request.form.to_dict()
    print("token: " + data["token"])
    addUserToTokenParty(session.get('user_id'), data["token"])
    return "ok"


@app.route('/removeParty', methods=['POST'])
def removeParty():
    if not session.get('user_id'): return

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
        if not session.get('user_id'): return redirect('/login', 302)#redirect if not logged in
        return render_template('partyCreator.html')

    elif request.method == "POST":
        if not session.get('user_id'): return
        content = request.data.decode("utf-8")
        print(content)
        dict_cntnt = json.loads(content)

        if(dict_cntnt["isUpdate"]=="True"):#update values
            _id = dict_cntnt["id"]
            partie = Party.query.filter_by(creator_id=session.get("user_id"),id=_id).first()
            partie.setTitle(dict_cntnt["partyTitle"])
            partie.deleteInputTypes()
            partyID = _id

        else:#create a new party
            title = dict_cntnt["partyTitle"]
            newParty = Party(creator_id=session.get("user_id"),title= title)
            newParty.save()
            partyID = newParty.id
            UserParty(user_id = session.get('user_id'), party_id = partyID).save()

        inputTypes = dict_cntnt["inputTypes"]
        for inputType in inputTypes:

            _name = inputType["typeName"]
            _url = inputType["url"]
            InputType(party_id= partyID, name= _name, url= _url).save()
        return "/"


@app.route('/partyInfo', methods=['POST'])
def partyInfo():
    if not session.get('user_id'): return
    _id = int(request.data.decode("utf-8"))
    partie = Party.query.filter_by(creator_id=session.get("user_id"),id=_id).first()
    inputTypes = InputType.query.filter_by(party_id=_id).all()

    returnJson = jsonify(party=[partie.serialize], inputTypes=[i.serialize for i in inputTypes])
    return returnJson


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        joinToken = request.args.get('token')
        if(joinToken):
            return redirect('/?token='+joinToken, 302)
        else : 
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


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect("/", 302)



@app.route('/setup', methods=['GET'])
def setup():
    try:
        mkdir('app/db')
    except FileExistsError:
        pass
    User.dbSetup()
    Party.dbSetup()
    UserParty.dbSetup()
    InputType.dbSetup()
    return "Setup complete"
