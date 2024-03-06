from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Электронная почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль:', validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    age = IntegerField('Ваш возраст:', validators=[DataRequired()])
    speciality = StringField('Специальность:', validators=[DataRequired()])
    position = StringField('Должность:', validators=[DataRequired()])
    address = StringField('Модуль проживания:', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')