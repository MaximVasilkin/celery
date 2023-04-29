import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Task(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)

