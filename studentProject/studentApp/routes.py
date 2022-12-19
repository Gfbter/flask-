# from pickletools import read_unicodestring1
import collections
from dataclasses import dataclass
from sqlalchemy import or_,and_, not_
from studentApp import app, db
from flask_login import current_user, login_user, logout_user, login_required
from studentApp.forms import AddCarForm, AddClientForm, AddOrderForm, AddOrderingServiceForm, SelectClientForm, AddAreaForm, AddEmployeeForm, AddServiceForm, SearchForm, LoginForm, RegistrationForm, FiltersForm, AdvancedFiltersForm
from studentApp.models import Client, Car, Area, Employee, OrderingService, Service, Order, OrderView, User
from flask import render_template, redirect, url_for, request
from studentApp.FilterParser import parse_filter

#, request, flash



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    title="Sign In"
    if current_user.is_authenticated:
        return redirect(url_for('order'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('order')
        return redirect(url_for('order'))

    return render_template('login.html', title=title, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))    

@app.route('/register', methods=['GET', 'POST'])
def register():
    title="Register"
    if current_user.is_authenticated:
        return redirect(url_for('order'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role="user")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title=title, form=form)
    
#  list(filter(lambda x: getattr(x, 'id') > 2 and 'Deer' in getattr(x, 'name'), clients))
@app.route('/client_list', methods=['GET', 'POST'])
@login_required
def client():
    title = "client list"
    clients = Client.query.all()
    filter = collections.namedtuple('Filter', ['name', 'value', 'operation'])
    filters = {
        'name': 'AdvancedFiltersForm',
        'filters': [
            filter('name', '', 0), 
            filter('telephone', '', 0), 
            filter('birth_date', '', 0)
        ]
    }
    form = AdvancedFiltersForm(data=filters)
    flag = False if current_user.role != "admin" else True 
    return render_template('client_list.html', title=title, clients=clients, form=form, flag=flag)

@app.route('/client/car_list/<int:client_id>')
@login_required
def car(client_id):
    title="car list"
    client = Client.query.filter_by(id=client_id).first_or_404()
    filter = collections.namedtuple('Filter', ['name', 'value', 'operation'])
    filters = {
        'name': 'AdvancedFiltersForm',
        'filters': [
            filter('car_number', '', 0), 
            filter('name', '', 0), 
            filter('release_date', '', 0),
            filter('vin_code', '', 0),
            filter('brand', '', 0)
        ]
    }
    form = AdvancedFiltersForm(data=filters)
    flag = False if current_user.role != "admin" else True
    cars = Car.query.filter_by(client_id=client_id).all()
    return render_template('car_list.html', title=title, form=form, cars=cars, client_name=client.name, client_id=client_id, flag=flag)

@app.route('/areas')
@login_required
def area():
    title="area list"
    filter = collections.namedtuple('Filter', ['name', 'value', 'operation'])
    filters = {
        'name': 'AdvancedFiltersForm',
        'filters': [
            filter('name', '', 0)
        ]
    }
    form = AdvancedFiltersForm(data=filters)
    flag = False if current_user.role != "admin" else True
    areas = Area.query.all()
    return render_template('area_list.html', form=form, title=title, areas=areas, flag=flag)

@app.route('/employees')
@login_required
def employee():
    title="employee list"
    filter = collections.namedtuple('Filter', ['name', 'value', 'operation'])
    filters = {
        'name': 'AdvancedFiltersForm',
        'filters': [
            filter('name', '', 0), 
            filter('telephone', '', 0), 
            filter('profession', '', 0)
        ]
    }
    form = AdvancedFiltersForm(data=filters)
    flag = False if current_user.role != "admin" else True
    employees = Employee.query.all()
    return render_template('employee_list.html', form=form, title=title, employees=employees, flag=flag)

@app.route('/services')
@login_required
def service():
    title="service list"
    filter = collections.namedtuple('Filter', ['name', 'value', 'operation'])
    filters = {
        'name': 'AdvancedFiltersForm',
        'filters': [
            filter('name', '', 0), 
            filter('price', '', 0)
        ]
    }
    form = AdvancedFiltersForm(data=filters)
    flag = False if current_user.role != "admin" else True
    services = Service.query.all()
    return render_template('service_list.html', form=form, title=title, services=services, flag=flag)

@app.route('/order')
@login_required
def order():
    title = "order list"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True
    orders = []
    for order in Order.query.all():
        orders.append(order.get_order_view())

    return render_template('order_list.html', title=title, form=form, orders=orders, flag=flag)

@app.route('/ordering_service/<int:order_id>')
@login_required
def ordering_service(order_id):
    title = "ordering service list"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True
    ordering_services = [] 
    for ordering_service in OrderingService.query.filter_by(order_id=order_id).all():
        ordering_services.append(ordering_service.get_ordering_service_view())
    return render_template('ordering_service_list.html', form=form, title=title, ordering_services=ordering_services, order_id=order_id, flag=flag)

@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    title = "add client"
    if current_user.role != "admin":
        return redirect(url_for('client'))
    form = AddClientForm()
    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            telephone=form.telephone.data, 
            birth_date=form.birth_date.data, 
            description=form.description.data
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('client'))
    return render_template('add_client.html', form=form, title=title)

