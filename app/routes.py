from flask import request, render_template, jsonify, session, redirect
from app import app
from app.user import User
from app.party import Party
from app.userParty import UserParty
from app.inputType import InputType
from os import mkdir


def addUserToTokenParty(_user_id, _token):
    partyToJoin = Party.query.filter_by(token=_token).first()

    entryTest = UserParty.query.filter_by(user_id=_user_id,
                                          party_id=partyToJoin.id).first()
    if entryTest is None:
        userParty = UserParty(user_id=_user_id,
                              party_id=partyToJoin.id)
        userParty.save()


@app.route('/', methods=['GET'])
def index():
    """Homepage"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        # check if user want to join a party
        joinToken = request.args.get('token')
        if(joinToken):
            addUserToTokenParty(session.get('user_id'), joinToken)

        return render_template('homePage.html')


@app.route('/partyList', methods=['POST'])
def partyList():
    """Return all the parties the user created"""
    if not session.get('user_id'):
        return redirect('/', 302)

    parties = Party.query.filter_by(creator_id=session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@app.route('/invPartyList', methods=['POST'])
def invPartyList():
    """Return all the parties the user is invited to"""
    if not session.get('user_id'):
        return redirect('/', 302)

    join = Party.query.join(UserParty)
    parties = join.filter(UserParty.user_id == session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@app.route('/getShareLink', methods=['POST'])
def getShareLink():
    """Return an invite link for the party. Send the party ID"""
    if not session.get('user_id'):
        return redirect('/', 302)

    data = int(request.data.decode("utf-8"))
    d = Party.query.filter_by(id=data).first()
    if session.get("user_id") == d.creator_id:
        url = "http://localhost:8000/login?token=" + d.token
        return url
    else:
        return "ko"


@app.route('/joinParty', methods=['POST'])
def joinParty():
    """Add the user to the party using its token"""
    if not session.get('user_id'):
        return redirect('/', 302)

    data = request.form.to_dict()
    addUserToTokenParty(session.get('user_id'), data["token"])
    return "ok"


@app.route('/removeParty', methods=['POST'])
def removeParty():
    """Delete a party. Can only be done by the party's creator"""
    if not session.get('user_id'):
        return redirect('/', 302)

    data = int(request.data.decode("utf-8"))
    d = Party.query.filter_by(id=data).first()
    if session.get("user_id") == d.creator_id:
        d.delete()
        return "ok"
    else:
        return "ko"


@app.route('/partyCreator', methods=['GET', 'POST'])
def partyCreator():
    if not session.get('user_id'):
        return redirect('/login', 302)

    elif request.method == "GET":
        return render_template('partyCreator.html')

    elif request.method == "POST":
        content = request.get_json(force=True)

        if(content["isUpdate"] == "True"):  # update values
            _id = content["id"]
            partie = Party.query.filter_by(creator_id=session.get("user_id"),
                                           id=_id).first()
            partie.setTitle(content["partyTitle"])
            partie.deleteInputTypes()
            partyID = _id

        else:  # create a new party
            title = content["partyTitle"]
            newParty = Party(creator_id=session.get-'user_id',
                             title=title)
            newParty.save()
            partyID = newParty.id
            UserParty(user_id=session.get('user_id'),
                      party_id=partyID).save()

        inputTypes = content["inputTypes"]
        for i in inputTypes:
            name = i["typeName"]
            url = i["url"]
            inputType = InputType(party_id=partyID,
                                  name=name,
                                  url=url)
            inputType.save()

        return "/"


@app.route('/partyInfo', methods=['POST'])
def partyInfo():
    """Return infos on party"""
    if not session.get('user_id'):
        return redirect('/', 302)

    _id = int(request.data.decode("utf-8"))
    partie = Party.query.filter_by(creator_id=session.get("user_id"),
                                   id=_id).first()
    inputTypes = InputType.query.filter_by(party_id=_id).all()

    returnJson = jsonify(party=[partie.serialize],
                         inputTypes=[i.serialize for i in inputTypes])
    return returnJson


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        joinToken = request.args.get('token')
        if(len(joinToken) >= 10):
            return redirect('/?token='+joinToken, 302)
        else:
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
