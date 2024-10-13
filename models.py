from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # landlord, tenant, or admin
    properties = db.relationship('Property', backref='owner', lazy=True)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rent_amount = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    beds = db.Column(db.Integer, nullable=False)
    baths = db.Column(db.Integer, nullable=False)
    sqft = db.Column(db.Integer, nullable=False)
    legal_description = db.Column(db.String(500), nullable=True)
    dwelling_type = db.Column(db.String(50), nullable=False)  # Single Family, Duplex, etc.
    unit_number = db.Column(db.String(50), nullable=True)
    vacancy_status = db.Column(db.String(50), nullable=False)
    lease_term = db.Column(db.String(50), nullable=False)  # Lease term (12mo, 6mo, etc.)
    deposit = db.Column(db.Float, nullable=True)
    maintenance_schedule = db.Column(db.Text, nullable=True)
    maintenance_timestamp = db.Column(db.DateTime, nullable=True)
    documents = db.relationship('Document', backref='property', lazy=True)
    payments = db.relationship('Payment', backref='property', lazy=True)
    tenants = db.relationship('Tenant', backref='property', lazy=True)
    leases = db.relationship('LeaseAgreement', backref='property', lazy=True)

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    emergency_contact = db.Column(db.String(100), nullable=True)
    application_status = db.Column(db.String(50), nullable=True)
    background_check = db.Column(db.String(100), nullable=True)  # URL or path to background check document
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    lease = db.relationship('LeaseAgreement', backref='tenant', uselist=False)
    report_logs = db.relationship('TenantLog', backref='tenant', lazy=True)

class LeaseAgreement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    rent_amount = db.Column(db.Float, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    lease_history = db.relationship('LeaseHistory', backref='lease', lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    method = db.Column(db.String(50), nullable=False)  # Cash, Direct Deposit, Stripe
    payment_type = db.Column(db.String(50), nullable=False)  # Recurring, One-time, Tenant Release
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_url = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=True)
    document_type = db.Column(db.String(50), nullable=False)  # Lease, Maintenance, etc.

class PropertyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

class TenantLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)

class LeaseHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('lease_agreement.id'), nullable=False)
    modified_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    change_details = db.Column(db.Text, nullable=False)
