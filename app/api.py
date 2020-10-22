from flask import request, session, jsonify, redirect, abort
from app import app
from app.user import User
from app.input import Input
from app.party import Party
from app.userParty import UserParty
from app.inputType import InputType


# Decorator
def protectedApi(f):
    """This defines a decorator that can be used to limit api interaction to
    logged in users"""
    def _protectedApi(*args, **kwargs):
        if not session.get('user_id'):  # Not logged in
            abort(401)  # Unauthorized
        else:
            return f(*args, **kwargs)
    return _protectedApi


def addUserToTokenParty(_user_id, _token):
    partyToJoin = Party.query.filter_by(token=_token).first()

    entryTest = UserParty.query.filter_by(user_id=_user_id,
                                          party_id=partyToJoin.id).first()
    if entryTest is None:
        userParty = UserParty(user_id=_user_id,
                              party_id=partyToJoin.id)
        userParty.save()


@protectedApi
@app.route('/api/partyList', methods=['POST'])
def partyList():
    """Return all the parties the user created"""
    parties = Party.query.filter_by(creator_id=session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@protectedApi
@app.route('/api/invPartyList', methods=['POST'])
def invPartyList():
    """Return all the parties the user is invited to"""
    join = Party.query.join(UserParty)
    parties = join.filter(UserParty.user_id == session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@protectedApi
@app.route('/api/getPartyInfo', methods=['POST'])
def getPartyInfo():
    """Create a Party infos"""
    _token = request.form.to_dict()['token']
    
    partie = Party.query.filter_by(creator_id=session.get("user_id"),
                                   token=_token).first()
    _id = partie.id
    inputTypes = InputType.query.filter_by(party_id=_id).all()

    returnJson = jsonify(party=[partie.serialize],
                         inputTypes=[i.serialize for i in inputTypes])
    return returnJson


@protectedApi
@app.route('/api/joinParty', methods=['POST'])
def joinParty():
    """Add the user to the party using its token"""
    data = request.form.to_dict()
    addUserToTokenParty(session.get('user_id'), data["token"])
    return "ok"


@protectedApi
@app.route('/api/removeParty', methods=['POST'])
def removeParty():
    """Delete a party. Can only be done by the party's creator"""
    _token = request.form.to_dict()['token']
    Party.query.filter_by(creator_id=session.get("user_id"),
                                   token=_token).first().delete()
    
    return "ok"


@protectedApi
@app.route('/api/createParty', methods=['POST'])
def createParty():
    """Create a Party"""
    _title = request.form.to_dict()['title']

    newParty = Party(creator_id=session.get('user_id'),
                             title=_title)

    newParty.save()
    partyID = newParty.id
    UserParty(user_id=session.get('user_id'),
                party_id=partyID).save()

    returnJson = jsonify(party=[newParty.serialize],
                         inputTypes=[])

    return returnJson    


@protectedApi
@app.route('/api/updateParty', methods=['POST'])
def updateParty():
    """Update a Party infos"""
    _id = request.form.to_dict()['id']
    _title = request.form.to_dict()['title']

    partie = Party.query.filter_by(creator_id=session.get("user_id"),
                                   id=_id).first()
    partie.title = _title
    partie.save()
    return "/"


@protectedApi
@app.route('/api/addInputType', methods=['POST'])
def addInputType():
    content = request.form.to_dict()
    _name = content["name"]
    _url = content["url"]
    _party_id = int(content["party_id"])
    _inputType_id = int(content["id"])
    if(_inputType_id==-1):#it's an input type update
        inputType = InputType(name=_name, 
                                url=_url,
                                party_id=_party_id)
        inputType.save()

    else:
        inputType = InputType.query.filter_by(party_id=_party_id,
                                           id=_inputType_id).first()
        inputType.name = _name
        inputType.url = _url
        inputType.save()

    return jsonify(inputType.serialize)


@protectedApi
@app.route('/api/removeInputType', methods=['POST'])
def removeInputType():
    content = request.form.to_dict()
    _inputType_id = content["id"]
    _party_id = content["party_id"]
    inputType = InputType.query.filter_by(party_id=_party_id,
                                        id=_inputType_id).first()

    inputType.delete()
    return "ok"



@protectedApi
@app.route('/api/getInput', methods=['POST'])
def getInput():
    """Return the input"""
    _id = request.form.to_dict()["input_id"]
    input = Input.query.filter_by(creator_id=session.get("user_id"),
                                        id=_id).first()
    return input.serialize


@protectedApi
@app.route('/api/getInputList', methods=['POST'])
def getInputList():
    """Return the input list"""
    _party_token = request.form.to_dict()["token"]
    _party_id = Party.query.filter_by(token=_party_token).first().id
    inputs = Input.query.filter_by(creator_id=session.get("user_id"),
                                    party_id=_party_id).all()
    return jsonify(input_list=[i.serialize for i in inputs])


@protectedApi
@app.route('/api/saveInput', methods=['POST'])
def saveInput():
    """Save the input"""
    content = request.form.to_dict()
    
    _title = content["title"]
    _token = content["token"]
    _type_id = content["type_id"]
    _random_target = content["random_target"]
    _content = content["content"]
    _party_id = Party.query.filter_by(token=_token).first().id

    if(content["isUpdate"] == "True"):  # update values
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


@protectedApi
@app.route('/api/removeInput', methods=['POST'])
def removeInput():
    """Delete the input types"""
    _input_id = request.form.to_dict()["input_id"]
    Input.query.filter_by(creator_id=session.get("user_id"),
                                    id=_input_id).first().delete()
    
    return "ok"


@protectedApi
@app.route('/api/getPlayers', methods=['POST'])
def getPlayers():
    """Return all the Players in the party"""
    _token = request.form.to_dict()["partyToken"]

    join = User.query.join(UserParty)
    party = Party.query.filter_by(token=_token).first()

    players = join.filter(UserParty.party_id == party.id).all()
    
    return jsonify(players=[i.serialize for i in players])


@protectedApi
@app.route('/api/getInputs', methods=['POST'])
def getInputs():
    """Return all the Inputs in the party"""
    _token = request.form.to_dict()["partyToken"]

    party = Party.query.filter_by(token=_token).first()
    inputs = Input.query.filter_by(party_id=party.id).all()
    
    return jsonify(inputs=[i.serialize for i in inputs])

@protectedApi
@app.route('/api/getTypes', methods=['POST'])
def getTypes():
    """Return all the Inputs in the party"""
    _token = request.form.to_dict()["partyToken"]

    party = Party.query.filter_by(token=_token).first()
    types = InputType.query.filter_by(party_id=party.id).all()
    
    return jsonify(types=[i.serialize for i in types])

@protectedApi
@app.route('/api/getParties', methods=['POST'])
def getParties():
    """Return all the Parties the player can play"""

    parties = Party.query.filter_by(creator_id=session.get("user_id")).all()
    return jsonify(parties=[i.serialize for i in parties])

    