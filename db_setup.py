# import the necessary tools and define Base

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Define the classes for the database


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):
    '''The table to hold all the category names and ids'''

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return the formatted object data"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    '''The table to hold all the details of the items'''
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return the formatted object data"""
        return {
            'title': self.title,
            'id': self.id,
            'description': self.description,
        }

# Go for engine


engine = create_engine('sqlite:///content.db')
Base.metadata.create_all(engine)
