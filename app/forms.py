from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(username=username.data).first()
        if user is not None:
            raise ValidationError('Please choose a different Username')

    def validate_email(self, email):
        email = User.query.filter(email=email.data).first()
        if email is not None:
            raise ValidationError('That email is already in use')


class StoryPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Say something', validators=[DataRequired()])
    delete = SubmitField('Delete')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('What did you think?', validators=[DataRequired()])
    delete = SubmitField('Delete')
    submit = SubmitField('Submit')
