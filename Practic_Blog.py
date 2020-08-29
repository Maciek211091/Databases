from sqlalchemy import Integer, String, Column, Sequence, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    nickname = Column(String)

    post = relationship("Post", back_populates='user')


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates='post')
    post_keyword = relationship("Post_Keyword", back_populates='post')


class Post_Keyword(Base):
    __tablename__ = 'post_keyword'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    keyword_id = Column(Integer, ForeignKey("keyword.id"))

    post = relationship("Post", back_populates='post_keyword')
    keyword = relationship("Keyword", back_populates='post_keyword')


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    word = Column(String, nullable=False)

    post_keyword = relationship("Post_Keyword", back_populates='keyword')


init_db()