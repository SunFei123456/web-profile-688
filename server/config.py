"""
数据库配置文件
支持从环境变量或 .env 文件读取配置
"""

import os
from typing import Dict

# 尝试加载 .env 文件（如果存在）
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ 已加载 .env 配置文件")
except ImportError:
    print("ℹ 未安装 python-dotenv，将使用环境变量或默认配置")

# 数据库配置
DB_CONFIG: Dict[str, any] = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'visitor_db'),
}

# 显示配置信息（隐藏密码）
def print_config():
    """打印当前数据库配置（隐藏密码）"""
    safe_config = DB_CONFIG.copy()
    if safe_config.get('password'):
        safe_config['password'] = '***' + safe_config['password'][-2:] if len(safe_config['password']) > 2 else '***'
    
    print("\n数据库配置:")
    print(f"  - 主机: {safe_config['host']}")
    print(f"  - 端口: {safe_config['port']}")
    print(f"  - 用户: {safe_config['user']}")
    print(f"  - 密码: {safe_config['password']}")
    print(f"  - 数据库: {safe_config['database']}\n")

