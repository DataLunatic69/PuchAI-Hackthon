# HostelBuddy MCP Server Deployment Guide

## 🚀 Deployment Options

### 1. Local Development Server (Current Setup)
**Status**: ✅ Already Running
- **URL**: `http://localhost:8086/mcp/`
- **Use Case**: Development, testing, local use

### 2. Cloud Deployment Options

#### Option A: DigitalOcean/Linode VPS (Recommended)
- **Cost**: $5-10/month
- **Best for**: Small to medium scale, full control
- **Setup Time**: 15-30 minutes

#### Option B: Railway/Render (Easiest)
- **Cost**: $5-10/month
- **Best for**: Quick deployment, minimal setup
- **Setup Time**: 5-10 minutes

#### Option C: AWS/Google Cloud (Enterprise)
- **Cost**: Variable ($10-50+/month)
- **Best for**: High availability, enterprise scale
- **Setup Time**: 30-60 minutes

#### Option D: Docker + Any Cloud Provider
- **Cost**: Variable
- **Best for**: Scalable, reproducible deployments
- **Setup Time**: 20-40 minutes

---

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker installed on your system
- Your Groq API key
- Basic terminal knowledge

### Quick Deploy
```bash
# 1. Build the image
docker build -t hostelbuddy-mcp .

# 2. Run the container
docker run -d \
  --name hostelbuddy \
  -p 8086:8086 \
  -e GROQ_API_KEY=your_groq_api_key_here \
  -e AUTH_TOKEN=your_auth_token_here \
  -e MY_NUMBER=your_phone_number \
  hostelbuddy-mcp

# 3. Check if running
docker ps
```

---

## 🌐 VPS Deployment (Ubuntu/Debian)

### Step-by-Step Instructions

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git nginx -y

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### 2. Application Setup
```bash
# Clone your repository
git clone https://github.com/yourusername/hostel-buddy-mcp.git
cd hostel-buddy-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Create production environment file
cp .env.example .env.production
# Edit with your production values
nano .env.production
```

#### 3. Service Setup
```bash
# Create systemd service
sudo cp deployment/hostelbuddy.service /etc/systemd/system/
sudo systemctl enable hostelbuddy
sudo systemctl start hostelbuddy
sudo systemctl status hostelbuddy
```

#### 4. Nginx Reverse Proxy
```bash
# Configure Nginx
sudo cp deployment/nginx.conf /etc/nginx/sites-available/hostelbuddy
sudo ln -s /etc/nginx/sites-available/hostelbuddy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## ☁️ Railway Deployment (Easiest)

### 1. Prepare Your Repository
```bash
# Create railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python src/mcp_server.py",
    "healthcheckPath": "/health"
  }
}
```

### 2. Deploy
1. Visit [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables:
   - `GROQ_API_KEY`
   - `AUTH_TOKEN`
   - `MY_NUMBER`
4. Deploy!

---

## 🔧 Production Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here
AUTH_TOKEN=your_secure_auth_token_here
MY_NUMBER=your_phone_number

# Optional Production Settings
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8086
LOG_LEVEL=INFO
WORKERS=4
```

### Security Considerations
- Use strong, unique AUTH_TOKEN
- Enable HTTPS/SSL
- Set up firewall rules
- Regular security updates
- Monitor logs for suspicious activity

---

## 📊 Monitoring & Maintenance

### Health Check Endpoint
```python
# Add to mcp_server.py
@mcp.tool
async def health_check() -> str:
    """Health check endpoint for monitoring"""
    return "OK"
```

### Log Monitoring
```bash
# View logs
sudo journalctl -u hostelbuddy -f

# Log rotation
sudo logrotate /etc/logrotate.d/hostelbuddy
```

### Backup Strategy
- Database backups (if applicable)
- Configuration file backups
- Regular system snapshots

---

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
sudo lsof -i :8086
sudo kill -9 <PID>
```

#### Permission Denied
```bash
sudo chown -R $USER:$USER /path/to/hostelbuddy
chmod +x src/mcp_server.py
```

#### Memory Issues
```bash
# Check memory usage
free -h
# Restart service
sudo systemctl restart hostelbuddy
```

---

## 🔄 Updates & Maintenance

### Update Deployment
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -e . --upgrade

# Restart service
sudo systemctl restart hostelbuddy
```

### Rolling Updates (Zero Downtime)
```bash
# Blue-green deployment script
./deployment/rolling_update.sh
```

---

## 📞 Support

### Quick Start Commands
```bash
# Check service status
sudo systemctl status hostelbuddy

# View logs
sudo journalctl -u hostelbuddy -n 50

# Restart service
sudo systemctl restart hostelbuddy

# Test endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8086/mcp/
```

### Performance Tuning
- Increase worker processes for higher load
- Use Redis for session management
- Implement rate limiting
- Set up CDN for static assets

---

**Next Steps**: Choose your deployment method and follow the specific instructions above!