# CareHome Equipment Management System

A comprehensive web application for managing equipment and maintenance records in care home facilities. Built with Flask, MySQL, and modern web technologies.

## Features

- Equipment tracking and management
- Maintenance scheduling and records
- User authentication and authorization
- Modern, responsive UI
- Search and filter capabilities
- Status monitoring and alerts

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Docker (optional, for containerized deployment)
- Git

## Production Environment Setup

### 1. System Requirements

- Linux server (Ubuntu 20.04 LTS recommended)
- 2 CPU cores minimum
- 4GB RAM minimum
- 20GB storage minimum
- Domain name with SSL certificate

### 2. Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3-pip python3-venv nginx mysql-server supervisor

# Install Python dependencies
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential
```

### 3. Database Setup

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
git clone https://github.com/yourusername/carehome-asset-management.git
cd carehome-asset-management

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit the `.env` file with your production settings:

```env
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=your_secure_secret_key
DATABASE_URL=mysql://carehome_user:your_secure_password@localhost/carehome_db
```

### 5. Gunicorn Configuration

Create `/etc/supervisor/conf.d/carehome.conf`:

```ini
[program:carehome]
directory=/path/to/your/app
command=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:create_app()
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/carehome.err.log
stdout_logfile=/var/log/carehome.out.log
```

### 6. Nginx Configuration

Create `/etc/nginx/sites-available/carehome`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 30d;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/carehome /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL Configuration (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com
```

### 8. Start the Application

```bash
# Start Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start carehome

# Enable services to start on boot
sudo systemctl enable nginx
sudo systemctl enable supervisor
```

## Security Considerations

1. **Environment Variables**
   - Keep all sensitive information in `.env`
   - Never commit `.env` to version control
   - Use strong, unique passwords

2. **Database Security**
   - Use strong passwords for database users
   - Limit database user privileges
   - Enable SSL for database connections

3. **Application Security**
   - Keep dependencies updated
   - Use HTTPS only
   - Implement rate limiting
   - Regular security audits

4. **Server Security**
   - Configure firewall (UFW)
   - Regular system updates
   - Monitor system logs
   - Implement backup strategy

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
- Email: support@yourdomain.com
- Issue Tracker: GitHub Issues

## License

This project is licensed under the MIT License - see the LICENSE file for details. 