#!/bin/bash

# Update system
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y python3-pip python3-venv nginx gdal-bin libgdal-dev git

# Create pineguard user
useradd -m -r -s /bin/bash pineguard

# Create application directory
mkdir -p /opt/pineguard
cd /opt/pineguard

# Copy files from current directory
cp -r /root/pineguard/* /opt/pineguard/
chown -R pineguard:pineguard /opt/pineguard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up systemd service
cp pineguard.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable pineguard
systemctl start pineguard

# Configure Nginx
cat > /etc/nginx/sites-available/pineguard << 'EOL'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOL

# Enable site and restart Nginx
ln -s /etc/nginx/sites-available/pineguard /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
systemctl restart nginx
