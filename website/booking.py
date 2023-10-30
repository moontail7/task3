# booking_utils.py

from datetime import datetime
import uuid

def generate_booking_reference(event, user):
    unique_id = uuid.uuid4().hex[:8]  # Generate a unique ID
    booking_reference = f"{user.id}-{event.id}-{unique_id}"
    return booking_reference
