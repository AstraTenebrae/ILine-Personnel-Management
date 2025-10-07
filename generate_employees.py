# generate_data.py
from mimesis import Person, Datetime
from mimesis.enums import Locale
import random
from database import db, Employee
from sqlalchemy import text

def generate_employees():
    db.session.query(Employee).delete()
    db.session.execute(text("ALTER SEQUENCE employee_id_seq RESTART WITH 1"))
    db.session.commit()
    
    person = Person(Locale.RU)
    datetime_gen = Datetime()
    employees = []
    ceo = Employee(
        fullname=person.full_name(),
        position='CEO',
        date=datetime_gen.datetime(2010, 2015),
        salary=random.uniform(300000, 500000),
        manager_id=None
    )
    employees.append(ceo)
    db.session.add(ceo)
    db.session.commit()
    
    counts = {
        'Manager': 4,
        'Team Lead': 50, 
        'Senior Developer': 500,
        'Developer': 50000
    }
    managers_by_position = {
        'CEO': [ceo],
        'Manager': [],
        'Team Lead': [],
        'Senior Developer': [],
        'Developer': []
    }


    for _ in range(counts['Manager']):
        manager = Employee(
            fullname=person.full_name(),
            position='Manager',
            date=datetime_gen.datetime(2015, 2020),
            salary=random.uniform(350000, 450000),
            manager_id=ceo.id
        )
        employees.append(manager)
        managers_by_position['Manager'].append(manager)
        db.session.add(manager)
    db.session.commit()
    
    for _ in range(counts['Team Lead']):
        manager = random.choice(managers_by_position['Manager'])
        team_lead = Employee(
            fullname=person.full_name(),
            position='Team Lead',
            date=datetime_gen.datetime(2018, 2021),
            salary=random.uniform(250000, 350000),
            manager_id=manager.id
        )
        employees.append(team_lead)
        managers_by_position['Team Lead'].append(team_lead)
        db.session.add(team_lead)
    db.session.commit()
    
    for _ in range(counts['Senior Developer']):
        manager = random.choice(managers_by_position['Team Lead'])
        senior_dev = Employee(
            fullname=person.full_name(),
            position='Senior Developer',
            date=datetime_gen.datetime(2019, 2022),
            salary=random.uniform(150000, 250000),
            manager_id=manager.id
        )
        employees.append(senior_dev)
        managers_by_position['Senior Developer'].append(senior_dev)
        db.session.add(senior_dev)    
    db.session.commit()
    
    for _ in range(counts['Developer']):
        manager = random.choice(managers_by_position['Senior Developer'])
        developer = Employee(
            fullname=person.full_name(),
            position='Developer',
            date=datetime_gen.datetime(2020, 2023),
            salary=random.uniform(50000, 150000),
            manager_id=manager.id
        )
        employees.append(developer)
        db.session.add(developer)    
    db.session.commit()


    print(f"База заполнена! Всего сотрудников: {len(employees)}")

if __name__ == '__main__':
    from api import app
    with app.app_context():
        generate_employees()