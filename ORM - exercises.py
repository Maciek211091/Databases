from sqlalchemy import create_engine, text, ForeignKey
from sqlalchemy import Integer, String, Column, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='addresses')

    def __repr__(self):
        return f"Address(email_address={self.email_address})"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f"User({self.name}, {self.fullname}, {self.nickname})"


User.addresses = relationship('Address', order_by=Address.id, back_populates='user')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

edward = User(name='Ed', fullname='Edward Johns', nickname='big_daddy')

session.add(edward)

session.commit()

# engine.execute('select * from users').fetchall()

session.add_all([
    User(name="Sam", fullname='Sam More', nickname='sammy12'),
    User(name='Joe', fullname='Joe Smith', nickname='js21')])

session.commit()

jack = User(name='Jack', fullname='Jack Doe', nickname='jc123')

print(jack.addresses)

jack.addresses = [Address(email_address='jack.doe@gmail.com')]

print(jack.addresses)

print(jack.addresses[0].user)

session.add(jack)
session.commit()
'''
results = engine.execute('select * from users').fetchall()

for res in results:
    print(res)

for user in session.query(User).order_by(User.id.desc()):
    print(user)

for user in session.query(User).filter(User.id==1):
    print(user)

for user in session.query(User).filter_by(id=1):
    print(user)

query = "SELECT id, fullname, nickname, FROM users where id=:id"
stmt = text(query)
stmt = stmt.columns(User.id, User.fullname, User.nickname)
session.query(User).from_statement(stmt).params(id=42).all()

'''