# 🔗 shrlnk.icu

A modern URL shortener service with a sleek web interface that allows you to create and customize short links with real-time social media preview capabilities. Built with Flask and designed for high performance and reliability.

## ✨ Features

- **User-Friendly Interface**: Simple web interface for link creation and customization
- **Real-time Preview**: See how your links will appear on social media platforms instantly
- **Custom URLs**: Create memorable, personalized short URLs
- **Link Management**: Track and manage your shortened URLs
- **Rate Limiting**: Built-in protection against abuse
- **Image Validation**: Secure handling of preview images
- **Mobile Responsive**: Works seamlessly on all devices

## 🛠 Tech Stack

- Python 3.12
- Flask (Web Framework)
- uv (Fast Python Package Installer)
- Gunicorn (WSGI HTTP Server)
- Nginx (Reverse Proxy)
- SQLite (Database)
- JavaScript (Real-time previews)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shrlnk.git
cd shrlnk
```

2. Install uv (if not already installed):
```bash
pip install uv
```

3. Just run the app.py and it will initialize the venv:
```bash
uv run app.py
```


3. Access the interface at `http://localhost:5000/interface`

## 🚀 Production Deployment

### Domain Setup

1. Purchase a domain from a domain registrar (e.g., Namecheap, GoDaddy, Route53)
2. Set up DNS records:
```
Type  | Name                      | Value/Target
A     | yourdomain.com            | <Your EC2 IP>
A     | www.yourdomain.com        | <Your EC2 IP>
```
3. Wait for DNS propagation (can take up to 48 hours, typically 15-30 minutes)

### AWS EC2 Setup

1. Launch an EC2 instance with AWS Linux
2. Configure Security Groups:
- Allow HTTP (Port 80)
- Allow HTTPS (Port 443)
- Allow SSH (Port 22)
3. Install required packages:
```bash
sudo yum update

sudo yum install python3.12 python3-pip gunicorn nginx certbot

python3-certbot-nginx
```

### Gunicorn Setup

Create a Gunicorn systemd service file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=Gunicorn instance to serve shrlnk
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/shrlnk
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable gunicorn
sudo systemctl start gonicorn
```

### Nginx Configuration

1. Create Nginx site configuration:
```bash
sudo nano /etc/nginx/sites-available/shrlnk
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;  # Replace with your domain

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/shrlnk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

3. Set up SSL with Let's Encrypt:
```bash
sudo certbot --nginx -d yourdomain.com
```

### Update Application Configuration

1. Update your Flask application configuration with your domain:
```python
DOMAIN = "yourdomain.com"  # Replace with your actual domain
```

## 📝 How to Use

1. Navigate to `https://yourdomain.com/interface` in your web browser
2. Enter the long URL you want to shorten
3. Optionally customize:
- Custom short URL path
- Title for social media preview
- Description for social media preview
- Preview image URL
4. See real-time previews of how your link will appear on different social platforms
5. Click "Generate" to create your shortened URL

### Features of the Web Interface

- **Real-time Preview**: As you type, see live previews of how your link will appear
- **Custom URL Path**: Create memorable URLs like `yourdomain.com/my-special-link`
- **Social Media Optimization**: Customize how your links appear when shared
- **Mobile Responsive**: Create and manage links from any device

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/shrlnk.icu/issues).

