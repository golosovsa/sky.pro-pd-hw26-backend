import datetime
from random import randint

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, func, Integer, BigInteger

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

KeyType = Integer


class Base(db.Model):
    __abstract__ = True

    created = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.datetime.now() - datetime.timedelta(minutes=randint(0, 100_000))
    )
    updated = Column(DateTime, default=func.now(), onupdate=func.now())


class BaseWithID(Base):
    __abstract__ = True

    id = Column(KeyType, primary_key=True, autoincrement=True)


class BaseManyToMany(Base):
    __abstract__ = True
