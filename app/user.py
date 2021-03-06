from flask_sqlalchemy import SQLAlchemy
from app import app
from hashlib import sha256

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def dbSetup():
        print(db.metadata.tables.keys())
        db.create_all()

    def saveUser(self):
        db.session.add(self)
        db.session.commit()

    def setPassword(self, passwd):
        self.password = sha256(passwd.encode('utf-8')).hexdigest()
        db.session.commit()

    def verifyPassword(self, passwd):
        return(self.password == sha256(passwd.encode('utf-8')).hexdigest())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {'id': self.id,
                'username': self.username,
                'email': self.email}