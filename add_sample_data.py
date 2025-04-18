from app import create_app, db
from app.models.equipment import Equipment, MaintenanceRecord
from datetime import datetime, timedelta
import random

def generate_equipment_data():
    # Equipment categories and subcategories from config
    categories = {
        'IT': ['Computers', 'Servers', 'Printers', 'POS systems'],
        'Fire Safety': ['Fire alarms and control panels', 'Fire extinguishers', 'Fire safety equipment'],
        'Kitchen': ['Kitchen electronic equipment', 'Kitchen cookers', 'Kitchen safety systems'],
        'Facilities': ['Boilers', 'Sprinkler systems', 'Laundry room equipment', 'Waste management equipment', 'Gardening equipment'],
        'Medical': ['Wheelchairs', 'Nursing beds', 'Standing hoists', 'Oxford hoists', 'Stand aids', 'Mobility aids', 'Weighing adapters', 'Specialist bath equipment'],
        'Household': ['Microwaves', 'Dishwashers', 'TVs and remotes', 'Hairdressing room equipment', 'Dining rooms equipment', 'Cleaning tools and machines'],
        'Security': ['Safe']
    }

    # Sample equipment names by category
    equipment_names = {
        'IT': ['Dell OptiPlex', 'HP ProBook', 'Lenovo ThinkPad', 'MacBook Pro', 'Dell Server', 'HP Printer', 'Epson Scanner', 'POS Terminal'],
        'Fire Safety': ['Fire Alarm Panel', 'Smoke Detector', 'Fire Extinguisher', 'Emergency Lighting', 'Fire Door', 'Sprinkler Head'],
        'Kitchen': ['Commercial Oven', 'Industrial Fridge', 'Food Processor', 'Dishwasher', 'Microwave', 'Coffee Machine', 'Food Warmer'],
        'Facilities': ['Boiler Unit', 'HVAC System', 'Laundry Machine', 'Water Heater', 'Garden Mower', 'Leaf Blower', 'Pressure Washer'],
        'Medical': ['Electric Wheelchair', 'Hospital Bed', 'Patient Hoist', 'Blood Pressure Monitor', 'Oxygen Concentrator', 'Patient Lift', 'Medical Cart'],
        'Household': ['Smart TV', 'Washing Machine', 'Vacuum Cleaner', 'Hair Dryer', 'Electric Kettle', 'Toaster', 'Blender'],
        'Security': ['Digital Safe', 'Security Camera', 'Access Control Panel', 'Key Card Reader']
    }

    # Sample locations
    locations = ['Reception', 'Admin Office', 'Main Hall', 'Kitchen', 'Room 101', 'Room 102', 'Room 103', 
                'Room 104', 'Room 105', 'Room 106', 'Room 107', 'Room 108', 'Room 109', 'Room 110',
                'Laundry Room', 'Storage Room', 'Maintenance Room', 'Staff Room', 'Dining Hall', 'Garden']

    # Generate 200 equipment items
    equipment_data = []
    for i in range(200):
        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category])
        name = random.choice(equipment_names[category])
        status = random.choice(['operational', 'operational', 'operational', 'maintenance', 'out_of_service'])  # Weighted towards operational
        
        # Generate unique serial number
        serial_prefix = ''.join([c[0] for c in category.split()]).upper()
        serial_number = f'SN-{serial_prefix}-{i+1:03d}'
        
        # Generate purchase date between 2020 and 2023
        purchase_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1095))
        
        equipment_data.append({
            'name': f'{name} {i+1}',
            'category': category,
            'subcategory': subcategory,
            'serial_number': serial_number,
            'purchase_date': purchase_date.date(),
            'location': random.choice(locations),
            'status': status,
            'notes': f'Sample equipment {i+1}'
        })
    
    return equipment_data

def generate_maintenance_data(equipment_objects):
    maintenance_types = ['routine', 'repair', 'inspection']
    technicians = ['IT Support', 'HP Technician', 'Fire Safety Officer', 'Kitchen Equipment Specialist',
                  'Medical Equipment Technician', 'Facilities Manager', 'Security Specialist']
    
    maintenance_data = []
    for equipment in equipment_objects:
        # Generate 1-3 maintenance records per equipment
        num_records = random.randint(1, 3)
        for _ in range(num_records):
            maintenance_date = equipment.purchase_date + timedelta(days=random.randint(30, 365))
            next_maintenance = maintenance_date + timedelta(days=random.randint(180, 365))
            
            maintenance_data.append({
                'equipment_id': equipment.id,
                'maintenance_date': maintenance_date,
                'maintenance_type': random.choice(maintenance_types),
                'description': f'{random.choice(maintenance_types).title()} maintenance for {equipment.name}',
                'performed_by': random.choice(technicians),
                'cost': round(random.uniform(50, 500), 2),
                'next_maintenance_date': next_maintenance
            })
    
    return maintenance_data

def add_sample_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        MaintenanceRecord.query.delete()
        Equipment.query.delete()
        db.session.commit()

        # Generate and add equipment
        equipment_data = generate_equipment_data()
        equipment_objects = []
        for data in equipment_data:
            equipment = Equipment(**data)
            equipment_objects.append(equipment)
            db.session.add(equipment)
        db.session.commit()

        # Generate and add maintenance records
        maintenance_data = generate_maintenance_data(equipment_objects)
        for data in maintenance_data:
            maintenance = MaintenanceRecord(**data)
            db.session.add(maintenance)
        db.session.commit()

        print(f"Added {len(equipment_objects)} equipment items and {len(maintenance_data)} maintenance records successfully!")

if __name__ == '__main__':
    add_sample_data() 