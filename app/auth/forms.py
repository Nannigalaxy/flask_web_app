from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Faculty


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Faculty.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_faculty(self, field):
        if Faculty.query.filter_by(first_name=field.data).first() and Faculty.query.filter_by(last_name=field.data).first():
            raise ValidationError('Faculty already exists.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
