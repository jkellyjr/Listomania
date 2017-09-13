# listomania/app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# user signup form
class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)] )
    phone_number = StringField('Phone number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=45)] )
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm',
        message = 'Passwords must match'),
        Length(min=5, max=15) ] )
    confirm = PasswordField('Repeat Password')


# login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=45)] )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=15) ] )
    remember_me = BooleanField('Remember_me', default = False)


# edit user
class EditForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    about_me = StringField('About me', validators = [Length(min = 0, max = 140)])


# posts
class PostForm(FlaskForm):
    post = StringField('Post', validators=[DataRequired()])

# search back
class SearchForm(FlaskForm):
    search = StringField('Search', validators = [DataRequired()])
