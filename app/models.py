from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


# this class is turned into an actual database table with shell
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary_key is the identifier for the table. every id column will automatically become unqiue for every user
    username = db.Column(db.String(25), nullable=False, unique=True) # all field must have value and must be unique. can have 25 char max
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    # new profile 
    bio = db.Column(db.Text, nullable=True) 
    image_file = db.Column(db.String(120), default="default.jpg")

class StudyRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True) # each room has a uniuqe id
    name = db.Column(db.String(100), nullable=False) # nullable means column cannot be empty
    description = db.Column(db.Text, nullable=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # links to the user who created the room
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    host = db.relationship('User', backref=db.backref('study_rooms', lazy=True))
    messages = db.relationship('Message', backref='room', cascade="all, delete", passive_deletes=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # foreign key means that the column must match the user.id column in user table
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('messages', lazy=True))
    




