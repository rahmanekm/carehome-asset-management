from app import db
from datetime import datetime

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), unique=True)
    purchase_date = db.Column(db.Date)
    last_maintenance = db.Column(db.Date)
    next_maintenance = db.Column(db.Date)
    status = db.Column(db.String(20), default='operational')  # operational, maintenance, out_of_service
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    maintenance_records = db.relationship('MaintenanceRecord', backref='equipment', lazy=True)

class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False)
    maintenance_type = db.Column(db.String(50))  # routine, repair, inspection
    description = db.Column(db.Text)
    performed_by = db.Column(db.String(100))
    cost = db.Column(db.Float)
    next_maintenance_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 