@app.route('/add_car/<int:client_id>', methods=['GET', 'POST'])
@login_required
def add_car(client_id):
    title = "add car"
    if current_user.role != "admin":
        return redirect(url_for('car'))
    form = AddCarForm()
    if form.validate_on_submit():
        car = Car(
            name=form.name.data, 
            car_number=form.car_number.data,
            release_date=form.release_date.data, 
            vin_code=form.vin_code.data, 
            brand=form.brand.data, 
            client_id=client_id, 
            description=form.description.data
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('car', client_id=client_id))
    return render_template("add_car.html", form=form, title=title)

@app.route('/add_area', methods=['GET', 'POST'])
@login_required
def add_area():
    title = "add area"
    if current_user.role != "admin":
        return redirect(url_for('area'))
    form = AddAreaForm()
    if form.validate_on_submit():
        area = Area(
            name=form.name.data, 
            description=form.description.data
        )
        db.session.add(area)
        db.session.commit()
        return redirect(url_for('area'))
    return render_template("add_area.html", form=form, title=title)

@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    title = "add employee"
    if current_user.role != "admin":
        return redirect(url_for('employee'))
    form = AddEmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            name=form.name.data,
            telephone=form.telephone.data,
            profession=form.profession.data, 
            description=form.description.data
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('employee'))
    return render_template('add_employee.html', form=form, title=title)

@app.route('/add_service', methods=['GET', 'POST'])
@login_required
def add_service():
    title = "add service"
    if current_user.role != "admin":
        return redirect(url_for('service'))
    form = AddServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            price=form.price.data, 
            description=form.description.data
        )
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('service'))
    return render_template('add_service.html', form=form, title=title)

@app.route('/add_order/<int:client_id>', methods=['GET', 'POST'])
@login_required
def add_order(client_id):
    title = "Add Order"
    if current_user.role != "admin":
        return redirect(url_for('order'))
    form = AddOrderForm()
    employee_list = [(employee.id, employee.name) for employee in Employee.query.all()]
    area_list = [(area.id, area.name) for area in Area.query.all()]
    form.employee.choices = employee_list
    form.area.choices = area_list
    car_list = None
    car_list = [(car.id, car.car_number) for car in Car.query.filter_by(client_id=client_id).all()]
    form.client_car.choices = car_list
    
    if form.validate_on_submit():
        order = Order(
            client_id=client_id,
            car_id=form.client_car.data,
            employee_id=form.employee.data,
            area_id=form.area.data, 
            date=form.date.data,
            expiration_date=form.expiration_date.data
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('order'))
    return render_template('add_order.html', title=title, form=form)

@app.route('/select_client', methods=['GET', 'POST'])
@login_required
def select_client():
    title = 'select client'
    form = SelectClientForm()
    if current_user.role != "admin":
        return redirect(url_for('order'))
    client_list = [(client.id, client.telephone) for client in Client.query.all()]
    form.client_telephone.choices = client_list
    if form.validate_on_submit():
        return redirect(url_for('add_order', client_id=request.form['client_telephone']))
    return render_template('select_client.html', title=title, form=form)

@app.route('/add_ordering_service/<int:order_id>', methods=['GET', 'POST'])
@login_required
def add_ordering_service(order_id):
    title = "add ordering service"
    if current_user.role != "admin":
        return redirect(url_for('ordering service'))
    form = AddOrderingServiceForm()
    service_name = [(service.id, service.name) for service in Service.query.all()]
    form.service_name.choices = service_name
    if form.validate_on_submit():
        ordering_service = OrderingService(
            order_id=order_id,
            service_id=form.service_name.data,
            quantity=form.quantity.data,
            price=form.price.data
        )
        db.session.add(ordering_service)
        db.session.commit()
        return redirect(url_for('ordering_service', order_id=order_id))
    return render_template('add_ordering_service.html', form=form, title=title, order_id=order_id)

