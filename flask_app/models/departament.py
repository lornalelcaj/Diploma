from flask_app.config.mysqlconnection import connectToMySQL # type: ignore
from flask import flash



class Departament:
    db_name = 'diplome_db_final'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    @classmethod
    def get_all_departaments_number(cls):
        query = "SELECT COUNT(*) FROM departaments where id!=3 "
        results = connectToMySQL(cls.db_name).query_db(query)[0]['COUNT(*)']
        if results:
            return results
        else:
            # Handle the case where the stored procedure call returns False
            print("Error: Failed to retrieve departaments.")
            return 0
        
    @classmethod
    def get_all_departaments(cls):
        query = "SELECT id, name FROM departaments WHERE id != 3"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        if results:
            return [{'id': result['id'], 'name': result['name']} for result in results]
        else:
            return None
        
    @classmethod
    def get_number_of_employee_per_departament(cls):
        query = "SELECT d.name AS department_name, COUNT(e.id) AS num_employees FROM departaments d LEFT JOIN employees e ON d.id = e.departament_id WHERE d.id != 3 GROUP BY d.name; "
        results = connectToMySQL(cls.db_name).query_db(query)
        employyes_per_departament= []
        if results:
            for row in results:
                employyes_per_departament.append(row)
            print(  employyes_per_departament)
            return employyes_per_departament 
        else:
            # Handle the case where the stored procedure call returns False
            print("Error: Failed to retrieve employees.")
            return []
        
    @classmethod
    def get_departament_id(cls, data):
        query = "SELECT id FROM departaments WHERE departaments.name = %(departament)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(result [0]['id'])
        return result[0]['id']
    
    @classmethod
    def get_employees_per_departament(cls):
        query= "SELECT  d.name AS department_name, e.id, e.first_name, e.last_name, e.birthday, e.hire_date, p.name AS position_name FROM  departaments d LEFT JOIN employees e ON d.id = e.departament_id LEFT JOIN positions p ON e.position_id = p.id WHERE e.departament_id != 3 OR e.departament_id IS NULL ORDER BY d.name, e.last_name; "
        results = connectToMySQL(cls.db_name).query_db(query)
        departments = {}
        if results:
            for row in results:
                department_name = row['department_name']
                if department_name not in departments:
                    departments[department_name] = []
                departments[department_name].append(row)
            return departments
        else:
            # Handle the case where the stored procedure call returns False
            print("Error: Failed to retrieve employees.")
            return {}
    