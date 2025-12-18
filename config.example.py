# WorkApp 配置文件模板
# 复制此文件为 config.py 并填入实际配置

import os

class Config:
    # Flask 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False

    # 数据库配置
    # 开发环境使用 SQLite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///workbench.db'
    # 生产环境使用 MySQL/PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///workbench.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 企业微信配置
    WECOM_CORPID = os.environ.get('WECOM_CORPID', 'your_corp_id')
    WECOM_SECRET = os.environ.get('WECOM_SECRET', 'your_app_secret')
    WECOM_AGENTID = os.environ.get('WECOM_AGENTID', 'your_agent_id')

    # 应用模式
    DEV_MODE = os.environ.get('DEV_MODE', 'false').lower() == 'true'

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # 服务器配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5001))


class DevelopmentConfig(Config):
    DEBUG = True
    DEV_MODE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///workbench_dev.db'


class ProductionConfig(Config):
    DEBUG = False
    DEV_MODE = False
    # 确保生产环境有强密码
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required in production")


# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
