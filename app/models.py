from app import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    is_emergency_contact = db.Column(db.Boolean, default=False)

class SalaryHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.String(50), nullable=False)