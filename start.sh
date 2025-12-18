#!/bin/bash

# WorkApp 启动脚本
# 支持开发和生产环境

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 环境检测
if [ "$FLASK_ENV" = "production" ]; then
    echo "🚀 启动生产环境..."

    # 检查必需的环境变量
    required_vars=("SECRET_KEY" "WECOM_CORPID" "WECOM_SECRET" "WECOM_AGENTID")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "❌ 错误: 生产环境需要设置 $var 环境变量"
            exit 1
        fi
    done

    # 使用 Gunicorn 启动
    if command -v gunicorn &> /dev/null; then
        echo "📦 使用 Gunicorn 启动应用..."
        exec gunicorn --config gunicorn.conf.py app:app
    else
        echo "⚠️  Gunicorn 未安装，使用 Flask 开发服务器..."
        export FLASK_ENV=production
        exec python app.py
    fi

else
    echo "🔧 启动开发环境..."

    # 开发环境配置
    export FLASK_ENV=development
    export DEV_MODE=true

    # 检查虚拟环境
    if [ -d "venv" ]; then
        echo "📦 激活虚拟环境..."
        source venv/bin/activate
    fi

    # 启动开发服务器
    echo "🌟 启动 WorkApp 开发服务器..."
    echo "📱 访问地址: http://localhost:5001"
    echo "🛠️  按 Ctrl+C 停止服务器"
    echo ""

    exec python app.py
fi