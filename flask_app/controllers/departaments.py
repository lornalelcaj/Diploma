from flask_app import app  # type: ignore
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask import flash
from flask_app.models.employee import Employee # type: ignore
from flask_app.models.position import Position # type: ignore
from flask_app.models.skill import Skill # type: ignore
from flask_app.models.departament import Departament # type: ignore

@app.route('/departaments')
def show_departaments():
    departments=Departament.get_employees_per_departament()
    no_of_emp_per_dep = Departament.get_number_of_employee_per_departament()
    return render_template('departaments.html',  departments_data=departments, no_of_emp_per_dep=no_of_emp_per_dep )