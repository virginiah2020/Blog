from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 20)])

    email = StringField('Email', validators = [DataRequired(), Email()])

    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')




class LoginForm(FlaskForm):
    email = StringField('Email',
    validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators = [DataRequired()])
    password = PasswordField('Password',
    validators = [DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')