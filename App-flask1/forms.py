from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, Email



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[InputRequired(), Length(min=10,max=150), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=150)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class QuoteForm(FlaskForm):
    content = TextAreaField('Quote', validators=[InputRequired()])
    submit = SubmitField('Save')

class AccountDeleteForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Delete')

class ProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[InputRequired()])
    submit = SubmitField('Save')