from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.equipment import Equipment, MaintenanceRecord
from datetime import datetime
from flask import current_app
from sqlalchemy import or_

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # Get search parameters
    search_query = request.args.get('search', '')
    search_category = request.args.get('category', '')
    search_location = request.args.get('location', '')
    search_status = request.args.get('status', '')

    # Base query
    equipment_query = Equipment.query

    # Apply search filters
    if search_query:
        equipment_query = equipment_query.filter(
            or_(
                Equipment.name.ilike(f'%{search_query}%'),
                Equipment.serial_number.ilike(f'%{search_query}%'),
                Equipment.notes.ilike(f'%{search_query}%')
            )
        )
    
    if search_category:
        equipment_query = equipment_query.filter_by(category=search_category)
    
    if search_location:
        equipment_query = equipment_query.filter_by(location=search_location)
    
    if search_status:
        equipment_query = equipment_query.filter_by(status=search_status)

    # Get filtered equipment
    filtered_equipment = equipment_query.all()
    
    # Get total equipment count
    equipment_count = Equipment.query.count()
    
    # Get equipment counts by category
    equipment_by_category = {}
    for category in current_app.config['EQUIPMENT_CATEGORIES'].keys():
        count = Equipment.query.filter_by(category=category).count()
        equipment_by_category[category] = count
    
    # Get equipment requiring maintenance (either status is maintenance or next_maintenance is due)
    maintenance_needed = Equipment.query.filter(
        (Equipment.status == 'maintenance') |
        (Equipment.next_maintenance <= datetime.utcnow().date())
    ).count()
    
    # Get out of service equipment count
    out_of_service = Equipment.query.filter_by(status='out_of_service').count()
    
    # Get recent maintenance records
    recent_maintenance = MaintenanceRecord.query.order_by(
        MaintenanceRecord.maintenance_date.desc()
    ).limit(5).all()

    # Get unique locations for dropdown
    locations = sorted(set(equipment.location for equipment in Equipment.query.all()))
    
    return render_template('index.html',
                         equipment_count=equipment_count,
                         equipment_by_category=equipment_by_category,
                         maintenance_needed=maintenance_needed,
                         out_of_service=out_of_service,
                         recent_maintenance=recent_maintenance,
                         filtered_equipment=filtered_equipment,
                         search_query=search_query,
                         search_category=search_category,
                         search_location=search_location,
                         search_status=search_status,
                         locations=locations,
                         categories=current_app.config['EQUIPMENT_CATEGORIES'])

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get search parameters
    search_query = request.args.get('search', '')
    search_category = request.args.get('category', '')
    search_location = request.args.get('location', '')
    search_status = request.args.get('status', '')

    # Base query
    equipment_query = Equipment.query

    # Apply search filters
    if search_query:
        equipment_query = equipment_query.filter(
            or_(
                Equipment.name.ilike(f'%{search_query}%'),
                Equipment.serial_number.ilike(f'%{search_query}%'),
                Equipment.notes.ilike(f'%{search_query}%')
            )
        )
    
    if search_category:
        equipment_query = equipment_query.filter_by(category=search_category)
    
    if search_location:
        equipment_query = equipment_query.filter_by(location=search_location)
    
    if search_status:
        equipment_query = equipment_query.filter_by(status=search_status)

    # Get filtered equipment
    filtered_equipment = equipment_query.all()
    
    # Get equipment counts by category
    equipment_by_category = {}
    for category in current_app.config['EQUIPMENT_CATEGORIES'].keys():
        count = Equipment.query.filter_by(category=category).count()
        equipment_by_category[category] = count
    
    # Get equipment requiring maintenance (either status is maintenance or next_maintenance is due)
    maintenance_needed = Equipment.query.filter(
        (Equipment.status == 'maintenance') |
        (Equipment.next_maintenance <= datetime.utcnow().date())
    ).count()

    # Get unique locations for dropdown
    locations = sorted(set(equipment.location for equipment in Equipment.query.all()))
    
    return render_template('dashboard.html',
                         equipment_by_category=equipment_by_category,
                         maintenance_needed=maintenance_needed,
                         filtered_equipment=filtered_equipment,
                         search_query=search_query,
                         search_category=search_category,
                         search_location=search_location,
                         search_status=search_status,
                         locations=locations,
                         categories=current_app.config['EQUIPMENT_CATEGORIES']) 