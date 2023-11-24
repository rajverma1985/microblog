from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Now')

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username in use, please user another username")

    @staticmethod
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("Email already in use, try logging in!")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=10, max=250)])
    submit = SubmitField('Update Profile')

    def __init__(self, old_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.old_username = old_username

    # **IMP NOTE: This is a special prefix which automatically get checked when using flask forms. If a method has
    # validate_ in front of it, it gets checked during validation calls. like this is view function edit_profile
    # form.validate_on_submit()**
    def validate_username(self, new_username):
        if new_username.data != self.old_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Username in use, please user another username.")


# user needs to do is click on "Follow" or "Unfollow", without submitting
# any data? To make this work, the form is going to be empty.
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('post', validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField('Submit Post')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
