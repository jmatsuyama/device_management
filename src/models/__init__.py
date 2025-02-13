from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(10), nullable=False)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    pc_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.DateTime(timezone=True))
    is_replacement = db.Column(db.Boolean, nullable=False, default=False)
    locker = db.relationship('Locker', backref='device', uselist=False)

class Locker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    is_locked = db.Column(db.Boolean, nullable=False, default=True)
    last_updated = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.UTC))
    password = db.Column(db.String(4))
    password_expiry = db.Column(db.DateTime(timezone=True))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))