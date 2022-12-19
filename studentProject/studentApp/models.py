from datetime import datetime
from mimetypes import init
from sqlalchemy import ForeignKey
from studentApp import db
from flask_login import UserMixin
from studentApp import login 
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

# flask db stamp head
# flask db migrate
# flask db upgrade

class Client(db.Model):
    '''Client'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True)
    telephone = db.Column(db.String(11), index=True, unique=True)
    birth_date = db.Column(db.Date, index=True)
    description = db.Column(db.String(140))

class Car(db.Model):
    '''Car'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_number = db.Column(db.String(9), index=True, unique=True)
    name = db.Column(db.String(128), index=True)
    release_date = db.Column(db.Date, index=True)
    vin_code = db.Column(db.String(17), index=True, unique=True)
    brand = db.Column(db.String(15), index=True)
    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    description = db.Column(db.String(140))

class Employee(db.Model):
    '''Employee'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True)
    telephone = db.Column(db.String(11), index=True, unique=True)
    profession = db.Column(db.String(64), index=True)
    description = db.Column(db.String(140))

class Area(db.Model):
    '''Area'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))

class Service(db.Model):
    '''Service'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.String(12), index=True)
    description = db.Column(db.String(140))    

class Order(db.Model):
    '''Order'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, ForeignKey('car.client_id'))
    car_id = db.Column(db.Integer, ForeignKey('car.id'))
    employee_id = db.Column(db.Integer, ForeignKey('employee.id'))
    area_id = db.Column(db.Integer, ForeignKey('area.id'))
    date = db.Column(db.Date, index=True)
    expiration_date = db.Column(db.Date, index=True)

    def get_order_view(self):
        '''get order view'''
        return OrderView(
            id = self.id,
            client_name=Client.query.filter_by(id=self.client_id).first_or_404().name,
            car_number=Car.query.filter_by(id=self.car_id).first_or_404().car_number,
            employee_name=Employee.query.filter_by(id=self.employee_id).first_or_404().name,
            area_name=Area.query.filter_by(id=self.area_id).first_or_404().name,
            date=self.date,
            expiration_date=self.expiration_date
        )

class OrderView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(128), index=True)
    car_number = db.Column(db.String(9), index=True)
    employee_name = db.Column(db.String(128), index=True)
    area_name = db.Column(db.String(64), index=True)
    date = db.Column(db.Date, index=True)
    expiration_date= db.Column(db.Date, index=True)

class OrderingService(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, ForeignKey('order.id'))
    service_id = db.Column(db.Integer, ForeignKey('service.id'))
    quantity = db.Column(db.Integer, index=True)
    price = db.Column(db.String(15), index=True)

    def get_ordering_service_view(self):
        '''get_ordering_service_view'''
        return OrderingServiceView(
            id=self.id,
            service_name=Service.query.filter_by(id=self.service_id).first_or_404().name,
            quantity=self.quantity,
            price=self.price
        )

class OrderingServiceView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(64), index=True)
    quantity = db.Column(db.Integer, index=True)
    price = db.Column(db.Integer, index=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), index=True)
    

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        return True if self.role == "admin" else False

    def __repr__(self):
        return '<User {}>'.format(self.username)
