import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, PropertyForm, TenantForm
from models import db, User, Property, Tenant, LeaseAgreement

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', properties=properties)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        new_property = Property(
            name=form.name.data,
            address=form.address.data,
            rent_amount=form.rent_amount.data,
            beds=form.beds.data,
            baths=form.baths.data,
            sqft=form.sqft.data,
            dwelling_type=form.dwelling_type.data,
            lease_term=form.lease_term.data,
            vacancy_status=form.vacancy_status.data,
            owner_id=current_user.id
        )
        db.session.add(new_property)
        db.session.commit()
        flash('Property added successfully!', 'success')
        return redirect(url_for('property_detail', property_id=new_property.id))
    return render_template('add_property.html', form=form)

@app.route('/property/<int:property_id>')
@login_required
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    tenant_form = TenantForm()
    return render_template('property_detail.html', property=property, form=tenant_form)

@app.route('/property/<int:property_id>/add_tenant', methods=['POST'])
@login_required
def add_tenant(property_id):
    property = Property.query.get_or_404(property_id)
    form = TenantForm()
    if form.validate_on_submit():
        new_tenant = Tenant(
            name=form.name.data,
            contact_email=form.contact_email.data,
            phone_number=form.phone_number.data,
            emergency_contact=form.emergency_contact.data,
            application_status=form.application_status.data,
            property_id=property.id
        )
        db.session.add(new_tenant)
        
        new_lease = LeaseAgreement(
            start_date=form.lease_start.data,
            end_date=form.lease_end.data,
            rent_amount=form.rent_amount.data,
            tenant_id=new_tenant.id,
            property_id=property.id
        )
        db.session.add(new_lease)
        
        if form.background_check.data:
            # Handle file upload (you may want to save it to a specific location)
            filename = secure_filename(form.background_check.data.filename)
            form.background_check.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_tenant.background_check = filename

        db.session.commit()
        flash('Tenant added successfully!', 'success')
        return redirect(url_for('property_detail', property_id=property.id))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('property_detail', property_id=property.id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
