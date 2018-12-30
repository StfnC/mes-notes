from time import time
import jwt
from datetime import datetime
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from matplotlib.dates import datestr2num

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    grades = db.relationship('Grade', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'''<User {self.username}>'''

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def user_loader(id):
    return User.query.get(int(id))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.Integer, index=True, default=datetime.utcnow)
    subject = db.Column(db.String(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'''<Grade {self.mark}>'''

    def reformat_date(self, date):
        self.timestamp = datestr2num(date)
