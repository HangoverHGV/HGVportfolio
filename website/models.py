from flask_login import UserMixin
from . import db
class Rezultate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lungime = db.Column(db.String(50))
    diametru = db.Column(db.String(50))
    volumul = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    calculator = db.relationship('Rezultate')