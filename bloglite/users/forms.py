from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from bloglite.models import User



class RegistrationForm(FlaskForm):

    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email_address=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('Username already Exists')

    def validate_email(self,email_address):
        user=User.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError('Email already Exists')
    
    

class LoginForm(FlaskForm):
    email_address=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')


    def validate_email(self,email_address):
        user=User.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError(' Email does not exist ')
        

class EditProfileForm(FlaskForm):

    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    bio = StringField('Add Bio')
    email_address=StringField('Email',validators=[DataRequired(),Email()])
    picture=FileField('Upload Display Picture', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit=SubmitField('Update')
    
    def validate_username(self,username):
        if username.data != current_user.name:
            user=User.query.filter_by(name=username.data).first()
            if user:
                raise ValidationError('Username already Exists')

    def validate_email(self,email_address):
        if email_address.data != current_user.email_address:
            user=User.query.filter_by(email_address=email_address.data).first()
            if user:
                raise ValidationError('Email already Exists')
            

class FollowForm(FlaskForm):
    submit=SubmitField()

class DeleteAccountForm(FlaskForm):
    submit=SubmitField()

class SearchForm(FlaskForm):
    usertosearch=StringField('Find Friends',validators=[DataRequired()])
    submit=SubmitField('Search')