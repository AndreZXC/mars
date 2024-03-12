import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import datetime as dt
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    lead = orm.relationship('User')
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    categories = orm.relationship("Category", secondary="association", backref="jobs")

    def dates(self, start=dt.datetime.now()):
        self.start_date = start
        self.end_date = self.start_date + dt.timedelta(hours=self.work_size)
