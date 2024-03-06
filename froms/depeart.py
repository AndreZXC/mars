from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class DepartamentForm(FlaskForm):
    title = StringField('Название департамента:', validators=[DataRequired()])
    email = EmailField('Почта департамента:', validators=[DataRequired()])
    chief = IntegerField('Id главы:', validators=[DataRequired()])
    members = StringField('Участники:')
    submit = SubmitField('Подтвердить')