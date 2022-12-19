'''forms'''
from socketserver import DatagramRequestHandler
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField, DateField, SelectField, IntegerField, PasswordField, FieldList, FormField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class AddClientForm(FlaskForm):
    '''AddClientForm'''
    name = StringField('Name', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired()])
    birth_date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    submit = SubmitField('Conifirm')

class AddCarForm(FlaskForm):
    '''AddCarForm'''
    name = StringField('Name', validators=[DataRequired()])
    car_number = StringField('Car Number', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    vin_code = StringField('Vin_code', validators=[DataRequired()])
    release_date = DateField('Release_date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    submit = SubmitField('Confirm')

class AddAreaForm(FlaskForm):
    '''AddAreaForm'''
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    submit = SubmitField('Confirm')

class AddEmployeeForm(FlaskForm):
    '''AddEmployeeForm'''
    name = StringField('Name', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired()])
    profession = StringField('Profession', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    submit = SubmitField('Confirm')

class AddServiceForm(FlaskForm):
    '''AddServieForm'''
    name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=200)])
    submit = SubmitField('Confirm')

class AddOrderForm(FlaskForm):
    '''AddOrderForm'''
    client_car = SelectField('Client car', validators=[DataRequired()])
    employee = SelectField('Employee name', validators=[DataRequired()])
    area = SelectField('Area name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    expiration_date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SelectClientForm(FlaskForm):
    client_telephone = SelectField('Client telephone', validators=[DataRequired()])
    submit = SubmitField('Ok')

class AddOrderingServiceForm(FlaskForm):
    service_name = SelectField('Service', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Ok')

class SearchForm(FlaskForm):
    '''SearchForm'''
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class FilterForm(FlaskForm):    
    name = StringField("Filter", render_kw={"placeholder": "----placeholder"})

class FiltersForm(FlaskForm):
    name = StringField('FiltersForm-Name', validators=[Optional()])    
    filters = FieldList(FormField(FilterForm))
    submit = SubmitField('Search')

class AdvancedFilterForm(FlaskForm):
    name = StringField("Filter column:", render_kw={'readonly': True, 'border': 0})    
    operation = SelectField("Operation:", choices=[
        ('=', 'equal'), 
        ('<', 'less'), 
        ('>', 'greater'), 
        ('between', 'between'),
        ('not between', 'not between'),
        ('>=', 'greater or equal'),
        ('<=', 'less or equal'),
        ('<>', 'not equal'),
        ('in', 'in'),
        ('not in', 'not in'),
        ('like', 'like'),
        ('not like', 'not like')
    ])
    value = StringField("Value:", render_kw={"placeholder": 'type parameters'})


class AdvancedFiltersForm(FlaskForm):
    name = HiddenField('FitltersForm-Name', validators=[Optional()])
    filters = FieldList(FormField(AdvancedFilterForm))
    submit = SubmitField('Search')
    