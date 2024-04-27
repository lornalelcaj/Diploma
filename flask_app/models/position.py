from flask_app.config.mysqlconnection import connectToMySQL # type: ignore
from flask import flash
import json


class Position:
    db_name = 'diplome_db_final'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.departament_id = data['departament_id']
        self.min_salary = data['min_salary']
        self.max_salary = data['max_salary']
        self.status = data['status']

    @classmethod    
    def create_position(cls, data, skills):
        try:
            # Convert skills list to a comma-separated string
            skills_str = ','.join(skills)
            
            # Call the stored procedure
            result = connectToMySQL(cls.db_name).call_proc('create_position_and_skills', args=(data['name'], data['departament_id'], data['min_salary'], data['max_salary'], data['status'], skills_str))
            
            if result:
                print("Position and skills created successfully!")
                return True
            else:
                print("Failed to create position and skills.")
                return False
        except Exception as e:
            print("Error creating position and skills:", e)
            return False



    
    @classmethod
    def get_all_vacancy_positions(cls):
        query = "SELECT COUNT(*) FROM positions WHERE status='Unoccupied' "
        results = connectToMySQL(cls.db_name).query_db(query)[0]['COUNT(*)']
        print(results)
        if results:
            return results
        else:
            # Handle the case where the stored procedure call returns False
            print("Error: Failed to retrieve employees.")
            return 0


    @classmethod
    def get_all_vacancy_positions_names(cls):
        query = "SELECT positions.id, positions.name FROM positions JOIN departaments ON positions.departament_id = departaments.id WHERE positions.status = 'Unoccupied' "
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        if results:
            return [{'id': result['id'], 'name': result['name']} for result in results]
        else:
            return None

    @staticmethod
    def validate_position(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.", 'name')
            is_valid = False
        if int (data['min_salary'])> int(data['max_salary']) :
            flash("error.", 'max_salary')
            is_valid = False
        if not data['status'] :
            flash("error.", 'max_salary')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_salary_per_position(cls, position_id):
        query = "SELECT min_salary, max_salary FROM positions WHERE positions.id = %(position_id)s"
        result = connectToMySQL(cls.db_name).query_db(query, {'position_id': position_id})
        return  result[0]
