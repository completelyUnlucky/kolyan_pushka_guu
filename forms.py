from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Вход')



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')


class RequestForm(FlaskForm):
    description = StringField('Описание заявки', validators=[DataRequired()])
    payment_amount = FloatField('Размер оплаты', validators=[DataRequired()])
    submit = SubmitField('Опубликовать заявку')

