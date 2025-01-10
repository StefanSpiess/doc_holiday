from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Address, SalaryHistory
import subprocess

ess = Blueprint('ess', __name__)

def get_git_commit():
    try:
        commit_id = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
        return commit_id
    except Exception as e:
        print(f"Error getting git commit: {e}")
        return "unknown"

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
    return render_template('ess/dashboard.html', data=data, employee_id=employee_id, app_version=get_git_commit())

@ess.route('/update/<string:object_type>', methods=['GET', 'POST'])
def update(object_type):
    employee_id = "stefan.spiess"
    print(f"Updating {object_type} for employee_id: {employee_id}")

    if request.method == 'POST':
        if object_type == 'address':
            new_address = request.form['address']
            address = Address.query.filter_by(employee_id=employee_id, is_emergency_contact=False).first()
            if address:
                address.address = new_address
            else:
                address = Address(employee_id=employee_id, address=new_address, is_emergency_contact=False)
                db.session.add(address)
        elif object_type == 'emergency_contact':
            new_contact = request.form['emergency_contact']
            emergency_contact = Address.query.filter_by(employee_id=employee_id, is_emergency_contact=True).first()
            if emergency_contact:
                emergency_contact.address = new_contact
            else:
                emergency_contact = Address(employee_id=employee_id, address=new_contact, is_emergency_contact=True)
                db.session.add(emergency_contact)
        elif object_type == 'salary':
            year = request.form['year']
            salary = request.form['salary']
            new_salary_entry = SalaryHistory(employee_id=employee_id, year=year, salary=salary)
            db.session.add(new_salary_entry)

        db.session.commit()
        print("Update successful")
        return redirect(url_for('ess.dashboard'))

    return render_template(f'ess/update_{object_type}.html', employee_id=employee_id, app_version=get_git_commit())

@ess.route('/update/salary', methods=['GET', 'POST'])
def update_salary():
    employee_id = "stefan.spiess"
    if request.method == 'POST':
        if 'delete' in request.form:
            entry_id = request.form['delete']
            entry = SalaryHistory.query.get(entry_id)
            if entry:
                db.session.delete(entry)
        elif 'edit_id' in request.form:
            entry_id = request.form['edit_id']
            entry = SalaryHistory.query.get(entry_id)
            if entry:
                entry.year = request.form['year']
                entry.salary = request.form['salary']
        else:
            year = request.form['year']
            salary = request.form['salary']
            new_salary_entry = SalaryHistory(employee_id=employee_id, year=year, salary=salary)
            db.session.add(new_salary_entry)

        db.session.commit()
        return redirect(url_for('ess.update_salary'))

    salary_history = SalaryHistory.query.filter_by(employee_id=employee_id).order_by(SalaryHistory.year.desc()).all()
    return render_template('ess/update_salary.html', salary_history=salary_history, employee_id=employee_id, app_version=get_git_commit())
