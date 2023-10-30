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
    
