from flask_app import app  # type: ignore
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask import flash
import json
from flask_app.models.employee import Employee # type: ignore
from flask_app.models.position import Position # type: ignore
from flask_app.models.skill import Skill # type: ignore
from flask_app.models.departament import Departament # type: ignore

@app.route('/addposition')
def addposition():
    if 'user_id' not in session:
        return redirect('/logout/')
    dep=Departament.get_all_departaments()
    skills=Skill.get_all_skills()
    return render_template('add_position.html', dep=dep, skills=skills)

@app.route('/createposition' , methods=['POST'])
def create_position():
    print("hyriii")    
    if 'user_id' not in session:
        return redirect('/logout/')
    dep_id=Departament.get_departament_id(data = {'departament': request.form['departament']})
    print("hyriii")
    data = {
        'name': request.form['name'],
        'departament_id': dep_id,
        'min_salary': request.form['min_salary'],
        'max_salary': request.form['max_salary'],
        'status': request.form['status']
    }
    print(data)
    skills=request.form.getlist('skills[]')
    print(skills)
    if Position.validate_position(data) and skills:
        Position.create_position(data, skills)
        return redirect(request.referrer)


