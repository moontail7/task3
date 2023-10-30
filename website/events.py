from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import uuid
from .booking import generate_booking_reference
from .models import Booking


# Create a Blueprint for events
bp = Blueprint('event', __name__, url_prefix='/events')

# Show the details of an event
@bp.route('/<id>', methods=['GET', 'POST'])
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    form = CommentForm()
    
    # Create a new BookingForm for handling ticket purchases
    booking_form = BookingForm(request.form)

    if booking_form.validate_on_submit():
        ticket_quantity = int(booking_form.ticket_quantity.data)
        ticket_type = str(booking_form.ticket_type.data)

    return render_template('events/show.html', event=event, form=form, booking_form=booking_form)


# Create a new event
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        # Create a new event and add it to the database
        event = Event(
            name=form.name.data,
            description=form.description.data,
            image=db_file_path,
            venue=form.venue.data,
            status=form.status.data,
            date=form.date.data,
            user_id=current_user.id  # Assign the user ID
        )
        db.session.add(event)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.create'))
    return render_template('events/create.html', form=form)

# Function to handle file uploads
def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
    db_upload_path = '/static/image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

# Add a comment to an event
@bp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            event=event,
            user=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
    return redirect(url_for('event.show', id=id))

# events.py
@bp.route('/<id>/book', methods=['POST'])
@login_required
def book(id):
    event = Event.query.get(id)
    form = BookingForm(request.form)

    if form.validate():
        ticket_quantity = form.ticket_quantity.data
        booking_reference = generate_booking_reference(event, current_user)
        ticket_type = form.ticket_type.data  # Get ticket_type from the form

        # Create a new Booking instance for the current booking
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            quantity=ticket_quantity,
            ticket_type=ticket_type,  # Include ticket_type
            booking_reference=booking_reference,
            is_history=True  # This is not in booking history
        )
        db.session.add(booking)
        db.session.commit()

        flash(f'Your booking reference ID is {booking_reference}', 'success')
    return redirect(url_for('event.show', id=id))

# events.py

@bp.route('/booking_history')
@login_required
def booking_history():
    # Query the database to get the user's booking history
    user_bookings = Booking.query.filter_by(user_id=current_user.id, is_history=True).all()
    
    # Query the events created by the user
    user_events = current_user.events_created.all()
    
    return render_template('events/history.html', user_bookings=user_bookings, user_events=user_events)
