from sqlalchemy import Column, Table, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

association_table = Table('subscriptions', Base.metadata,
    Column('user_email', String(80), ForeignKey('user.email')),
    Column('event_id', Integer, ForeignKey('event.id'))
)


class User(Base):
    __tablename__ = 'user'
    email = Column(String(80), primary_key=True)
    subscriptions = relationship('Event', secondary=association_table, backref='subscribers')

    @property
    def serialize(self):
        return {
            'email': self.email
        }


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    location = Column(String(20), nullable=False)
    start = Column(String(20), nullable=False)
    end = Column(String(20), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'start': self.start,
            'end': self.end,
            'subscribers': [user.email for user in self.subscribers]

        }

engine = create_engine('sqlite:///event.db')
Base.metadata.create_all(engine)
