from sqlalchemy import orm
import sqlalchemy
from .db_session import SqlAlchemyBase


class Depart(SqlAlchemyBase):
    __tablename__ = "depart"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           autoincrement=True,
                           primary_key=True)

    creator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('jobs.id'))
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # user = orm.relation('User')
    # jobs = orm.relation('Jobs')
