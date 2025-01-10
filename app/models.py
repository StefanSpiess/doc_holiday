from app import db

class SalaryHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.String(50), nullable=False)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10))
    city = db.Column(db.String(50))
    street = db.Column(db.String(100))
    house_number = db.Column(db.String(10))
    concern_of = db.Column(db.String(50))
    is_emergency_contact = db.Column(db.Boolean, default=False)
    contact_information = db.relationship("ContactInformation", backref="address", uselist=False)

class ContactInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    mobile_number = db.Column(db.String(15))
    landline_number = db.Column(db.String(15))
    email_address = db.Column(db.String(100))

class EmergencyContact(Address):
    contact_information = db.relationship("ContactInformation", backref="emergency_contact", uselist=False)