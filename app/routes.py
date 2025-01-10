from flask import Blueprint, render_template
import subprocess

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
