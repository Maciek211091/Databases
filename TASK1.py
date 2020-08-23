from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')

engine.execute("CREATE TABLE Users(id int, name varchar, nickname varchar)")

users = [(1, "Roman", 'magneton_bora'), (2, "Sam", 'big_daddy'), (3, "Sara", "lovely_kitty")]


def add_users(engine, users_list):
    results = []
    for (user_id, name, nickname) in users_list:
        result = engine.execute(f"INSERT INTO Users VALUES('{user_id}', '{name}', '{nickname}')")
        results.append(result)
    return results


add_users(engine, users)

result = engine.execute("SELECT * FROM Users")

for user in result:
    print(f"{user.id}, {user.name}, {user.nickname}")

# func that creates sql table - very simple to be modified


def create_table(sql_query):
    engine.execute(sql_query)


create_table(f'CREATE TABLE Salary(id int primary key, salary_grade varchar(10))')
create_table(f'CREATE TABLE Localization(id int primary key, name varchar(20))')
create_table(f'CREATE TABLE Departments(id int primary key, name varchar(20))')
create_table(f'CREATE TABLE Employees(id int primary key, Name varchar(30), Department varchar(30), '
             f'Localization varchar(20), Salary varchar(10), FOREIGN KEY(Department) REFERENCES Departments(id), '
             f'FOREIGN KEY(Salary) REFERENCES Salary(id), FOREIGN KEY(Localization) REFERENCES Localization(id))')


loc_list = [(1, "Kraków"), (2, "Warszawa"), (3, "Gdańsk")]
dep_list = [(1, "Finances"), (2, "IT"), (3, "CTO")]
sal_list = [(1, "3000-5000"), (2, "4000-6000"), (3, "5000-7000")]
emp_list = [(1, "Maciej Lesiak", 2, 1, 3), (2, "Krzysztof Lesiak", 1, 2, 2)]

for (loc_id, loc) in loc_list:
    engine.execute(f"INSERT INTO Localization VALUES('{loc_id}', '{loc}')")

for (dep_id, name) in dep_list:
    engine.execute(f"INSERT INTO Departments VALUES('{dep_id}', '{name}')")

for (sal_id, val) in sal_list:
    engine.execute(f"INSERT INTO Salary VALUES('{sal_id}', '{val}')")

for (emp_id, name, dep, loc, sal) in emp_list:
    engine.execute(f"INSERT INTO Employees VALUES('{emp_id}', '{name}', '{dep}', '{loc}', '{sal}')")

query = engine.execute("Select * from Employees e join Salary s on e.Salary=s.id")
for res in query:
    print(res)
