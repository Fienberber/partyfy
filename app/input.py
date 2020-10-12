from flask_sqlalchemy import SQLAlchemy
from app import app
from app.inputType import InputType
from app.party import Party
from app.user import User

db = SQLAlchemy(app)


class Input(db.Model):
    __tablename__ = 'input'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey(InputType.id), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey(Party.id), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    repeat = db.Column(db.Integer, unique=False, nullable=False)
    random_target = db.Column(db.Integer, unique=False, nullable=False)
    content = db.Column(db.String(80), unique=False, nullable=False)

    @staticmethod
    def dbSetup():
        db.create_all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {'id': self.id,
                'title': self.title,
                'type_id': self.type_id,
                'party_id': self.party_id,
                'creator_id': self.creator_id,
                'repeat': self.repeat,
                'random_target': self.random_target,
                'content': self.content}
