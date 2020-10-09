from flask_sqlalchemy import SQLAlchemy
from app import app
from app.user import User

db = SQLAlchemy(app)


class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=False)


    def __init__(self, _id, _creator_id, _title):
        self.id = _id
        self.creator_id = _creator_id
        self.title = _title


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
       return {
           'id'         : self.id,
           'creator_id': self.creator_id,
           # This is an example how to deal with Many2Many relations
           'title'  : self.title
       }
