import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://username:password@localhost/carehome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Equipment categories
    EQUIPMENT_CATEGORIES = {
        'IT': ['Computers', 'Servers', 'Printers', 'POS systems'],
        'Fire Safety': ['Fire alarms and control panels', 'Fire extinguishers', 'Fire safety equipment'],
        'Kitchen': ['Kitchen electronic equipment', 'Kitchen cookers', 'Kitchen safety systems'],
        'Facilities': ['Boilers', 'Sprinkler systems', 'Laundry room equipment', 'Waste management equipment', 'Gardening equipment'],
        'Medical': ['Wheelchairs', 'Nursing beds', 'Standing hoists', 'Oxford hoists', 'Stand aids', 'Mobility aids', 'Weighing adapters', 'Specialist bath equipment'],
        'Household': ['Microwaves', 'Dishwashers', 'TVs and remotes', 'Hairdressing room equipment', 'Dining rooms equipment', 'Cleaning tools and machines'],
        'Security': ['Safe']
    } 