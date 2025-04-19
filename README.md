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
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE carehome_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'carehome_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON carehome_db.* TO 'carehome_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Application Setup

```bash
# Clone the repository
git clone https://github.com/rahmanekm/carehome-asset-management
cd carehome-asset-management

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
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

1. Create a MySQL database:
```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE carehome_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'carehome_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON carehome_db.* TO 'carehome_user'@'localhost';
FLUSH PRIVILEGES;
```

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

## Security Considerations

1. **Environment Variables**
   - Keep all sensitive information in `.env`
   - Never commit `.env` to version control
   - Use strong, unique passwords

2. **Database Security**
   - Use strong passwords for database users
   - Limit database user privileges
   - Regularly update database credentials

## Backup Strategy

1. **Database Backups**
```bash
# Create backup script
sudo nano /usr/local/bin/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u carehome_user -p'your_password' carehome_db > $BACKUP_DIR/carehome_db_$DATE.sql
find $BACKUP_DIR -type f -mtime +7 -delete
```

2. **Application Backups**
```bash
# Create backup script
sudo nano /usr/local/bin/backup-app.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /path/to/your/app
find $BACKUP_DIR -type f -mtime +7 -delete
```

## Monitoring

1. **System Monitoring**
   - Set up monitoring tools (e.g., Prometheus, Grafana)
   - Configure alerts for system resources
   - Monitor application logs

2. **Application Monitoring**
   - Set up error tracking (e.g., Sentry)
   - Monitor response times
   - Track user activity

## Maintenance

1. **Regular Updates**
   - Update system packages weekly
   - Update Python dependencies monthly
   - Review and update security configurations

2. **Database Maintenance**
   - Regular backups
   - Optimize queries
   - Monitor performance

3. **Application Maintenance**
   - Regular code updates
   - Performance optimization
   - Security patches

## Troubleshooting

Common issues and solutions:

1. **Application Not Starting**
   - Check supervisor logs
   - Verify environment variables
   - Check file permissions

2. **Database Connection Issues**
   - Verify database credentials
   - Check MySQL service status
   - Review firewall settings

3. **Performance Issues**
   - Check system resources
   - Review database queries
   - Optimize application code

## Support

For support, please contact:
- Email: mymails.abdul@gmail.com
- Issue Tracker: GitHub Issues

## License

This project is licensed under the MIT License - see the LICENSE file for details.