@app.route('/client/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    title = "edit client"
    if current_user.role != "admin":
        return redirect(url_for('client'))
    if current_user.role != "admin":
        return redirect(url_for('order'))
    client = Client.query.filter_by(id=id).first_or_404()
    form = AddClientForm()
    if form.validate_on_submit():
        client.name = form.name.data
        client.telephone = form.telephone.data
        client.birth_date = form.birth_date.data
        client.description = form.description.data
        db.session.commit()
        return redirect(url_for('client'))
    return render_template('edit_client.html', form=form, title=title, client=client)

@app.route('/car/<int:client_id>/<int:car_id>', methods=['GET', 'POST'])
@login_required
def edit_car(client_id, car_id):
    title = "edit car"
    if current_user.role != "admin":
        return redirect(url_for('car'))
    car = Car.query.filter_by(id=car_id).first_or_404()
    form = AddCarForm()
    if form.validate_on_submit():
        car.name = form.name.data
        car.car_number = form.car_number.data
        car.brand = form.brand.data
        car.vin_code = form.vin_code.data
        car.release_date = form.release_date.data
        car.description = form.description.data
        db.session.commit()
        return redirect(url_for('car', client_id=client_id))
    return render_template('edit_car.html', form=form, title=title, car=car)

@app.route('/area/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_area(id):
    title = "edit area"
    if current_user.role != "admin":
        return redirect(url_for('area'))
    area = Area.query.filter_by(id=id).first_or_404()
    form = AddAreaForm()
    if form.validate_on_submit():
        area.name = form.name.data
        area.description = form.description.data
        db.session.commit()
        return redirect(url_for('area'))
    return render_template('edit_area.html', form=form, title=title, area=area)

@app.route('/employee/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    title = "edit employee"
    if current_user.role != "admin":
        return redirect(url_for('employee'))
    employee = Employee.query.filter_by(id=id).first_or_404()
    form = AddEmployeeForm()
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.telephone = form.telephone.data
        employee.profession = form.profession.data
        employee.description = form.description.data
        db.session.commit()
        return redirect(url_for('employee'))
    return render_template('edit_employee.html', form=form, title=title, employee=employee)

@app.route('/service/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    title = "edit service"
    if current_user.role != "admin":
        return redirect(url_for('service'))
    service = Service.query.filter_by(id=id).first_or_404()
    form = AddServiceForm()
    if form.validate_on_submit():
        service.name = form.name.data
        service.price = form.price.data
        service.description = form.description.data
        db.session.commit()
        return redirect(url_for('service'))
    return render_template('edit_service.html', form=form, title=title, service=service)

@app.route('/order/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    title = "edit order"
    if current_user.role != "admin":
        return redirect(url_for('order'))
    form = AddOrderForm()
    order = Order.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        order.date = form.name.data
        order.expiration_date = form.expiration_date.data
        db.session.commit()
        return redirect(url_for('order'))
    return render_template('edit_order.html', form=form, title=title, order=order)

@app.route('/ordering_service/<int:order_id>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ordering_service(id, order_id):
    title = "edit order"
    if current_user.role != "admin":
        return redirect(url_for('ordering service'))
    form = AddOrderForm()
    order = Order.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        order.date = form.name.data
        order.expiration_date = form.expiration_date.data
        db.session.commit()
        return redirect(url_for('order'))
    return render_template('edit_order.html', form=form, title=title, order=order)

@app.route('/delete_client/<int:id>')
@login_required
def delete_client(id):
    title = "client list"
    Client.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('client')) 

@app.route('/delete_car/<int:client_id>/<int:car_id>')
@login_required
def delete_car(client_id, car_id):
    title = "car list"
    Car.query.filter_by(id=car_id).delete()
    db.session.commit()
    return redirect(url_for('car', client_id=client_id))
    
@app.route('/delete_area/<int:id>')
@login_required
def delete_area(id):
    # title = "client_list"
    Area.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('area'))    

@app.route('/delete_employee/<int:id>')
@login_required
def delete_employee(id):
    title = "employee list"
    Employee.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('employee')) 

@app.route('/delete_service/<int:id>')
@login_required
def delete_service(id):
    title = "service list"
    Service.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('service'))  

@app.route('/delete_order/<int:id>')
@login_required
def delete_order(id):
    title = "order list"
    if current_user.role != "admin":
        return redirect(url_for('order'))
    Order.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('order')) 

@app.route('/delete_ordering_service/<int:order_id>/<int:id>')
@login_required
def delete_ordering_service(id, order_id):
    title = "ordering service"
    OrderingService.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('ordering_service', order_id=order_id))

