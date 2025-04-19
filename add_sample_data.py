from app import create_app, db
from app.models.equipment import Equipment, MaintenanceRecord
from datetime import datetime, timedelta
import random

def create_sample_data():
    app = create_app()
    with app.app_context():
        # Sample locations
        locations = [
            'Ground Floor', 'First Floor', 'Second Floor', 'Reception', 
            'Kitchen', 'Dining Room', 'Laundry Room', 'Staff Room',
            'Garden', 'Storage Room', 'Medical Room', 'Activity Room'
        ]

        # Sample equipment names and details by category
        equipment_data = {
            'IT': {
                'items': ['Desktop Computer', 'Laptop', 'Printer', 'Scanner', 'POS Terminal', 'Network Router', 'Security Camera'],
                'prefix': 'IT'
            },
            'Fire Safety': {
                'items': ['Fire Alarm Panel', 'Smoke Detector', 'Fire Extinguisher', 'Emergency Light', 'Fire Blanket'],
                'prefix': 'FS'
            },
            'Kitchen': {
                'items': ['Commercial Oven', 'Dishwasher', 'Refrigerator', 'Food Processor', 'Microwave', 'Coffee Machine'],
                'prefix': 'KT'
            },
            'Facilities': {
                'items': ['HVAC Unit', 'Water Heater', 'Generator', 'Washing Machine', 'Dryer', 'Vacuum Cleaner'],
                'prefix': 'FC'
            },
            'Medical': {
                'items': ['Patient Bed', 'Wheelchair', 'Blood Pressure Monitor', 'Oxygen Concentrator', 'Patient Lift', 'ECG Machine'],
                'prefix': 'MD'
            },
            'Household': {
                'items': ['Television', 'Air Purifier', 'Water Dispenser', 'Electric Fan', 'Space Heater'],
                'prefix': 'HH'
            },
            'Security': {
                'items': ['CCTV System', 'Access Control Panel', 'Security Gate', 'Safe', 'Intercom System'],
                'prefix': 'SC'
            }
        }

        # Status options with weights
        status_options = ['operational'] * 70 + ['maintenance'] * 20 + ['out_of_service'] * 10

        # Maintenance types
        maintenance_types = ['routine', 'repair', 'inspection']

        # Technicians
        technicians = [
            'John Smith', 'Emma Wilson', 'Michael Brown', 'Sarah Davis',
            'James Johnson', 'Lisa Anderson', 'Robert Taylor', 'Patricia Moore'
        ]

        # Generate equipment
        equipment_count = 0
        maintenance_count = 0
        
        print("Starting to generate sample data...")

        for category, data in equipment_data.items():
            for _ in range(random.randint(20, 40)):  # 20-40 items per category
                item_name = random.choice(data['items'])
                serial_number = f"{data['prefix']}-{random.randint(1000, 9999)}"
                
                # Generate dates
                purchase_date = datetime.now() - timedelta(days=random.randint(0, 1095))  # Up to 3 years old
                last_maintenance = purchase_date + timedelta(days=random.randint(30, 180))
                next_maintenance = last_maintenance + timedelta(days=random.randint(90, 365))

                # Create equipment
                equipment = Equipment(
                    name=item_name,
                    category=category,
                    subcategory=random.choice(data['items']),
                    serial_number=serial_number,
                    purchase_date=purchase_date.date(),
                    last_maintenance=last_maintenance.date(),
                    next_maintenance=next_maintenance.date(),
                    status=random.choice(status_options),
                    location=random.choice(locations),
                    notes=f"Sample {item_name} in {category} category"
                )
                db.session.add(equipment)
                equipment_count += 1

                # Generate 1-3 maintenance records per equipment
                for _ in range(random.randint(1, 3)):
                    maint_date = purchase_date + timedelta(days=random.randint(30, 900))
                    next_maint_date = maint_date + timedelta(days=random.randint(90, 365))
                    
                    maintenance = MaintenanceRecord(
                        equipment=equipment,
                        maintenance_date=maint_date.date(),
                        maintenance_type=random.choice(maintenance_types),
                        description=f"Regular maintenance check for {item_name}",
                        performed_by=random.choice(technicians),
                        cost=round(random.uniform(50, 500), 2),
                        next_maintenance_date=next_maint_date.date()
                    )
                    db.session.add(maintenance)
                    maintenance_count += 1

                if equipment_count % 10 == 0:
                    print(f"Generated {equipment_count} equipment records...")

        db.session.commit()
        print(f"\nSuccessfully added {equipment_count} equipment records and {maintenance_count} maintenance records.")

if __name__ == '__main__':
    create_sample_data() 