from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('landlord', 'Landlord'), ('tenant', 'Tenant')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class PropertyForm(FlaskForm):
    name = StringField('Property Name', validators=[DataRequired(), Length(max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    rent_amount = FloatField('Rent Amount', validators=[DataRequired(), NumberRange(min=0)])
    beds = IntegerField('Number of Bedrooms', validators=[DataRequired(), NumberRange(min=0)])
    baths = FloatField('Number of Bathrooms', validators=[DataRequired(), NumberRange(min=0)])
    sqft = IntegerField('Square Footage', validators=[DataRequired(), NumberRange(min=0)])
    dwelling_type = SelectField('Dwelling Type', choices=[
        ('single_family', 'Single Family'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('duplex', 'Duplex'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    lease_term = SelectField('Lease Term', choices=[
        ('month_to_month', 'Month-to-Month'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years')
    ], validators=[DataRequired()])
    vacancy_status = SelectField('Vacancy Status', choices=[
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Property')
