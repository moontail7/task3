from flask_login import UserMixin
from . import db
from datetime import datetime

# User model for user authentication
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)  # User's name
    emailid = db.Column(db.String(100), index=True, nullable=False)  # User's email
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password
    
    comments = db.relationship('Comment', backref='user')  # Relationship to comments
    
    # Relationship to events created by the user
    events_created = db.relationship('Event', backref='creator', lazy='dynamic')

    def __repr__(self):
        return f"Name: {self.name}"
    


# Event model for storing event information
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))  # Event name
    description = db.Column(db.String(200))  # Event description
    date = db.Column(db.String(200))  # Event date
    status = db.Column(db.String(200))  # Event date
    venue = db.Column(db.String(200))  # Event venue
    image = db.Column(db.String(400))  # Event image
    comments = db.relationship('Comment', backref='event')  # Relationship to comments
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f"Name: {self.name}"
    
    # Additional methods as needed