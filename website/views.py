from flask import Blueprint, render_template, request, redirect, url_for, abort
from .models import Event
from . import db
from sqlalchemy import and_

# Create a Blueprint for the main part of the application
mainbp = Blueprint('main', __name__)

# Route to display the main index page
@mainbp.route('/')
def index():
    # Retrieve a list of events from the database
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    if 'search' in request.args and request.args['search']:
        query = "%" + request.args['search'] + "%"
        # Create a query with a filter condition
        events = db.session.query(Event).filter(Event.description.like(query)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))

@mainbp.route('/sort', methods=['GET', 'POST'])
def sort():
    sort_by = request.form.get('sort_by', 'default')

    if sort_by == 'Open':
        events = db.session.query(Event).filter(Event.status == 'Open').order_by(Event.status).all()
    elif sort_by == 'Cancelled':
        events = db.session.query(Event).filter(Event.status == 'Event Cancelled').order_by(Event.status).all()
    elif sort_by == 'Sold Out':
        events = db.session.query(Event).filter(Event.status == 'Sold Out').order_by(Event.status).all()
    elif sort_by == 'Inactive':
        events = db.session.query(Event).filter(Event.status == 'Inactive').order_by(Event.status).all()
    else:
        events = db.session.query(Event).filter(Event.status == 'Open').all()

    return render_template('index.html', events=events, sort_by=sort_by)    