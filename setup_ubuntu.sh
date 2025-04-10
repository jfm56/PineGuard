#!/bin/bash
set -e

echo "Updating system packages..."
apt-get update
apt-get upgrade -y

echo "Installing Python and other dependencies..."
apt-get install -y python3 python3-pip python3-venv nginx gdal-bin libgdal-dev

echo "Creating application directory..."
mkdir -p /opt/pineguard
cd /opt/pineguard

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install fastapi uvicorn python-multipart

echo "Creating service user..."
useradd -r -s /bin/false pineguard || true

echo "Setting up Nginx configuration..."
cat > /etc/nginx/sites-available/pineguard << 'EOL'
server {
    listen 80;
    server_name _;

    location / {
        root /opt/pineguard/app/static;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOL

echo "Enabling Nginx configuration..."
ln -sf /etc/nginx/sites-available/pineguard /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "Setting up systemd service..."
cat > /etc/systemd/system/pineguard.service << 'EOL'
[Unit]
Description=PineGuard Application
After=network.target

[Service]
User=pineguard
Group=pineguard
WorkingDirectory=/opt/pineguard
Environment="PATH=/opt/pineguard/venv/bin"
ExecStart=/opt/pineguard/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

[Install]
WantedBy=multi-user.target
EOL

echo "Setting permissions..."
chown -R pineguard:pineguard /opt/pineguard

echo "Starting services..."
systemctl daemon-reload
systemctl enable pineguard
systemctl restart pineguard
systemctl restart nginx

echo "Setup complete!"
