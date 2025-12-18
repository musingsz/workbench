# WorkApp - 企业应用中心

## 🌟 项目简介

**WorkApp** 是一款专为企业打造的智能应用管理平台，让团队协作更高效，让应用管理更简单。通过统一的入口，集中管理所有工作工具，提升组织数字化转型效率。

## ✨ 核心特性

### 🏢 企业级应用管理
- **统一入口**: 所有工作应用一站式访问
- **智能分组**: 按项目、部门或功能分类管理
- **权限控制**: 支持公开和私有应用分组

### 🚀 智能化体验
- **自动识别**: 输入URL自动抓取应用信息
- **图标管理**: 支持网络图标和本地上传
- **使用统计**: 实时跟踪应用访问热度

### 🎨 现代化界面
- **响应式设计**: 适配桌面和移动设备
- **深色模式**: 支持夜间工作模式
- **流畅动画**: 精心设计的交互动画

### 🔒 企业级安全
- **企业微信集成**: 安全的SSO登录
- **权限管理**: 精细化的访问控制
- **数据隔离**: 企业数据安全保护

## 🛠 技术架构

- **后端**: Python Flask + SQLAlchemy
- **前端**: HTML5 + Tailwind CSS + Alpine.js
- **数据库**: SQLite (可升级至MySQL/PostgreSQL)
- **认证**: 企业微信OAuth2

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Flask 3.0+
- 企业微信应用权限

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd workapp
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置企业微信**
   ```bash
   export WECOM_CORPID="your_corp_id"
   export WECOM_SECRET="your_app_secret"
   export WECOM_AGENTID="your_agent_id"
   ```

4. **启动应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   打开浏览器访问: `http://localhost:5001`

## 🚀 生产部署

### Docker 部署 (推荐)

```bash
# 使用 Docker Compose 部署
docker-compose up -d --build
```

### 传统部署

```bash
# 使用启动脚本
./start.sh

# 或使用 Gunicorn
gunicorn --config gunicorn.conf.py app:app
```

详细部署指南请参考 [部署文档](DEPLOYMENT.md)

## 🔧 配置说明

### 环境变量

- `FLASK_ENV`: `development` 或 `production`
- `SECRET_KEY`: Flask 应用密钥 (生产环境必需)
- `WECOM_CORPID`: 企业微信 CorpID
- `WECOM_SECRET`: 企业微信应用密钥
- `WECOM_AGENTID`: 企业微信应用ID
- `DEV_MODE`: `true` (开发) 或 `false` (生产)
- `DATABASE_URL`: 数据库连接字符串

### 配置文件

复制 `config.example.py` 为 `config.py` 并填入实际配置。

## 📋 使用指南

### 创建应用中心
1. 点击"创建我的应用中心"
2. 为不同的团队或项目创建独立的工作台

### 添加应用分组
1. 在工作台中点击"新建分组"
2. 设置分组名称和权限

### 添加应用
1. 在分组中点击"添加"按钮
2. 输入应用URL，系统自动识别信息
3. 上传自定义图标或使用自动识别的图标

### 管理应用
- 悬浮显示应用详细信息
- 点击右上角编辑或删除应用
- 查看应用使用统计

## 🔧 配置说明

### 开发模式
```python
DEV_MODE = True  # 开发环境使用模拟登录
```

### 生产配置
```python
DEV_MODE = False  # 生产环境使用企业微信登录
```

### 数据库配置
默认使用SQLite，生产环境建议使用MySQL：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@host/db'
```

## 📚 API文档

### 主要接口

- `GET /login` - 用户登录
- `GET /logout` - 用户登出
- `GET /` - 主页面
- `POST /workbench/new` - 创建工作台
- `POST /workspace/{id}/app/new` - 添加应用
- `POST /api/fetch-meta` - 获取应用元数据

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

如有问题或建议，请通过以下方式联系：
- 项目Issues: [GitHub Issues]
- 邮箱: contact@workhub.com

---

**WorkApp** - 让企业应用管理变得简单而强大！ 🚀
