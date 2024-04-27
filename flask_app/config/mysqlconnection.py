# a cursor is the object we use to interact with the database
import pymysql.cursors  # type: ignore
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 

    def call_proc(self, proc_name, args=None):
        with self.connection.cursor() as cursor:
            try:
                if args:
                    # If args are provided, use proper syntax for calling a stored procedure with arguments
                    placeholders = ','.join(['%s'] * len(args))
                    query = f"CALL {proc_name}({placeholders})"
                    print("Calling procedure with args:", query, args)
                    cursor.execute(query, args)
                else:
                    # If no args, just call the stored procedure without passing any parameters
                    query = f"CALL {proc_name}()"
                    print("Calling procedure:", query)
                    cursor.callproc(proc_name)
                # Fetch the result after executing the stored procedure
                result = cursor.fetchall()
                print("Procedure result:", result)
                return result
            except Exception as e:
                print("Error calling stored procedure:", e)
                return False
            
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)