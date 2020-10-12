from flask import request, session, jsonify, redirect
from app import app
from app.party import Party
from app.userParty import UserParty
from app.inputType import InputType


def addUserToTokenParty(_user_id, _token):
    partyToJoin = Party.query.filter_by(token=_token).first()

    entryTest = UserParty.query.filter_by(user_id=_user_id,
                                          party_id=partyToJoin.id).first()
    if entryTest is None:
        userParty = UserParty(user_id=_user_id,
                              party_id=partyToJoin.id)
        userParty.save()


@app.route('/api/partyList', methods=['POST'])
def partyList():
    """Return all the parties the user created"""
    if not session.get('user_id'):
        return redirect('/', 302)

    parties = Party.query.filter_by(creator_id=session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@app.route('/api/invPartyList', methods=['POST'])
def invPartyList():
    """Return all the parties the user is invited to"""
    if not session.get('user_id'):
        return redirect('/', 302)

    join = Party.query.join(UserParty)
    parties = join.filter(UserParty.user_id == session.get("user_id")).all()
    return jsonify(json_list=[i.serialize for i in parties])


@app.route('/api/getShareLink', methods=['POST'])
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


@app.route('/api/joinParty', methods=['POST'])
def joinParty():
    """Add the user to the party using its token"""
    if not session.get('user_id'):
        return redirect('/', 302)

    data = request.form.to_dict()
    addUserToTokenParty(session.get('user_id'), data["token"])
    return "ok"


@app.route('/api/removeParty', methods=['POST'])
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


@app.route('/api/partyInfo', methods=['POST'])
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
