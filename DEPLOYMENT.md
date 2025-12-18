# WorkApp 部署指南

## 📋 前置要求

### 系统要求
- **操作系统**: Linux/macOS/Windows
- **Python**: 3.8+
- **内存**: 至少 512MB
- **存储**: 至少 1GB 可用空间

### 网络要求
- **域名**: 配置SSL证书 (推荐 Let's Encrypt)
- **端口**: 80/443 (HTTP/HTTPS)
- **企业微信**: 应用回调域名配置

## 🔧 企业微信配置

### 1. 创建企业微信应用

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/)
2. 进入"应用管理" → "创建应用"
3. 填写应用信息：
   - **应用名称**: WorkApp
   - **应用描述**: 企业应用管理中心
   - **应用图标**: 上传图标
   - **可见范围**: 选择需要使用的部门/成员

### 2. 获取应用凭据

在应用详情页获取：
- **CorpID**: 企业ID
- **AgentId**: 应用ID
- **Secret**: 应用密钥

### 3. 配置回调域名

在应用"网页授权及JS-SDK"设置中：
- **授权回调域**: `https://your-domain.com`
- **可信域名**: `https://your-domain.com`

## 🚀 部署步骤

### 方法一：Docker 部署 (推荐)

#### 1. 创建 Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 5001

CMD ["python", "app.py"]
```

#### 2. 创建 docker-compose.yml
```yaml
version: '3.8'

services:
  workapp:
    build: .
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
      - WECOM_CORPID=your_corp_id
      - WECOM_SECRET=your_app_secret
      - WECOM_AGENTID=your_agent_id
      - DEV_MODE=false
      - SQLALCHEMY_DATABASE_URI=mysql://user:password@db:3306/workapp
    volumes:
      - ./static/uploads:/app/static/uploads
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=workapp
      - MYSQL_USER=workapp
      - MYSQL_PASSWORD=your-db-password
      - MYSQL_ROOT_PASSWORD=your-root-password
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - workapp
    restart: unless-stopped

volumes:
  mysql_data:
```

#### 3. 创建 Nginx 配置
```nginx
upstream workapp {
    server workapp:5001;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL 配置
    ssl_certificate /etc/ssl/certs/your-domain.crt;
    ssl_certificate_key /etc/ssl/certs/your-domain.key;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # 静态文件缓存
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 应用代理
    location / {
        proxy_pass http://workapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持 (如果需要)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### 4. 部署命令
```bash
# 构建和启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f workapp

# 更新应用
docker-compose pull && docker-compose up -d
```

### 方法二：传统部署

#### 1. 服务器准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python和依赖
sudo apt install python3 python3-pip python3-dev build-essential -y

# 安装MySQL (可选)
sudo apt install mysql-server -y
```

#### 2. 应用部署
```bash
# 克隆代码
git clone <repository-url>
cd workapp

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建配置文件
cp config.example.py config.py
# 编辑 config.py 填入实际配置

# 初始化数据库
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

# 启动应用
python3 app.py
```

#### 3. 使用 Systemd 服务
```bash
# 创建服务文件
sudo nano /etc/systemd/system/workapp.service
```

```ini
[Unit]
Description=WorkApp Enterprise Application Center
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/workapp
Environment="PATH=/path/to/workapp/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/path/to/workapp/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl daemon-reload
sudo systemctl start workapp
sudo systemctl enable workapp

# 查看状态
sudo systemctl status workapp
```

## 🔒 安全配置

### 1. SSL证书配置
```bash
# 使用 certbot 获取免费SSL证书
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 2. 防火墙配置
```bash
# UFW 配置
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

### 3. 应用安全
- **SECRET_KEY**: 使用强密码生成器生成
- **数据库密码**: 使用复杂密码
- **文件权限**: 限制上传目录权限

## 📊 监控和维护

### 健康检查
```bash
# 添加健康检查路由
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

### 日志配置
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('workapp.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

### 备份策略
```bash
# 数据库备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u workapp -p workapp > backup_$DATE.sql

# 文件备份
tar -czf uploads_backup_$DATE.tar.gz static/uploads/
```

## 🔧 故障排除

### 常见问题

#### 企业微信登录失败
1. 检查 CorpID、Secret、AgentId 配置
2. 确认回调域名配置正确
3. 查看企业微信应用权限设置

#### 数据库连接失败
1. 检查数据库服务器状态
2. 验证连接字符串格式
3. 确认数据库用户权限

#### 文件上传失败
1. 检查上传目录权限
2. 验证文件大小限制
3. 确认磁盘空间充足

#### 性能问题
1. 启用 Gunicorn WSGI服务器
2. 配置数据库连接池
3. 添加缓存层 (Redis)

## 📞 技术支持

如遇部署问题，请：
1. 查看应用日志: `docker-compose logs workapp`
2. 检查系统资源使用情况
3. 验证网络连接和防火墙设置

---

**WorkApp** - 让企业应用管理变得简单而强大！ 🚀