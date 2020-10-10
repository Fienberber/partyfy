from flask_sqlalchemy import SQLAlchemy
from app import app
from app.party import Party

db = SQLAlchemy(app)


class InputType(db.Model):
    __tablename__ = 'input_type'
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey(Party.id), nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=True)

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
                'party_id': self.party_id,
                'name': self.name,
                'url': self.url}
