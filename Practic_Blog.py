from sqlalchemy import Integer, String, Column, Sequence, create_engine, ForeignKey, Table
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
    comments = relationship("Comments", back_populates='user')

    def __init__(self, first_name, nickname):
        self.first_name = first_name
        self.nickname = nickname

    def __repr__(self):
        return f"User({self.id}, {self.first_name}, {self.nickname})"


# tworzenie tabeli pomocniczej - nie trzeba w klasie jeśli nie potrzebujemy dodawać wartości
post_keyword = Table('post_keywords', Base.metadata, Column('post_id', ForeignKey('post.id'), primary_key=True),
                     Column('keyword_id', ForeignKey('keyword.id'), primary_key=True))


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    comments_list = Column(String)
    likes = Column(Integer)

    user = relationship("User", back_populates='post')
    keyword = relationship("Keyword", secondary=post_keyword, back_populates='post')
    comments = relationship("Comments", back_populates='post')

    def __init__(self, author, title, content, likes=0):
        self.author = author
        self.title = title
        self.content = content
        self.likes = likes

    def give_like(self):
        self.likes += 1

    def __repr__(self):
        return f"Post({self.id}, {self.title}, likes {self.likes})"


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    keyword = Column(String, nullable=False)

    post = relationship("Post", secondary=post_keyword, back_populates='keyword')

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return f"Keyword({self.id}, {self.keyword})"


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    comment_content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates='comments')
    post = relationship("Post", back_populates='comments')


init_db()


def create_user(name: str, nickname: str):

    print(f"Creating user {nickname}")

    return User(name, nickname)


def create_post(user, title, content):
    print(f"Creating post titled: {title}")

    return Post(user, title, content)


def list_from_query(query):
    res = []
    for el in query:
        res.append(el[0])

    return res


'''
to be changed into CLI app
'''