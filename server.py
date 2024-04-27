from flask_app import app
from flask_app.controllers import employees
from flask_app.controllers import skills
from flask_app.controllers import positions
from flask_app.controllers import departaments


if __name__=="__main__":
    app.run(debug=True) 
     