# F2 CareHome - Equipment Management System

A comprehensive web application for managing equipment and assets in UK-based care homes.

## Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Security Considerations](#security-considerations)
- [Installation Guide](#installation-guide)
- [Database Setup](#database-setup)
- [Sample Data](#sample-data)
- [Web Server Configuration](#web-server-configuration)
- [SSL/TLS Setup](#ssltls-setup)
- [Monitoring Setup](#monitoring-setup)
- [Backup Configuration](#backup-configuration)
- [Maintenance and Updates](#maintenance-and-updates)
- [Troubleshooting](#troubleshooting)
- [Support](#support)
- [Production Deployment](#production-deployment)

## Features

### Equipment Management
- Comprehensive equipment inventory tracking
- Equipment categorization and classification
- Serial number and asset tag management
- Location tracking and management
- Status monitoring (Operational, Maintenance Required, Out of Service)

### Maintenance Management
- Scheduled maintenance tracking
- Maintenance history and records
- Maintenance alerts and notifications
- Work order management
- Service provider tracking

### User Management
- Role-based access control
- User authentication and authorization
- Activity logging
- User profile management

### Reporting and Analytics
- Equipment status reports
- Maintenance history reports
- Equipment utilization analytics
- Custom report generation

## System Requirements

### Hardware Requirements
- CPU: 2+ cores
- RAM: 4GB minimum
- Storage: 20GB minimum
- Network: 100Mbps connection

### Software Requirements
- Operating System:
  - Ubuntu 20.04 LTS or later
  - CentOS 8 or later
  - Windows Server 2019 or later
- Database: MySQL 8.0 or later
- Web Server: Nginx 1.18 or later
- Python: 3.8 or later
- Node.js: 14.x or later (for asset compilation)

## Security Considerations

1. **Network Security**
   - Configure firewall rules
   - Enable HTTPS only
   - Implement rate limiting
   - Set up IP whitelisting if needed

2. **Application Security**
   - Use strong password policies
   - Implement session timeout
   - Enable CSRF protection
   - Regular security updates

3. **Data Security**
   - Encrypt sensitive data
   - Regular backups
   - Access logging
   - Data retention policies

## Installation Guide

### 1. System Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3-pip python3-venv nginx mysql-server supervisor git

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Application Setup

```bash
# Clone the repository
git clone https://github.com/rahmanekm/carehome-asset-management.git
cd carehome-asset-management

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### 3. Environment Configuration

```bash
# Create .env file
cp .env.example .env

# Edit .env with production settings
nano .env
```

Required environment variables:
```
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:password@localhost/carehome
MAIL_SERVER=smtp.your-email-provider.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

## Database Setup

### 1. MySQL Configuration

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE carehome CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'carehome_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON carehome.* TO 'carehome_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Database Migration

```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

## Sample Data

The application includes a sample data generator that creates realistic equipment and maintenance records. To populate the database with sample data:

```bash
# Run the sample data generator
python add_sample_data.py
```

This will create:
- 195+ equipment records across 7 categories
- 380+ maintenance records
- Realistic data including:
  - Equipment details (name, category, serial number, etc.)
  - Maintenance history
  - Status distribution (70% operational, 20% maintenance, 10% out of service)
  - Location assignments
  - Maintenance schedules

Sample data categories include:
- IT Equipment
- Fire Safety
- Kitchen Equipment
- Facilities
- Medical Equipment
- Household Items
- Security Systems

## Web Server Configuration

### 1. Gunicorn Setup

```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn configuration
sudo nano /etc/supervisor/conf.d/carehome.conf
```

Add the following configuration:
```ini
[program:carehome]
command=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 run:app
directory=/path/to/carehome-asset-management
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/carehome.err.log
stdout_logfile=/var/log/carehome.out.log
```

### 2. Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/carehome
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/carehome-asset-management/app/static;
        expires 30d;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/carehome /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/TLS Setup

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Set up automatic renewal
sudo systemctl enable certbot.timer
```

## Monitoring Setup

### 1. Log Management

```bash
# Set up log rotation
sudo nano /etc/logrotate.d/carehome
```

Add the following configuration:
```conf
/var/log/carehome.*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload supervisor
    endscript
}
```

### 2. System Monitoring

```bash
# Install monitoring tools
sudo apt install -y prometheus node-exporter
```

## Backup Configuration

### 1. Database Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup_carehome.sh
```

Add the following script:
```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u carehome_user -p'password' carehome > $BACKUP_DIR/carehome_$DATE.sql
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
# Make script executable
sudo chmod +x /usr/local/bin/backup_carehome.sh

# Add to crontab
sudo crontab -e
```

Add the following line:
```cron
0 2 * * * /usr/local/bin/backup_carehome.sh
```

## Maintenance and Updates

### 1. System Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
source /path/to/venv/bin/activate
pip install -r requirements.txt --upgrade
```

### 2. Application Updates

```bash
# Pull latest changes
cd /path/to/carehome-asset-management
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt
npm install

# Restart application
sudo supervisorctl restart carehome
```

## Troubleshooting

### Common Issues

1. **Application Not Starting**
   - Check supervisor logs: `sudo supervisorctl status carehome`
   - Check application logs: `tail -f /var/log/carehome.err.log`

2. **Database Connection Issues**
   - Verify MySQL service is running: `sudo systemctl status mysql`
   - Check database credentials in .env file
   - Test database connection: `mysql -u carehome_user -p`

3. **Nginx Configuration Issues**
   - Test Nginx configuration: `sudo nginx -t`
   - Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

### Database Migration Issues

If you encounter errors during database migration, follow these steps:

1. **Clean Up Existing Database**:
```bash
# Connect to MySQL
mysql -u root -p

# Drop and recreate the database
DROP DATABASE carehome;
CREATE DATABASE carehome CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **Reset Migrations**:
```bash
# Remove existing migrations
rm -rf migrations/

# Initialize fresh migrations
flask db init

# Create and apply initial migration
flask db migrate -m "Initial migration"
flask db upgrade
```

3. **Common Errors and Solutions**:

   a. "Directory migrations already exists and is not empty"
   ```bash
   rm -rf migrations/
   flask db init
   ```

   b. "Table 'equipment' already exists"
   ```bash
   # Drop the database and recreate it
   mysql -u root -p -e "DROP DATABASE carehome; CREATE DATABASE carehome;"
   flask db upgrade
   ```

   c. "Target database is not up to date"
   ```bash
   # Reset the database and migrations
   rm -rf migrations/
   mysql -u root -p -e "DROP DATABASE carehome; CREATE DATABASE carehome;"
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Support

For technical support or issues, please contact:
- Email: mymails.abdul@gmail.com
- Documentation: [Documentation Link]
- Issue Tracker: [GitHub Issues]

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Production Deployment

### 1. Server Setup

```bash
# Create application directory
sudo mkdir -p /opt/carehome-asset-management
sudo chown -R $USER:$USER /opt/carehome-asset-management

# Clone the repository
cd /opt/carehome-asset-management
git clone https://github.com/rahmanekm/carehome-asset-management.git .

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the application
pip install -e .
```

### 2. Environment Configuration

```bash
# Create .env file
cp .env.example .env
nano .env

# Set FLASK_APP environment variable
echo "export FLASK_APP=run.py" >> ~/.bashrc
source ~/.bashrc
```

### 3. Database Setup

```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade

# Add sample data (optional)
python add_sample_data.py
```

### 4. Gunicorn Setup

```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn configuration
sudo nano /etc/supervisor/conf.d/carehome.conf
```

Add the following configuration:
```ini
[program:carehome]
command=/opt/carehome-asset-management/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 run:app
directory=/opt/carehome-asset-management
user=www-data
autostart=true
autorestart=true
environment=FLASK_APP="run.py"
stderr_logfile=/var/log/carehome.err.log
stdout_logfile=/var/log/carehome.out.log
```

### 5. Start the Application

```bash
# Start Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start carehome

# Check status
sudo supervisorctl status carehome
``` 
