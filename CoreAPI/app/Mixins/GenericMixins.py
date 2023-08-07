from sqlalchemy import Column, BigInteger, func
from sqlalchemy.ext.declarative import declared_attr
from submodule_models_3kle import db
from typing import TypeVar
T = TypeVar('T')


class GenericMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(BigInteger, default=func.extract('epoch', func.current_timestamp()))

    @declared_attr
    def last_updated(cls):
        return db.Column(BigInteger, default=func.extract('epoch', func.current_timestamp()), onupdate=func.extract('epoch', func.current_timestamp()))

    def to_dict(cls):
        return {column.name: getattr(cls, column.name) for column in cls.__table__.columns}

    def update_table(cls, updates: dict):
        valid_attributes = [column.key for column in cls.__table__.columns]

        valid_updates = {key: value for key, value in updates.items() if key in valid_attributes}

        for key, value in valid_updates.items():
            setattr(cls, key, value)

        db.session.commit()
        return valid_updates
    
    def save(cls, refresh: bool=False):
        db.session.add(cls)
        db.session.commit()

        if refresh:
            db.session.refresh(cls)



