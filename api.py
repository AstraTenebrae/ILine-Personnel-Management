from flask import Flask, render_template, request
from database import Employee, db
from functions import sorting

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/employees'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


API_ROUTE = '/api/v1'
EMPLOYEES_API_ROUTE = '/employees'


@app.route(EMPLOYEES_API_ROUTE, methods=['GET'])
def read_all():
    query = Employee.query
    
    page = request.args.get(key='page', default=1, type=int)
    size = request.args.get(key='size', default=20, type=int)
    query = sorting(query, model=Employee)
    employees = query.paginate(
        page=page, 
        per_page=size,
        max_per_page=100,
        error_out=False,
    )
    return render_template("all_employees.html", employees=employees, title='all employees')


with app.app_context():
    db.create_all()