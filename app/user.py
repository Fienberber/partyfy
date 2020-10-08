from flask_sqlalchemy import SQLAlchemy
from app import app
from hashlib import sha256

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def dbSetup():
        db.create_all()

    def saveUser(self):
        db.session.add(self)
        db.session.commit()

    def verifyPassword(self, passwd):
        return(self.password == sha256(passwd.encode('utf-8')).hexdigest())
