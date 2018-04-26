from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email,  Length


class SignupForm(Form):
    first_name = StringField('First name',validators=[DataRequired('First name is required')])
    last_name = StringField('Last name',validators=[DataRequired('Last name is required')])
    email = StringField('Email',validators=[DataRequired('Email is required'),Email('Please enter a valid email address')])
    password = PasswordField('Password',validators=[DataRequired('Password is required'),Length(min=6,message='Password must be atleast 6 characters long')])
    submit = SubmitField('Sign Up')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired('Please enter your email address'),Email('Please enter a valid email address')])
    password = PasswordField('Password',validators=[DataRequired('Password is required'),Length(min=6,message='Password must be atleast 6 characters long')])
    submit = SubmitField('Sign In')
    
class NewTiffinForm(Form):

    timing = SelectField('Timing', choices=[['Break Fast','Break Fast' ], ['Lunch', 'Lunch'], ['Dinner', 'Dinner'] ])
    tiffinType = SelectField('Tiffin Type', choices=[['Veg', 'Veg'], ['Non-Veg', 'Non-Veg']])
    size = SelectField('Size', choices=[['small', 'small'], ['Medium', 'Medium'], ['Large', 'Large']])
    existingAddress = SelectField('Choose existing Delivery Address', choices= [["",""]])
    newAddressName = StringField('Please enter a nick name for this address')
    addressLine1 = StringField('Address line 1')
    addressLine2 = StringField('Address line 2')
    city = SelectField('City', choices=[['NewDelhi', 'NewDelhi'], ['Gurugram', 'Gurugram'], ['Noida', 'Noida']])
    pincode = StringField('Pin Code')
    proceed = SubmitField('Proceed')
