from sqlalchemy import create_engine, text, ForeignKey, func, exists
from sqlalchemy import Integer, String, Column, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, aliased, selectinload

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()

