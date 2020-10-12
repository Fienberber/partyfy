from flask import request, render_template, jsonify, session, redirect
from app import app
from app import api
from app.user import User
from app.party import Party
from app.userParty import UserParty
from app.inputType import InputType
from os import mkdir


@app.route('/', methods=['GET'])
def index():
    """Homepage"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        # check if user want to join a party
        joinToken = request.args.get('token')
        if(joinToken):
            api.addUserToTokenParty(session.get('user_id'), joinToken)

        return render_template('homePage.html')


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

# Temporary
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
    InputType.dbSetup()
    return "Setup complete"
