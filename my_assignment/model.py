import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

#SQL DB Section
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

###Models###
##User Model
class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

##Company Model
class Company(db.Model):

    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    postal_code = db.Column(db.String(20), nullable=False)

    #one to many relationship
    usage = db.relationship('Usage', backref='companies')
    energy = db.relationship('Energy', backref='companies')
    waste = db.relationship('Waste', backref='companies')
    businessTravel = db.relationship('BusinessTravel', backref='companies')


    def __init__(self, name, address, sector, contact_person, email, postal_code):
        self.name = name
        self.address = address
        self.sector = sector
        self.contact_person = contact_person
        self.email = email
        self.postal_code = postal_code

#Usage model
class Usage(db.Model):
    
    __tablename__ = 'usage'
    
    id = db.Column(db.Integer, primary_key=True)
    energy = db.Column(db.Float, nullable=False)
    waste = db.Column(db.Float, nullable=False)
    fuel = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    month = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False)

    #foreign key
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __init__(self, energy, waste, fuel, result, month, year, company_id):
        self.energy = energy
        self.waste = waste
        self.fuel = fuel
        self.result = result
        self.month = month
        self.year = year
        self.company_id = company_id

#Energy usage model
class Energy(db.Model):

    __tablename__ = "energy"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False) 
    e_bill = db.Column(db.Float, nullable=False)
    g_bill = db.Column(db.Float, nullable=False)
    f_bill = db.Column(db.Float, nullable=False)

    #foreign key
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __init__(self, month, year, e_bill, g_bill, f_bill, company_id):
        self.month = month
        self.year = year
        self.e_bill = e_bill
        self.g_bill = g_bill
        self.f_bill = f_bill
        self.company_id = company_id

#Waste model
class Waste(db.Model):

    __tablename__ = "waste"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False) 
    g_waste = db.Column(db.Float, nullable=False)
    r_waste = db.Column(db.Float, nullable=False)

    #foreign key
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __init__(self, month, year, g_waste, r_waste, company_id):
        self.month = month
        self.year = year
        self.e_bill = g_waste
        self.r_waste = r_waste
        self.company_id = company_id

#Business Travel Model
class BusinessTravel(db.Model):
    
    __tablename__ = "businessTravel"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False) 
    b_travel = db.Column(db.Float, nullable=False)
    avg_fuel = db.Column(db.Float, nullable=False)

    #foreign key
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __init__(self, month, year, b_travel, avg_fuel, company_id):
        self.month = month
        self.year = year
        self.b_travel = b_travel
        self.avg_fuel = avg_fuel
        self.company_id = company_id    

with app.app_context():
    db.create_all()
