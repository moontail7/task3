from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, IntegerField, StringField, PasswordField, SelectField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed 


# Define a set of allowed image file extensions
ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg', 'jpeg'}

# Form for creating an event
class EventForm(FlaskForm):
    STATUS_LIST = [
        ('Open', 'Open'),
        ('Inactive', 'Inactive'),
        ('Sold Out', 'Sold Out'),
        ('Cancelled', 'Event Cancelled'),
    ]
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Event Description', validators=[InputRequired()])
    standard_ticket_price = DecimalField('Standard Ticket Price', validators=[InputRequired()], default=50.00)
    vip_ticket_price = DecimalField('VIP Ticket Price', validators=[InputRequired()], default=100.00)
    group_ticket_price = DecimalField('Group Ticket Price', validators=[InputRequired()], default=175.00)
    venue = TextAreaField('Event Venue', validators=[InputRequired()])
    date = TextAreaField('Event Date', validators=[InputRequired()])
    status = SelectField('Event Status', choices=STATUS_LIST)
    image = FileField('Event Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='File is not supported')])
    submit = SubmitField("Create")

# Form for user login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# Form for user registration
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# Form for adding comments
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')
    
# Form for buying tickets
class BookingForm(FlaskForm):
    ticket_quantity = IntegerField('Number of Tickets', validators=[NumberRange(min=1, message='Please select at least 1 ticket')])
    # Initialize ticket_type without choices here; we'll set them in the view
    ticket_type = SelectField('Ticket Type', choices=[])
    submit = SubmitField('Book Tickets')

class EditEventForm(FlaskForm):
    STATUS_LIST = [
        ('Open', 'Open'),
        ('Inactive', 'Inactive'),
        ('Sold Out', 'Sold Out'),
        ('Cancelled', 'Event Cancelled'),
    ]

    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Event Description', validators=[InputRequired()])
    standard_ticket_price = DecimalField('Standard Ticket Price', validators=[InputRequired()])
    vip_ticket_price = DecimalField('VIP Ticket Price', validators=[InputRequired()])
    group_ticket_price = DecimalField('Group Ticket Price', validators=[InputRequired()])
    venue = TextAreaField('Event Venue', validators=[InputRequired()])
    date = TextAreaField('Event Date', validators=[InputRequired()])
    status = SelectField('Event Status', choices=STATUS_LIST)
    image = FileField('Event Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='File is not supported')])
    submit = SubmitField("Update Event")