from flask_app import app  # type: ignore
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask import flash
from flask_app.models.employee import Employee # type: ignore
from flask_app.models.position import Position # type: ignore
from flask_app.models.skill import Skill # type: ignore
from flask_app.models.departament import Departament # type: ignore

@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('log_in.html')


@app.route('/register', methods=['POST'])
def create_applicant():
    if not Employee.validate_user(request.form):
        flash('Somethings wrong ninja!', 'signUp')
        return redirect(request.referrer)
    
    if Employee.get_employee_by_email(request.form):
        flash('My friend, this email already exists! What are you trying to do?!! Hack me?!', 'email')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8'), # Decode the hashed password
        'departament_name': ' ',
        'role': 'Applicant'
    }
    Employee.create_employee(data)
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'email')
        return redirect(request.referrer)
    if not Employee.get_employee_by_email(data):
        flash('This email doesnt exist in this application', 'email')
        return redirect(request.referrer)

    employee = Employee.get_employee_by_email(data)

    if not bcrypt.check_password_hash(employee['password'], request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'password')
        return redirect(request.referrer)
        
    session['user_id'] = employee['id']
    return redirect('/')


@app.route('/')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        all_emp=Employee.get_all_employees_number()
        all_dep=Departament.get_all_departaments_number()
        app_apl=Employee.get_all_applications_number()
        vacancy_positions=Position.get_all_vacancy_positions()
        return render_template('test.html', all_emp=all_emp, all_dep=all_dep, vacancy_positions=vacancy_positions, app_apl=app_apl)
    return redirect('/logout')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/loginPage')

@app.route('/addemployee')
def add_employee():
    if 'user_id' not in session:
        return redirect('/logout/')
    dep=Departament.get_all_departaments()
    positions=Position.get_all_vacancy_positions_names()
    return render_template('add_employee.html', dep=dep, positions=positions)


@app.route('/registeremployee', methods=['POST'])
def register_employee():
    print(request.form)
    if not Employee.validate_employee(request.form):
         flash('Somethings wrong ninja!', 'add_employee')
         print('went wrong')
         return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'birthday': request.form['birthday'],
        'hire_date': request.form['hire_date'],
        'phone': request.form['phone'],
        'departament': int(request.form['departament']),
        'role': 'Employee',
        'position' : int(request.form['position']),
        'salary': request.form['salary'],
        'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8'), # Decode the hashed password
        'status': 'Employeed'

    }
    print(data)
    Employee.create_employee(data)
    return redirect('/')




