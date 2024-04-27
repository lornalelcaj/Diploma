from flask_app.config.mysqlconnection import connectToMySQL # type: ignore
from flask import flash



class Skill:
    db_name = 'diplome_db_final'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']

    @classmethod
    def create_skill(cls, data):
        query = "INSERT INTO skills ( name, description) VALUES (  %(name)s, %(description)s);"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
    @staticmethod
    def validate_skill(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.", 'name')
            is_valid = False
        if len(data['description']) < 5:
            flash("description be at least 5 characters.", 'description')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all_skills(cls):
        query = "SELECT id, name FROM skills"
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            return [{'id': result['id'], 'name': result['name']} for result in results]
        else:
            return None