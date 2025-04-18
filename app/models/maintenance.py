from datetime import datetime
from app import db

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    maintenance_type = db.Column(db.String(50), nullable=False)  # e.g., 'routine', 'repair', 'inspection'
    description = db.Column(db.Text)
    cost = db.Column(db.Float)
    technician = db.Column(db.String(100))
    next_maintenance = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    equipment = db.relationship('Equipment', backref=db.backref('maintenance_records', lazy=True))

    def __repr__(self):
        return f'<Maintenance {self.id} for Equipment {self.equipment_id}>' 