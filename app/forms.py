from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={'class':'form-control form-class'})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={'class':'form-control form-class'})
    remember_me = BooleanField('Remember Me',render_kw={})
    submit = SubmitField('Sign In',render_kw={'class':' btn btn-primary'})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={'class':'form-control form-class'})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={'class':'form-control form-class'})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={'class':'form-control form-class'})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')],render_kw={'class':'form-control form-class'})
    user_role=RadioField('Role',validators=[DataRequired()] ,choices=[('Teacher','Teacher'),('Student','Student')],render_kw={'class':'form-control form-class'})
    submit = SubmitField('Register',render_kw={'class':'btn btn-primary'})

    def validate_username(self, username):
        user_ = user.query.filter_by(username=username.data).first()
        if user_ is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user_ = user.query.filter_by(email=email.data).first()
        if user_ is not None:
            raise ValidationError('Please use a different email address.')


