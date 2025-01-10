from flask import Blueprint, render_template
import subprocess
from app.models import Address, ContactInformation, EmergencyContact  # Fix the import path
from app import db

main = Blueprint('main', __name__)

def get_git_commit():
    try:
        commit_id = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
        return commit_id
    except Exception as e:
        print(f"Error getting git commit: {e}")
        return "unknown"

@main.route("/")
def home():
    apps = [
        {"name": "Employee Self Service", "icon": "bi-people", "url": "/ess"}
    ]
    app_version = get_git_commit()
    employee_id = "stefan.spiess"
    return render_template('index.html', apps=apps, app_version=app_version, employee_id=employee_id)

@main.route("/about")
def about():
    return "About the HR App."

# Example data for home route
def seed_example_data():
    # Address
    address = Address(
        employee_id="stefan.spiess",
        zip_code="12345",
        city="Example City",
        street="Example Street",
        house_number="42",
        concern_of="Home",
        is_emergency_contact=False
    )
    # Emergency Contact
    emergency_contact = Address(
        employee_id="stefan.spiess",
        zip_code="54321",
        city="Emergency City",
        street="Emergency Street",
        house_number="24",
        concern_of="Emergency",
        is_emergency_contact=True
    )
    contact_info = ContactInformation(
        address=emergency_contact,
        mobile_number="123-456-7890",
        landline_number="098-765-4321",
        email_address="example@example.com"
    )
    db.session.add_all([address, emergency_contact, contact_info])
    db.session.commit()

# Function to retrieve example data
def get_example_data():
    address = Address.query.filter_by(employee_id="stefan.spiess", is_emergency_contact=False).first()
    emergency_contact = Address.query.filter_by(employee_id="stefan.spiess", is_emergency_contact=True).first()
    if emergency_contact:
        contact_info = ContactInformation.query.filter_by(address_id=emergency_contact.id).first()
        emergency_contact = EmergencyContact(
            zip_code=emergency_contact.zip_code,
            city=emergency_contact.city,
            street=emergency_contact.street,
            house_number=emergency_contact.house_number,
            concern_of=emergency_contact.concern_of,
            contact_information=contact_info
        )
    return {
        "address": address,
        "emergency_contact": emergency_contact
    }
