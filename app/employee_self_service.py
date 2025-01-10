from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Address, ContactInformation, SalaryHistory

# Define Blueprint
ess = Blueprint('ess', __name__)

@ess.route('/')
def dashboard():
    employee_id = "stefan.spiess"
    address = Address.query.filter_by(employee_id=employee_id, is_emergency_contact=False).first()
    emergency_contact = Address.query.filter_by(employee_id=employee_id, is_emergency_contact=True).first()
    salary_history = SalaryHistory.query.filter_by(employee_id=employee_id).order_by(SalaryHistory.year.desc()).all()

    data = {
        "address": address,
        "emergency_contact": emergency_contact,
        "salary_history": salary_history
    }
    return render_template('ess/dashboard.html', data=data)

@ess.route('/update/<string:object_type>', methods=['GET', 'POST'])
def update(object_type):
    employee_id = "stefan.spiess"

    if request.method == 'POST':
        if object_type == 'address':
            new_data = {
                "street": request.form['street'],
                "house_number": request.form['house_number'],
                "zip_code": request.form['zip_code'],
                "city": request.form['city'],
                "concern_of": request.form['concern_of']
            }
            address = Address.query.filter_by(employee_id=employee_id, is_emergency_contact=False).first()
            if address:
                for key, value in new_data.items():
                    setattr(address, key, value)
            else:
                address = Address(employee_id=employee_id, is_emergency_contact=False, **new_data)
                db.session.add(address)
        elif object_type == 'emergency_contact':
            new_data = {
                "street": request.form['street'],
                "house_number": request.form['house_number'],
                "zip_code": request.form['zip_code'],
                "city": request.form['city'],
                "concern_of": request.form['concern_of']
            }
            contact_data = {
                "mobile_number": request.form['mobile_number'],
                "landline_number": request.form.get('landline_number'),
                "email_address": request.form['email_address']
            }
            emergency_contact = Address.query.filter_by(employee_id=employee_id, is_emergency_contact=True).first()
            if emergency_contact:
                for key, value in new_data.items():
                    setattr(emergency_contact, key, value)
                contact_info = ContactInformation.query.filter_by(address_id=emergency_contact.id).first()
                if contact_info:
                    for key, value in contact_data.items():
                        setattr(contact_info, key, value)
                else:
                    contact_info = ContactInformation(address=emergency_contact, **contact_data)
                    db.session.add(contact_info)
            else:
                emergency_contact = Address(employee_id=employee_id, is_emergency_contact=True, **new_data)
                db.session.add(emergency_contact)
                contact_info = ContactInformation(address=emergency_contact, **contact_data)
                db.session.add(contact_info)
        db.session.commit()
        return redirect(url_for('ess.dashboard'))

    return render_template(f'ess/update_{object_type}.html')
