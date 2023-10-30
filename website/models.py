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
    
# Booking model for storing booking information
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    quantity = db.Column(db.Integer)
    ticket_type = db.Column(db.String(30))
    booking_reference = db.Column(db.String(50))
    is_history = db.Column(db.Boolean, default=False)  
    event = db.relationship('Event', backref='bookings')

    def __init__(self, user_id, event_id, quantity, ticket_type, booking_reference, is_history=False):
        self.user_id = user_id
        self.event_id = event_id
        self.quantity = quantity
        self.ticket_type = ticket_type
        self.booking_reference = booking_reference
        self.is_history = is_history  # Set is_history to False by default for new bookings
    
        
# Comment model for storing user comments
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))  # Comment text
    created_at = db.Column(db.DateTime, default=datetime.now())  # Comment creation timestamp
    image = db.Column(db.String(400))  # Comment image
    date = db.Column(db.String(10))  # Comment date
    status = db.Column(db.String(30))  # Comment status
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to link to the user
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))  # Foreign key to link to the event

    def __repr__(self):
        return f"Comment: {self.text}"