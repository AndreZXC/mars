import datetime

from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired


class NewJobForm(FlaskForm):
    job = StringField('Название работы:', validators=[DataRequired()])
    teamlead = IntegerField('Айди тимлида:', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность:', validators=[DataRequired()])
    start_date = DateTimeLocalField('Начало:', default=datetime.datetime.now())
    completed = BooleanField('Завершено')
    collaborators = StringField('Участники (id):', validators=[DataRequired()])
    submit = SubmitField(label='Создать')