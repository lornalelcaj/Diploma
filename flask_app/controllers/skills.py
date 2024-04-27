from flask_app import app  # type: ignore
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask import flash
from flask_app.models.employee import Employee # type: ignore
from flask_app.models.position import Position # type: ignore
from flask_app.models.skill import Skill # type: ignore

@app.route('/createskill', methods=['POST'])
def create_skill():
    if 'user_id' not in session:
        return redirect('/logout/')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
    }
    if Skill.validate_skill(data):
        Skill.create_skill(data)
        return redirect(request.referrer)
    else:
        print("error")
        return 