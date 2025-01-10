from flask import Blueprint, render_template, request, redirect, url_for
from app import db
import jsonify
from app.models import ObjectModel, Entry  # Replace with your actual model name

# Define the Quality Checks Blueprint
quality_checks = Blueprint('quality_checks', __name__)

# Route to display all entries
@quality_checks.route('/entries')
def list_entries():
    entries = Entry.query.all()
    return render_template('quality_checks/list_entries.html', entries=entries)

# Route to create a new entry
@quality_checks.route('/entries/new', methods=['POST'])
def new_entry():
    related_object_id = request.form.get('related_object_id')
    title = request.form.get('title')
    description = request.form.get('description')

    # Validate that the related_object_id exists
    if not related_object_id:
        return "Error: Related object is required.", 400
    
    # Validate other fields if necessary
    if not title or not description:
        return "Error: Title and description are required.", 400

    # Create and save the new entry
    entry = Entry(related_object_id=related_object_id, title=title, description=description)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('quality_checks.list_entries'))

@quality_checks.route('/search_objects')
def search_objects():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    # Query the database for matching objects
    objects = ObjectModel.query.filter(ObjectModel.name.ilike(f"%{query}%")).all()
    
    # Convert objects to JSON format
    matching_objects = [{"id": obj.id, "name": obj.name} for obj in objects]
    return jsonify(matching_objects)
