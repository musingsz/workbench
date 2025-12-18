# Gunicorn 配置文件
# 用于生产环境部署

import os

# 服务器配置
bind = f"0.0.0.0:{os.environ.get('PORT', '5001')}"
backlog = 2048

# 工作进程配置
workers = int(os.environ.get('WEB_CONCURRENCY', 2))
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# 超时配置
timeout = 30
keepalive = 2

# 日志配置
loglevel = os.environ.get('LOG_LEVEL', 'info')
accesslog = '/var/log/workapp/access.log'
errorlog = '/var/log/workapp/error.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程命名
proc_name = 'workapp'

# 应用配置
raw_env = [
    f'FLASK_ENV={os.environ.get("FLASK_ENV", "production")}',
    f'SECRET_KEY={os.environ.get("SECRET_KEY", "default-secret")}',
    f'DATABASE_URL={os.environ.get("DATABASE_URL", "sqlite:///workbench.db")}',
    f'WECOM_CORPID={os.environ.get("WECOM_CORPID", "")}',
    f'WECOM_SECRET={os.environ.get("WECOM_SECRET", "")}',
    f'WECOM_AGENTID={os.environ.get("WECOM_AGENTID", "")}',
    f'DEV_MODE={os.environ.get("DEV_MODE", "false")}'
]

# 安全配置
user = os.environ.get('APP_USER', 'www-data')
group = os.environ.get('APP_GROUP', 'www-data')
tmp_upload_dir = None