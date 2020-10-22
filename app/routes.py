from flask import request, render_template, jsonify, session, redirect
from app import app
from app import api
from app import mail
from app.user import User
from app.party import Party
from app.userParty import UserParty
from app.input import Input
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


@app.route('/partyCreator', methods=['GET'])
def partyCreator():
    if not session.get('user_id'):
        return redirect('/login', 302)

    elif request.method == "GET":
        return render_template('partyCreator.html')


@app.route('/inputEditor', methods=['GET'])
def inputEditor():
    """Input Editor"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        return render_template('inputEditor.html')

@app.route('/gameEngine', methods=['GET'])
def gameEngine():
    """Game Engine"""
    if not session.get('user_id'):
        return render_template('index.jinja2')
    else:
        return render_template('gameEngine.html')

@app.route('/newPassword', methods=['GET'])
def newPassword():
    """Password Management"""
    return render_template('NewPassword.html')


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


@app.route('/changePass', methods=['POST'])
def changePass():
    """Changes the password"""
    old_Pass = request.form.to_dict()["oldPass"]
    new_Pass = request.form.to_dict()["newPass"]
    _email = request.form.to_dict()["email"]

    user = User.query.filter_by(email=_email).first()
    if(user.verifyPassword(old_Pass)):
        user.setPassword(new_Pass)
        return "Password Changed successfully"

    return "Wrong password, try again or request a new one."


@app.route('/getNewPass', methods=['POST'])
def getNewPass():
    """Send an email with a new random generated password"""
    _email = request.form.to_dict()["email"]
    if(mail.sendNewPassword(_email)):
        return "The new password has been sent, please check your inbox"

    return "An error has occured, please try again"


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
    Input.dbSetup()
    InputType.dbSetup()
    return "Setup complete"

