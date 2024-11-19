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
    postal_code = db.Column(db.Integer, nullable=False)

    #one to many relationship
    usage = db.relationship('Usage', backref='companies')

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

with app.app_context():
    db.create_all()
