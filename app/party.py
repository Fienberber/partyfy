from flask_sqlalchemy import SQLAlchemy
from app import app
from app.user import User
import secrets


db = SQLAlchemy(app)


class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, **kwargs):
        super(Party, self).__init__(**kwargs)
        self.token = secrets.token_urlsafe(16)

    @staticmethod
    def dbSetup():
        db.create_all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def deleteInputTypes(self):
        from app.inputType import InputType

        inputTypes = InputType.query.filter_by(party_id=self.id).all()
        for i in inputTypes:
            i.delete()


    def deleteUsers(self):
        from app.userParty import UserParty

        usersInParty = UserParty.query.filter_by(party_id=self.id).all()
        for i in usersInParty:
            i.delete()

    def delete(self):
        self.deleteInputTypes()
        self.deleteUsers()
        db.session.delete(self)
        db.session.commit()

    def setTitle(self, _title):
        self.title = _title
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {'id': self.id,
                'token': self.token,
                'creator_id': self.creator_id,
                'title': self.title}
