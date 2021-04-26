import datetime
import sqlalchemy

from data.db_session import SqlAlchemyBase


class Objects(SqlAlchemyBase):
    __tablename__ = 'objects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    device = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_working = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
