from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm, EditEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
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
        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=form)

def check_upload_file(form):
    fp = form.image.data
    # Check if fp is a FileStorage object and has a filename
    if isinstance(fp, FileStorage) and fp.filename:
        filename = secure_filename(fp.filename)
        BASE_PATH = os.path.dirname(__file__)
        upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
        db_upload_path = '/static/image/' + secure_filename(filename)
        fp.save(upload_path)
        return db_upload_path
    else:
        # Handle case where no file is uploaded (return None or a default path)
        return None

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
@bp.route('/<int:id>/book', methods=['POST'])
@login_required
def book(id):
    event = Event.query.get_or_404(id)  # Using get_or_404 to make sure the event exists
    # Here, instead of using request.form directly, we instantiate the form without it
    form = BookingForm()

    # Dynamically set the choices based on the event details
    form.ticket_type.choices = [
        ('standard', f'Standard Ticket - ${event.standard_ticket_price}'),
        ('vip', f'VIP Ticket - ${event.vip_ticket_price}'),
        ('group', f'Group Ticket - ${event.group_ticket_price} per person'),
    ]

    # We populate the form with request.form data after setting the choices
    form.process(request.form)

    if form.validate_on_submit():  # If your form validation is successful
        ticket_quantity = form.ticket_quantity.data
        ticket_type = form.ticket_type.data
        booking_reference = generate_booking_reference(event, current_user)

        # Determine the price based on ticket type
        ticket_price = 0
        if ticket_type == 'standard':
            ticket_price = event.standard_ticket_price
        elif ticket_type == 'vip':
            ticket_price = event.vip_ticket_price
        elif ticket_type == 'group':
            ticket_price = event.group_ticket_price

        # Create a new Booking instance for the current booking
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            quantity=ticket_quantity,
            ticket_type=ticket_type,
            booking_reference=booking_reference,
            total_price=ticket_price * ticket_quantity,  # Calculate total price
            is_history=True  # Presumably, you want to start with the booking not being in history
        )
        db.session.add(booking)
        db.session.commit()

        # Flash message with booking reference and price information
        flash(f'Your booking reference ID is {booking_reference}. The total price is ${booking.total_price}.', 'success')
        # Redirect to booking history or a confirmation page
        return redirect(url_for('event.show', id=id))
    else:
        # If there is an error in form validation, you may want to flash a message and redirect
        flash('There was an error with your booking.', 'danger')
        return redirect(url_for('event.show', id=id))  # Redirect back to the event detail page

# events.py

@bp.route('/booking_history')
@login_required
def booking_history():
    # Query the database to get the user's booking history
    user_bookings = Booking.query.filter_by(user_id=current_user.id, is_history=True).all()
    
    # Query the events created by the user
    user_events = current_user.events_created.all()
    
    return render_template('events/history.html', user_bookings=user_bookings, user_events=user_events)

@bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)


    form = EditEventForm(obj=event)  # Prefill form with event data

    if form.validate_on_submit():
        # Update event details
        event.name = form.name.data
        event.description = form.description.data
        event.date = form.date.data
        event.venue = form.venue.data

        # Handle file upload if there's a new image
        if form.image.data:
            event.image = check_upload_file(form)

        db.session.commit()
        flash('Your event has been updated!', 'success')
        return redirect(url_for('event.show', id=event_id))

    return render_template('events/edit.html', form=form)

@bp.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    # Add any required checks before deletion
    # For example, check if the current user is authorized to delete the event

    db.session.delete(event)
    db.session.commit()

    flash('Event has been deleted successfully.', 'success')
    return redirect(url_for('event.booking_history'))  