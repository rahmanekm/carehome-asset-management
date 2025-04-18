from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models.equipment import Equipment, MaintenanceRecord
from app import db
from datetime import datetime

bp = Blueprint('equipment', __name__)

@bp.route('/equipment')
@login_required
def equipment_list():
    category = request.args.get('category', 'all')
    status = request.args.get('status', 'all')
    
    query = Equipment.query
    
    if category != 'all':
        query = query.filter_by(category=category)
    if status != 'all':
        query = query.filter_by(status=status)
    
    equipment = query.all()
    return render_template('equipment/list.html',
                         equipment=equipment,
                         categories=current_app.config['EQUIPMENT_CATEGORIES'],
                         current_category=category,
                         current_status=status)

@bp.route('/equipment/add', methods=['GET', 'POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        equipment = Equipment(
            name=request.form['name'],
            category=request.form['category'],
            subcategory=request.form['subcategory'],
            serial_number=request.form['serial_number'],
            purchase_date=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date(),
            location=request.form['location'],
            notes=request.form['notes']
        )
        
        db.session.add(equipment)
        db.session.commit()
        flash('Equipment added successfully!')
        return redirect(url_for('equipment.equipment_list'))
    
    return render_template('equipment/add.html',
                         categories=current_app.config['EQUIPMENT_CATEGORIES'])

@bp.route('/equipment/<int:id>')
@login_required
def equipment_detail(id):
    equipment = Equipment.query.get_or_404(id)
    return render_template('equipment/detail.html', equipment=equipment)

@bp.route('/equipment/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    
    if request.method == 'POST':
        equipment.name = request.form['name']
        equipment.category = request.form['category']
        equipment.subcategory = request.form['subcategory']
        equipment.serial_number = request.form['serial_number']
        equipment.purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date()
        equipment.location = request.form['location']
        equipment.notes = request.form['notes']
        equipment.status = request.form['status']
        
        db.session.commit()
        flash('Equipment updated successfully!')
        return redirect(url_for('equipment.equipment_detail', id=id))
    
    return render_template('equipment/edit.html',
                         equipment=equipment,
                         categories=current_app.config['EQUIPMENT_CATEGORIES'])

@bp.route('/equipment/<int:id>/maintenance', methods=['GET', 'POST'])
@login_required
def add_maintenance(id):
    equipment = Equipment.query.get_or_404(id)
    
    if request.method == 'POST':
        maintenance = MaintenanceRecord(
            equipment_id=id,
            maintenance_date=datetime.strptime(request.form['maintenance_date'], '%Y-%m-%d').date(),
            maintenance_type=request.form['maintenance_type'],
            description=request.form['description'],
            performed_by=request.form['performed_by'],
            cost=float(request.form['cost']) if request.form['cost'] else None,
            next_maintenance_date=datetime.strptime(request.form['next_maintenance_date'], '%Y-%m-%d').date() if request.form['next_maintenance_date'] else None
        )
        
        equipment.last_maintenance = maintenance.maintenance_date
        equipment.next_maintenance = maintenance.next_maintenance_date
        
        db.session.add(maintenance)
        db.session.commit()
        flash('Maintenance record added successfully!')
        return redirect(url_for('equipment.equipment_detail', id=id))
    
    return render_template('equipment/maintenance.html', equipment=equipment) 