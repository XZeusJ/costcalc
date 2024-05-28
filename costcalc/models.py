from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from costcalc.extensions import db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Labor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

