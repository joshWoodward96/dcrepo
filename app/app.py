from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init Database
db = SQLAlchemy(app)
# Init Marshmallow 
ma = Marshmallow(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    secondName = db.Column(db.String(100))
    email = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    district = db.Column(db.String(2))

    def __init__(self, firstName, secondName, email, occupation, district):
        self.firstName = firstName
        self.secondName = secondName
        self.email = email
        self.occupation = occupation
        self.district = district
    

# Employee Schema
class EmployeeSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'firstName', 'secondName', 'email', 'occupation', 'district')

# Initialise Schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Home
@app.route('/')
def home():
    return "Disease Control Employee Microservice."

# Return all employees
@app.route("/employees", methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    response = employees_schema.dump(all_employees)
    return jsonify(response)


# Return employee
@app.route("/employee/<id>", methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)


# Add employee
@app.route("/addEmployee", methods=['POST'])
def add_employee():

    firstName = request.json['firstName']
    secondName = request.json['secondName']
    email = request.json['email']
    occupation = request.json['occupation']
    district = request.json['district']

    new_employee = Employee(firstName, secondName, email, occupation, district)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)


# Delete employee
@app.route("/deleteEmployee/<id>", methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()

    return employee_schema.jsonify(employee)


# Edit employee
@app.route("/editEmployee/<id>", methods=['PUT'])
def edit_employee(id):
    employee = Employee.query.get(id)

    firstName = request.json['firstName']
    secondName = request.json['secondName']
    email = request.json['email']
    occupation = request.json['occupation']
    district = request.json['district']

    employee.firstName = firstName
    employee.secondName = secondName
    employee.email = email
    employee.occupation = occupation
    employee.district = district

    db.session.commit()

    return employee_schema.jsonify(employee)

# Establish if app is running
@app.route("/health")
def health():
     return jsonify(
         status="UP"
     )
    
if __name__ == "__main__":
    app.run(port=80, host='0.0.0.0')