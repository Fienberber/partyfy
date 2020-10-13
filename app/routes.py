from flask import request, render_template, jsonify, session, redirect
from app import app
from app.user import User
from app.party import Party
from app.userParty import UserParty
from app.input import Input
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

@app.route('/createParty', methods=['POST'])
def createParty():
    """Create a Party"""
    if not session.get('user_id'):
        return redirect('/', 302)

    _title = request.form.to_dict()['title']

    newParty = Party(creator_id=session.get('user_id'),
                             title=_title)

    newParty.save()
    partyID = newParty.id
    UserParty(user_id=session.get('user_id'),
                party_id=partyID).save()

    returnJson = jsonify(newParty.serialize,
                         inputTypes=[])
    return returnJson

@app.route('/getPartyInfo', methods=['POST'])
def getPartyInfo():
    """Create a Party infos"""
    if not session.get('user_id'):
        return redirect('/', 302)

    _token = request.form.to_dict()['token']
    
    partie = Party.query.filter_by(creator_id=session.get("user_id"),
                                   token=_token).first()
    _id = partie.id
    inputTypes = InputType.query.filter_by(party_id=_id).all()

    returnJson = jsonify(party=[partie.serialize],
                         inputTypes=[i.serialize for i in inputTypes])
    return returnJson

@app.route('/updateParty', methods=['POST'])
def updateParty():
    """Update a Party infos"""
    if not session.get('user_id'):
        return redirect('/', 302)

    _id = request.form.to_dict()['id']
    _title = request.form.to_dict()['title']

    partie = Party.query.filter_by(creator_id=session.get("user_id"),
                                   id=_id).first()
    partie.title = _title
    partie.save()
    return "/"

@app.route('/partyCreator', methods=['GET'])
def partyCreator():
    if not session.get('user_id'):
        return redirect('/login', 302)

    elif request.method == "GET":
        return render_template('partyCreator.html')

    elif request.method == "POST":
        content = request.get_json()
        if(content['isUpdate']):  # update values
            _id = content["id"]
            partie = Party.query.filter_by(creator_id=session.get("user_id"),
                                           id=_id).first()
            partie.setTitle(content["partyTitle"])
            partie.deleteInputTypes()
            partyID = _id

        else:  # create a new party
            title = content["partyTitle"]
            newParty = Party(creator_id=session.get('user_id'),
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


@app.route('/addInputType', methods=['POST'])
def addInputType():
    content = request.form.to_dict()
    _name = content["name"]
    _url = content["url"]
    _party_id = content["party_id"]

    if(content["id"]== -1):#it's an input type update
        inputType = InputType(name=_name, url=_url)
        inputType.save()

    else:
        _inputType_id = content["id"]
        inputType = InputType.query.filter_by(party_id=_party_id,
                                           id=_inputType_id).first()
        inputType.name = _name
        inputType.url = _url
        inputType.save()


    return jsonify(inputType.serialize)


@app.route('/removeInputType', methods=['POST'])
def removeInputType():
    content = request.form.to_dict()
    _inputType_id = content["id"]
    _party_id = content["party_id"]
    inputType = InputType.query.filter_by(party_id=_party_id,
                                        id=_inputType_id).first()

    inputType.delete()
    return "ok"


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



@app.route('/inputEditor', methods=['GET'])
def inputEditor():
    """Input Editor"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        return render_template('inputEditor.html')


@app.route('/getTypes', methods=['POST'])
def getTypes():
    """Return the input types"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        partyToken = request.form.to_dict()
        partyToken = partyToken["partyToken"]
        partyId = Party.query.filter_by(token=partyToken).first().id
        types = InputType.query.filter_by(party_id=partyId).all()
        return jsonify(json_list=[i.serialize for i in types])


@app.route('/getInput', methods=['POST'])
def getInput():
    """Return the input"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        _id = request.form.to_dict()["input_id"]
        input = Input.query.filter_by(creator_id=session.get("user_id"),
                                           id=_id).first()
        return input.serialize

@app.route('/getInputList', methods=['POST'])
def getInputList():
    """Return the input list"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        _party_token = request.form.to_dict()["token"]
        _party_id = Party.query.filter_by(token=_party_token).first().id
        inputs = Input.query.filter_by(creator_id=session.get("user_id"),
                                        party_id=_party_id).all()
        return jsonify(input_list=[i.serialize for i in inputs])

@app.route('/saveInput', methods=['POST'])
def saveInput():
    """Save the input"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        content = request.form.to_dict()
        
        _title = content["title"]
        _token = content["token"]
        _type_id = content["type_id"]
        _random_target = content["random_target"]
        _content = content["content"]
        _party_id = Party.query.filter_by(token=_token).first().id
        print("type id: " + str(_type_id))

        if(content["isUpdate"] == "True"):  # update values
            print("is update !" + content["isUpdate"])
            _input_id = content["inputId"]
            input = Input.query.filter_by(creator_id=session.get("user_id"),
                                           id=_input_id).first()
            input.title = _title
            input.type_id = _type_id
            input.party_id = _party_id
            input.content = _content
            input.random_target = _random_target
            input.save()
            inputID = input

        else:  # create a new Input
            print("Create new"  + content["isUpdate"])
            newInput = Input(creator_id=session.get('user_id'),
                             title=_title,
                             type_id = _type_id,
                             party_id = _party_id,
                             content = _content,
                             random_target = _random_target,
                             repeat = 0)

            newInput.save()
            inputID = newInput

        return jsonify(inputID.serialize)

@app.route('/removeInput', methods=['POST'])
def removeInput():
    """Delete the input types"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        _input_id = request.form.to_dict()["input_id"]
        Input.query.filter_by(creator_id=session.get("user_id"),
                                        id=_input_id).first().delete()
        
        return "ok"


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if session.get('user_id'):
        joinToken = request.args.get('token')
        if(joinToken):
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
    """Handle user account creation"""
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
    """Handle user logout"""
    session.clear()
    return redirect("/", 302)


@app.route('/setup', methods=['GET'])
def setup():
    """Setup the server for the first use"""
    try:
        mkdir('app/db')
    except FileExistsError:
        pass
    User.dbSetup()
    Party.dbSetup()
    UserParty.dbSetup()
    Input.dbSetup()
    InputType.dbSetup()
    return "Setup complete"