@app.route('/client_search', methods=['GET', 'POST'])
@login_required
def client_search():
    title = "client search"    
    form = AdvancedFiltersForm()
    flag = False if current_user.role != "admin" else True
    if form.validate_on_submit():
        filter_list = []        
        for value in form.filters.data:
            if value['value'] != '':
                filter_list.append(parse_filter(Client, value['name'], value['value'], value['operation']))
        for filter in filter_list:
            print(filter)
    if len(filter_list) > 0:
        clients = db.session.query(Client).filter(and_(*filter_list)).all()
    else:
        clients = Client.query.all()
    return render_template('client_list.html', title=title, clients=clients, form=form, flag=flag)

@app.route('/car_search/<int:client_id>', methods=['GET', 'POST'])
@login_required
def car_search(client_id):
    title = "car_search"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True 
    cars = Car.query.all()
    client = Client.query.filter_by(id=client_id).first_or_404()
    if form.validate_on_submit():
        filter_list = []        
        for value in form.filters.data:
            if value['value'] != '':
                filter_list.append(parse_filter(Client, value['name'], value['value'], value['operation']))
        for filter in filter_list:
            print(filter)
    if len(filter_list) > 0:
        cars = db.session.query(Client).filter(and_(*filter_list)).all()
    else:
        cars = Client.query.all()
    return render_template('car_list.html', title=title, client_id=client_id, client_name=client.name, cars=cars, form=form, flag=flag)

@app.route('/area_search', methods=['GET', 'POST'])
@login_required
def area_search():
    title = "area search"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True 
    areas = Area.query.all()
    if form.validate_on_submit():
        filter_list = []        
        for value in form.filters.data:
            if value['value'] != '':
                filter_list.append(parse_filter(Client, value['name'], value['value'], value['operation']))
        for filter in filter_list:
            print(filter)
    if len(filter_list) > 0:
        areas = db.session.query(Client).filter(and_(*filter_list)).all()
    else:
        areas = Client.query.all()        
    return render_template('area_list.html', title=title, areas=areas, form=form, flag=flag)

@app.route('/employee_search', methods=['GET', 'POST'])
@login_required
def employee_search():
    title = "employee search"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True 
    employees = Employee.query.all()
    if form.validate_on_submit():
        filter_list = []        
        for value in form.filters.data:
            if value['value'] != '':
                filter_list.append(parse_filter(Client, value['name'], value['value'], value['operation']))
        for filter in filter_list:
            print(filter)
    if len(filter_list) > 0:
        employees = db.session.query(Client).filter(and_(*filter_list)).all()
    else:
        employees = Client.query.all()        
    return render_template('employee_list.html', title=title, employees=employees, form=form, flag=flag)

@app.route('/service_search', methods=['GET', 'POST'])
@login_required
def service_search():
    title = "service search"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True 
    services = Service.query.all()
    if form.validate_on_submit():
        filter_list = []        
        for value in form.filters.data:
            if value['value'] != '':
                filter_list.append(parse_filter(Client, value['name'], value['value'], value['operation']))
        for filter in filter_list:
            print(filter)
    if len(filter_list) > 0:
        services = db.session.query(Client).filter(and_(*filter_list)).all()
    else:
        srevices = Client.query.all()        
    return render_template('service_list.html', title=title, services=services, form=form, flag=flag)   

@app.route('/order_search', methods=['GET', 'POST'])
@login_required
def order_search():
    title = "service search"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True 
    if form.validate_on_submit():
        name = '%' + form.name.data + '%'
        if name != None:
            orders = Order.query.filter(Order.client_id.like(Client.query.filter(Client.name.like(name)).first_or_404().id))
            order_view = []
            for order in orders:
                order_view.append(order.get_order_view())
        return render_template('order_list.html', form=form, title=title, orders=order_view, flag=flag)
    return redirect(url_for('order'))

@app.route('/ordering_service_search/<int:order_id>', methods=['GET', 'POST'])
@login_required
def ordering_service_search(order_id):
    title = "ordering service search"
    form = SearchForm()
    flag = False if current_user.role != "admin" else True 
    if form.validate_on_submit():
        name = '%' + form.name.data + '%'
        if name != None:
            ordering_services = OrderingService.query.filter(OrderingService.service_id.like(Service.query.filter(Service.name.like(name)).first_or_404().id))
            ordering_service_view = []
            for ordering_service in ordering_services:
                ordering_service_view.append(ordering_service.get_ordering_service_view())
        return render_template('ordering_service_list.html', form=form, title=title, ordering_services=ordering_service_view, order_id=order_id, flag=flag)
    return redirect(url_for('ordering_service', order_id=order_id))    

