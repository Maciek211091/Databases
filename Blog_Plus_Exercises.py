from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Sequence,
    ForeignKey,
    Float,
    Table, func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import re

engine = create_engine("sqlite:///:memory:")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(bind=engine)


# Table that will create many to many relationship between students and courses
student_course = Table(
    "student_course",
    Base.metadata,
    Column("courses_id", Integer, ForeignKey("courses.id")),
    Column("students_id", Integer, ForeignKey("students.id")),
)


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(Integer)

    courses = relationship(
        "Courses", secondary=student_course, back_populates="students"
    )

    def __repr__(self):
        return f"Student(id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name})"


class Levels(Base):
    __tablename__ = "levels"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    courses = relationship("Courses", back_populates="level")

    def __repr__(self):
        return f"Level(id: {self.id}, name: {self.name})"


class Languages(Base):
    __tablename__ = "languages"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    courses = relationship("Courses", back_populates="language")

    def __repr__(self):
        return f"Language(id: {self.id}, name: {self.name})"


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    courses = relationship("Courses", back_populates="category")

    def __repr__(self):
        return f"Category(id: {self.id}, name: {self.name})"


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    nr_of_lessons = Column(Integer, nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"))

    language = relationship("Languages", back_populates="courses")
    category = relationship("Categories", back_populates="courses")
    level = relationship("Levels", back_populates="courses")
    students = relationship(
        "Students", secondary=student_course, back_populates="courses"
    )

    def __repr__(self):
        return f"Course(id: {self.id}, level: {self.level}, lang: {self.language}, students: {self.students})"


create_tables()

LEVELS_DATA = (
    {"name": "A0"},
    {"name": "A1"},
    {"name": "A2"},
    {"name": "B1"},
    {"name": "B2"},
    {"name": "C1"},
    {"name": "C2"},
)

LANG_DATA = (
    {"name": "English"},
    {"name": "German"},
    {"name": "Spanish"},
    {"name": "Italian"},
)

CATEGORIES_DATA = (
    {"name": "Evening"},
    {"name": "Regular"},
    {"name": "Weekend"},
)

STUDENT_DATA = (
    {
        "first_name": "Jim",
        "last_name": "Jarmush",
        "email": "jim@jim.pl",
        "phone_number": 123123120,
    },
    {
        "first_name": "Wes",
        "last_name": "Anderson",
        "email": "wes@wes.pl",
        "phone_number": 124123129,
    },
    {
        "first_name": "Sergio",
        "last_name": "Leone",
        "email": "sergio@sergio.pl",
        "phone_number": 125123128,
    },
    {
        "first_name": "Martin",
        "last_name": "Scorsese",
        "email": "martin@martin.pl",
        "phone_number": 126123126,
    },
    {
        "first_name": "Martin",
        "last_name": "Luther",
        "email": "martin@luther.pl",
        "phone_number": 126123345,
    },
    {
        "first_name": "James",
        "last_name": "Scorsese",
        "email": "martin@james.pl",
        "phone_number": 12614545626,
    },
    {
        "first_name": "John",
        "last_name": "Locke",
        "email": "john@lockepl",
        "phone_number": 1245664126,
    },
    {
        "first_name": "Robert",
        "last_name": "Redford",
        "email": "john@locke .pl",
        "phone_number": 1289664126,
    },
    {
        "first_name": "John",
        "last_name": "Johnny",
        "email": "john @locke.pl",
        "phone_number": 1267664126,
    },
    {
        "first_name": "John",
        "last_name": "Silver",
        "email": "john@silver.pl",
        "phone_number": 1267664126,
    },
)

COURSE_DATA = (
    {
        "nr_of_lessons": 56,
        "description": "Very nice",
        "price": 1000,
        "language_id": 1,
        "level_id": 1,
        "category_id": 1,
    },
    {
        "nr_of_lessons": 65,
        "description": "Very very nice",
        "price": 10_000,
        "language_id": 2,
        "level_id": 2,
        "category_id": 2,
    },
    {
        "nr_of_lessons": 560,
        "description": "Very well",
        "price": 100,
        "language_id": 3,
        "level_id": 3,
        "category_id": 3,
    },
    {
        "nr_of_lessons": 5656,
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


def get_student_objects():
    return [Students(**level) for level in STUDENT_DATA]


def create_students():
    session.add_all(get_student_objects())
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
    create_students()


def assign_student_to_course(course, student):
    course.students.append(student)
    session.commit()


def assign_multiple_students_to_course(course, students):
    """
    course: Courses instance
    students: sequence e.g. list of Students instances
    """
    for student in students:
        course.students.append(student)
    session.commit()


def assign_course_to_student(student, course):
    student.courses.append(course)
    session.commit()


def assign_multiple_course_to_student(student, courses):
    """
    student: instance of Students class
    courses: sequence e.g. list of course instances
    """
    for course in courses:
        student.courses.append(course)
    session.commit()


create_basic_data()

# Select courses
students = session.query(Students).all()
english = session.query(Courses).filter(Courses.id == 1).one()
german = session.query(Courses).filter(Courses.id == 2).one()
spanish = session.query(Courses).filter(Courses.id == 3).one()
english_evening = session.query(Courses).filter(Courses.id == 4).one()
# Assign students to courses
assign_multiple_students_to_course(course=english, students=students)
assign_multiple_students_to_course(course=german, students=students[:8])
assign_multiple_students_to_course(course=spanish, students=students[:6])
assign_multiple_students_to_course(course=english_evening, students=students)


"""
ZADANIA

1. Utworzyć query które policzy nam ilość takich samych imion, query powinno zwrócić imię oraz liczbę wystąpień w 
tabeli (trzeba użyć subquery) ('Sergio', 1)

2. Utworzyć query które zwróci najbardziej popularny kurs

3. Utworzyć query które zwróci studentów z błędnym adresem email

"""
#
# # Zadanie 1
#
# res1 = session.query(func.count(Students.first_name), Students.first_name).group_by(Students.first_name).all()
#
# print(res1)
#
# # Zadanie 2
#
# res2 = session.query(func.count(student_course), Courses).join(Courses).group_by(Courses.id).all()
#
# for res in res2:
#     print(res)
#
# # Zadanie 3
#
# pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
#
# res3 = session.query(Students.email).all()
#
# for res in res3:
#     if not re.match(pattern, res[0]):
#         print(res)
#

query = session.query(Students.first_name).all()

def list_from_query(query):
    res = []
    for el in query:
        res.append(el[0])

    return res


a = list_from_query(query)

print(a)

