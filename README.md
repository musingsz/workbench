# WorkApp - 企业应用中心

## 🌟 项目简介

**WorkApp** 是一款专为企业打造的智能应用管理平台，让团队协作更高效，让应用管理更简单。通过统一的入口，集中管理所有工作工具，提升组织数字化转型效率。

![WorkApp 演示界面](static/images/workapp-demo.png)

*WorkApp 企业应用中心演示界面 - 多部门工具统一管理平台*

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

4. **生成演示数据 (可选)**
   ```bash
   python3 seed_demo.py
   ```

5. **启动应用**
   ```bash
   python app.py
   ```

6. **访问应用**
   打开浏览器访问: `http://localhost:5001`

## 🎯 演示数据

项目提供了丰富的演示数据，帮助您快速了解 WorkApp 的功能：

### 生成演示数据

```bash
python3 seed_demo.py
```

### 演示内容

![WorkApp 多部门演示](static/images/workapp-demo.png)

*WorkApp 多部门工作台展示 - 每个部门都有专业的工具分组*

- **6个部门工作台**: 研发中心、产品部门、运营部门、市场部门、人力资源、财务部门
- **228个精选应用**: 涵盖企业各个业务场景
- **38个功能分组**: 每个部门6个专业分组

#### 研发中心 (8个分组)
- 开发工具、项目管理、CI/CD、测试工具、运维监控、云服务、设计工具、沟通协作

#### 产品部门 (6个分组)
- 需求管理、用户研究、原型设计、数据分析、项目协作、沟通工具

#### 运营部门 (6个分组)
- 数据分析、用户运营、内容营销、SEO工具、广告投放、邮件营销

#### 市场部门 (6个分组)
- 品牌设计、市场调研、竞争分析、内容创作、社交媒体、PR公关

#### 人力资源 (6个分组)
- 招聘管理、绩效管理、学习发展、员工体验、薪酬福利、组织发展

#### 财务部门 (6个分组)
- 财务管理、预算规划、财务分析、税务合规、费用报销、审计风控

### 清除演示数据

```bash
python3 seed_demo.py --clear
```

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
- 悬浮显示应用详细信息和访问统计
- 点击右上角编辑或删除应用
- 查看应用使用热度统计

### 使用演示数据
运行演示数据后，您可以：
1. 在侧边栏查看6个部门工作台
2. 点击任意部门工作台切换场景
3. 浏览各部门的专用工具分组
4. 点击任意应用图标跳转到对应工具
5. 悬浮查看应用详细信息和访问统计
6. 体验不同部门的工作流程和工具配置
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

## 🎨 界面预览

<p align="center">
  <img src="static/images/workapp-demo.png" alt="WorkApp 界面预览" width="800">
  <br>
  <em>WorkApp 现代化企业应用管理界面 - 左侧部门导航，右侧应用网格布局</em>
</p>

---

## 💝 捐赠支持

如果你觉得 **WorkApp** 为你减少了开发成本、化解了工作/生活里的难题，可以通过以下方式支持一下～

### 微信捐赠

<p align="center">
  <img src="static/images/wechat-donation-qr.png" alt="微信捐赠二维码" width="300">
  <br>
  <strong>微信扫码捐赠</strong>
  <br>
</p>

### 支持方式

- 🌟 **Star** 本项目 - 让更多人发现这个工具
- 📢 **分享** 给有需要的朋友或同事
- 💬 **反馈** 使用中的问题和建议
- 💰 **捐赠** 支持项目持续发展

### 致谢

感谢所有为开源社区做出贡献的开发者们！您的每一份支持都让我更有动力去完善这个项目。

---

**WorkApp** - 让企业应用管理变得简单而强大！ 🚀
