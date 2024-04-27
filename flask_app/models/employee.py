from flask_app.config.mysqlconnection import connectToMySQL # type: ignore
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PHONE_REGEX = re.compile(r'^(\+\d{1,3}\s?)?((\(\d{3}\))|\d{3})[\s.-]?\d{3}[\s.-]?\d{3,4}$')

from datetime import datetime, timedelta
from flask_app.models.position import Position


class Employee:
    db_name = 'diplome_db_final'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.hire_date = data['hire_date']
        self.department_name = data['department_name']
        self.role = data['role']
        self.status = data['status']
        self.phone = data['phone']
        self.photo = data['photo']


    @classmethod
    def create_employee(cls, data):
        
        proc = "add_employee"
        
        return connectToMySQL(cls.db_name).call_proc(proc, list(data.values()))
    

    @classmethod
    def get_employee_by_id(cls, data):
        query = "SELECT * FROM employees WHERE employyes.id = %(employee_id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0] 
    
    @classmethod
    def get_employee_role(cls, data):
        query = "SELECT role_id FROM employees WHERE employyes.id = %(employee_id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0] 

        
    @classmethod
    def get_all_employees_number(cls):
        query = "SELECT COUNT(*) FROM employees WHERE role_id!=2 "
        results = connectToMySQL(cls.db_name).query_db(query)
        employee_count = results[0]['COUNT(*)']
        print(employee_count)
        if results:
            return employee_count
        else:
            # Handle the case where the stored procedure call returns False
            print("Error: Failed to retrieve employees.")
            return 0
        
    @classmethod
    def get_all_applications_number(cls):
        query = "SELECT COUNT(*) FROM applications WHERE status='sent' "
        results = connectToMySQL(cls.db_name).query_db(query)[0]['COUNT(*)']
        print(results)
        if results:
            return results
        else:
            # Handle the case where the stored procedure call returns False
            print("Error: Failed to retrieve applications.")
            return 0


    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if Employee.email_exists(user['email']):
            flash("Email is already in use!", 'emailSignUp')
            is_valid = False
        if len(user['first_name']) < 3:
            flash("Name must be at least 3 characters.", 'name')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name be at least 3 characters.", 'lastName')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'passwordRegister')
            is_valid = False
        elif not any(c.isupper() for c in user['password']):
            flash("Password must contain at least one uppercase letter.", 'passwordRegister')
            is_valid = False
        elif not any(c.islower() for c in user['password']):
            flash("Password must contain at least one lowercase letter.", 'passwordRegister')
            is_valid = False
        elif not any(c.isdigit() for c in user['password']):
            flash("Password must contain at least one digit.", 'passwordRegister')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("Password do not match!", 'passwordConfirm')
            is_valid = False
        return is_valid
    
    @classmethod
    def email_exists(cls, email):
        query = "SELECT COUNT(*) FROM employees WHERE email = %(email)s"
        result = connectToMySQL(cls.db_name).query_db(query, {'email': email})
        print(result[0]['COUNT(*)'])
        return result[0]['COUNT(*)'] > 0


    @staticmethod
    def validate_employee(employee):
        is_valid = True
        if not EMAIL_REGEX.match(employee['email']): 
            print("Invalid email address!", 'emailSignUp')
            is_valid = False
        if Employee.email_exists(employee['email']):
            flash("Email is already in use!", 'emailSignUp')
            print('ekz')
            is_valid = False
        if len(employee['first_name']) < 3:
            print("Name must be at least 3 characters.", 'name')
            is_valid = False
        if len(employee['last_name']) < 3:
            print("Last name be at least 3 characters.", 'lastName')
            is_valid = False
        if len(employee['password']) < 8:
            print("Password must be at least 8 characters.", 'passwordRegister')
            is_valid = False
        elif not any(c.isupper() for c in employee['password']):
            print("Password must contain at least one uppercase letter.", 'passwordRegister')
            is_valid = False
        elif not any(c.islower() for c in employee['password']):
            print("Password must contain at least one lowercase letter.", 'passwordRegister')
            is_valid = False
        elif not any(c.isdigit() for c in employee['password']):
            print("Password must contain at least one digit.", 'passwordRegister')
            is_valid = False
        if datetime.strptime(employee['birthday'], "%Y-%m-%d") > datetime.now():
            print(f"Birthday cannot be in the future.", 'birthday')
            is_valid = False
        elif datetime.strptime(employee['birthday'], "%Y-%m-%d")  > datetime.now() - timedelta(days=365*16):  # jo me pak se 16 vjec
            print("Employee must be at least 100 years old.", 'birthday')
            is_valid = False
        if datetime.strptime(employee['hire_date'], "%Y-%m-%d") > datetime.now():
            print(f"Hire date cannot be in the future.", 'hire_date')
            is_valid = False
        if int(Position.get_salary_per_position(employee['position'])['max_salary'] )<int(employee['salary'])< int (Position.get_salary_per_position(employee['position'])['min_salary']):
            print(f"Salary cannot be out of range.", 'salary')
            is_valid = False
        if not PHONE_REGEX.match(employee['phone']): 
            print("Invalid phone number!", 'phone')
            is_valid = False 
        
        return is_valid


    @classmethod
    def get_employee_by_email(cls, data):
        query= 'SELECT * FROM employees WHERE employees.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]
    
    