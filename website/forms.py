from flask import Flask
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import EqualTo, Regexp, Email, Length, DataRequired, InputRequired


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[Length(min=3, max=10), InputRequired()])
    last_name = StringField("Last Name", validators=[Length(min=3, max=10), InputRequired()])
    email = EmailField("Email", validators=[Email(message="Use correct email"), DataRequired()])
    password = PasswordField("Password", validators=[Length(min=8, max=20), DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo("password"), DataRequired()])
    submit = SubmitField('Register')
    
    
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[Email(message="Use correct email"), DataRequired()])
    password = PasswordField("Password", validators=[Length(min=8, max=20), DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
