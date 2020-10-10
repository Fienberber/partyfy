from flask_sqlalchemy import SQLAlchemy
from app import app
from app.user import User
from app.party import Party

db = SQLAlchemy(app)


class UserParty(db.Model):
    __tablename__ = 'user_party'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey(Party.id), nullable=False)

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
                'user_id': self.user_id,
                'party_id': self.party_id}
