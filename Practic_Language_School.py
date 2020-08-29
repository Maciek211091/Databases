from sqlalchemy import Integer, String, Column, Sequence, Date, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(bind=engine)


class Levels(Base):
    __tablename__ = 'levels'

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    courses = relationship("Courses", back_populates='levels')

    def __repr__(self):
        return f"Levels({self.id}, {self.name})"


class Languages(Base):
    __tablename__ = 'languages'

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String, nullable=False)

    courses = relationship("Courses", back_populates='languages')

    def __repr__(self):
        return f"Languages({self.id}, {self.name})"


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String, nullable=False)

    courses = relationship("Courses", back_populates='categories')

    def __repr__(self):
        return f"Categories({self.id}, {self.name})"


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    lessons = Column(Integer, nullable=False)
    description = Column(String)
    language_id = Column(Integer, ForeignKey('languages.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    level_id = Column(Integer, ForeignKey('levels.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    price = Column(Float)

    languages = relationship("Languages", back_populates='courses')
    categories = relationship("Categories", back_populates='courses')
    levels = relationship("Levels", back_populates='courses')

    def __repr__(self):
        return f"Courses({self.id}, {self.language}, {self.level}, {self.category})"


init_db()

LANG_DATA = (
    {"name": "English"},
    {"name": "German"},
    {"name": "Spanish"},
    {"name": "Italian"},
)

LEVELS_DATA = (
    {"name": "A0"},
    {"name": "A1"},
    {"name": "A2"},
    {"name": "B1"},
    {"name": "B2"},
    {"name": "C1"},
    {"name": "C2"},
)

CATEGORIES_DATA = (
    {"name": "Evening"},
    {"name": "Regular"},
    {"name": "Weekend"},
)

COURSE_DATA = (
    {
        "lessons": 56,
        "description": "Very nice",
        "price": 1000,
        "language_id": 1,
        "level_id": 1,
        "category_id": 1,
    },
    {
        "lessons": 65,
        "description": "Very very nice",
        "price": 10_000,
        "language_id": 2,
        "level_id": 2,
        "category_id": 2,
    },
    {
        "lessons": 560,
        "description": "Very well",
        "price": 100,
        "language_id": 3,
        "level_id": 3,
        "category_id": 3,
    },
    {
        "lessons": 5656,
        "description": "Good enough",
        "price": 123,
        "language_id": 1,
        "level_id": 2,
        "category_id": 3,
    },
)


def get_level_objects():
    return [Levels(**level) for level in LEVELS_DATA]


def create_levels():
    session.add_all(get_level_objects())
    session.commit()


def get_lang_objects():
    return [Languages(**lang) for lang in LANG_DATA]


def create_langs():
    session.add_all(get_lang_objects())
    session.commit()


def get_categories_objects():
    return [Categories(**category) for category in CATEGORIES_DATA]


def create_categories():
    session.add_all(get_categories_objects())
    session.commit()


def get_course_objects():
    return [Courses(**level) for level in COURSE_DATA]


def create_courses():
    session.add_all(get_course_objects())
    session.commit()


def create_basic_data():
    create_levels()
    create_langs()
    create_categories()
    create_courses()


create_basic_data()

res = engine.execute("Select * from Courses")

for i in res:
    print(i)
