# sqlalchemy Example based on https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# adapted to use PostgreSQL instead of SQLite3


import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    fname = Column(String(250), nullable=False)
    lname = Column(String(250), nullable=False)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('postgresql://postgres:mysecret@posgres:5432/mydatabase')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a Person in the person table
new_person = Person(fname='John', lname='Cleese')
session.add(new_person)
session.commit()

new_person = Person(fname='Graham', lname='Chapman')
session.add(new_person)
session.commit()

new_person = Person(fname='Terry', lname='Gilliam')
session.add(new_person)
session.commit()

new_person = Person(fname='Eric', lname='Idle')
session.add(new_person)
session.commit()

new_person = Person(fname='Michael', lname='Palin')
session.add(new_person)
session.commit()

new_person = Person(fname='Terry', lname='Jones')
session.add(new_person)
session.commit()
