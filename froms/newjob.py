import datetime
from data.db_session import create_session, global_init
from data.category import Category
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField, IntegerField, DateTimeLocalField
from wtforms import SelectField
from wtforms.validators import DataRequired


class NewJobForm(FlaskForm):
    job = StringField('Название работы:', validators=[DataRequired()])
    teamlead = IntegerField('Айди тимлида:', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность:', validators=[DataRequired()])
    start_date = DateTimeLocalField('Начало:', default=datetime.datetime.now())
    completed = BooleanField('Завершено')
    collaborators = StringField('Участники (id):', validators=[DataRequired()])
    global_init('db/users.db')
    sess = create_session()
    cats = [item.name for item in sess.query(Category).all()]
    category = SelectField('Категория:', choices=(cats + ['NoneType']))
    submit = SubmitField(label='Создать')