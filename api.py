from flask import Flask, render_template, request, redirect, url_for
from database import Employee, db, positions
from functions import sorting, full_searching, partial_searching

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/employees'

db.init_app(app)


API_ROUTE = '/api/v1'
EMPLOYEES_API_ROUTE = '/employees'


@app.route(EMPLOYEES_API_ROUTE+'/', methods=['GET'])
def read_all():
    try:
        query = Employee.query
        page = request.args.get(key='page', default=1, type=int)
        size = request.args.get(key='size', default=20, type=int)
        query = sorting(query, model=Employee)
        query = full_searching(query, model=Employee)
        query = partial_searching(query, model=Employee)
        employees = query.paginate(
            page=page, 
            per_page=size,
            max_per_page=100,
            error_out=True,
        )
        return render_template("all_employees.html", employees=employees, title='all employees'), 200
    except Exception as e:
        return f"Ошибка: {str(e)}", 400

@app.route(EMPLOYEES_API_ROUTE+'/<int:id>/', methods=['GET'])
def read_one(id):
    employee = db.get_or_404(Employee, id)
    return render_template("one_employee.html", employee=employee, title=f'employee id:{id}'), 200


@app.route(API_ROUTE+EMPLOYEES_API_ROUTE+'/<int:id>/edit', methods=['POST'])
def change_manager(id):
    try:
        employee = db.get_or_404(Employee, id)        
        new_manager_id = int(request.form['manager'])

        if new_manager_id == id:
            return "Ошибка: сотрудник не может быть своим начальником", 400
        new_manager = Employee.query.get(new_manager_id)
        if not new_manager:
            return "Ошибка: начальник не найден", 400
        current_position_index = positions.index(employee.position)
        new_manager_position_index = positions.index(new_manager.position)    
        if new_manager_position_index != current_position_index - 1:
            return f"Ошибка: начальник должен быть на одну ступень выше.", 400

        employee.manager_id = new_manager_id
        db.session.commit()
        return redirect(url_for("read_one", id=employee.id)), 200
    except Exception as e:
        db.session.rollback()
        return f"Ошибка: {str(e)}", 400

with app.app_context():
    db.create_all()