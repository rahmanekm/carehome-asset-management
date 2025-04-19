from setuptools import setup, find_packages

setup(
    name="carehome-asset-management",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.3.3',
        'Flask-SQLAlchemy==3.1.1',
        'Flask-Login==0.6.2',
        'Flask-WTF==1.1.1',
        'Flask-Migrate==4.1.0',
        'PyMySQL==1.1.0',
        'python-dotenv==1.0.0',
        'Werkzeug==2.3.7',
        'email-validator==2.0.0'
    ],
) 