# Care Home Equipment Management System

A comprehensive web application for managing equipment and assets in UK-based care homes.

## Features

- Equipment inventory management
- Maintenance scheduling
- Asset tracking
- User authentication
- Equipment categorization
- Maintenance history
- Reporting capabilities

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the database:
- Create a MySQL database
- Update the .env file with your database credentials

4. Run the application:
```bash
python run.py
```

## Database Setup

1. Create a MySQL database
2. Update the .env file with your database credentials
3. Run the database migrations:
```bash
flask db upgrade
```

## Project Structure

```
carehome/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
└── run.py
``` 