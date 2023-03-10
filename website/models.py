from flask_login import UserMixin
from . import db
class Rezultate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lungime = db.Column(db.String(50))
    diametru = db.Column(db.String(50))
    volumul = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class OberplanSch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sch_id = db.Column(db.String(200), nullable=False)
    sch_name = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    pp = db.Column(db.String(150), nullable=False)
    calculator = db.relationship('Rezultate')
    oberplan = db.relationship('OberplanSch')

