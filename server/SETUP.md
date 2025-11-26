# 快速设置指南

本指南将帮助您快速设置和运行访客记录管理系统。

## 步骤 1: 安装 MySQL

### macOS
```bash
# 使用 Homebrew 安装
brew install mysql

# 启动 MySQL 服务
brew services start mysql

# 安全配置（可选）
mysql_secure_installation
```

### Ubuntu/Debian
```bash
# 安装 MySQL
sudo apt update
sudo apt install mysql-server

# 启动服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 安全配置
sudo mysql_secure_installation
```

### Windows
1. 下载 MySQL Community Server: https://dev.mysql.com/downloads/mysql/
2. 运行安装程序
3. 记住设置的 root 密码

## 步骤 2: 创建数据库和用户

登录 MySQL：
```bash
mysql -u root -p
```

执行以下 SQL 命令：
```sql
-- 创建数据库
CREATE DATABASE visitor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建专用用户（推荐）
CREATE USER 'visitor_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- 授予权限
GRANT ALL PRIVILEGES ON visitor_db.* TO 'visitor_user'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 退出
EXIT;
```

## 步骤 3: 配置应用

编辑 `config.py` 文件：

```python
DB_CONFIG: Dict[str, any] = {
    'host': 'localhost',
    'port': 3306,
    'user': 'visitor_user',          # 修改为你的用户名
    'password': 'your_secure_password',  # 修改为你的密码
    'database': 'visitor_db',
}
```

或者使用环境变量（推荐）：

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=visitor_user
export DB_PASSWORD=your_secure_password
export DB_NAME=visitor_db
```

## 步骤 4: 安装 Python 依赖

```bash
# 进入 server 目录
cd server

# 创建虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 步骤 5: 运行服务

### 方式一：使用启动脚本（推荐）

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

### 方式二：直接运行

```bash
python main.py
```

## 步骤 6: 验证安装

打开浏览器访问：

1. **API 文档**: http://localhost:8000/docs
2. **健康检查**: http://localhost:8000/health
3. **统计信息**: http://localhost:8000/api/stats

如果看到正常的响应，说明安装成功！

## 常见问题

### 问题 1: 无法连接到 MySQL

**解决方法:**
1. 检查 MySQL 服务是否运行
   ```bash
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status mysql
   
   # Windows
   services.msc（查看 MySQL 服务）
   ```

2. 检查用户名和密码是否正确
3. 检查 MySQL 端口是否为 3306

### 问题 2: Access denied for user

**解决方法:**
1. 确认用户已创建且密码正确
2. 检查用户权限：
   ```sql
   SHOW GRANTS FOR 'visitor_user'@'localhost';
   ```

### 问题 3: Database does not exist

**解决方法:**
应用会自动创建数据库。如果失败，请手动创建：
```sql
CREATE DATABASE visitor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 问题 4: 依赖安装失败

**解决方法:**
1. 更新 pip: `pip install --upgrade pip`
2. 使用国内镜像源:
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

### 问题 5: 端口 8000 已被占用

**解决方法:**
修改 `main.py` 中的端口：
```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8001,  # 修改为其他端口
    reload=True
)
```

## 下一步

- 访问 http://localhost:8000/docs 查看完整的 API 文档
- 打开管理页面 `../admin/index.html` 查看访客记录
- 阅读 `README.md` 了解更多功能和配置选项

## 获取帮助

如果遇到其他问题，请查看：
1. 项目 README.md
2. FastAPI 官方文档: https://fastapi.tiangolo.com/
3. MySQL 官方文档: https://dev.mysql.com/doc/

祝使用愉快！ 🎉

