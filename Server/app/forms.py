from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    email = StringField('Email', [DataRequired(), 
                                    Length(min=6, message=('Address must be at least 6 characters')),
                                    Email(message=('Please enter a valid email address.'))
                                    ])
    password = PasswordField('Password', [DataRequired(),
                                            Length(min=6, message=('Please select a stronger password.')),
                                            EqualTo('password_conf', message='Passwords must match')
                                        ])
    password_conf = PasswordField('Confirm Password', [DataRequired()])
    submit = SubmitField('Sign Up')
