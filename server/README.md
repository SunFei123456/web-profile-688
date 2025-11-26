# 访客记录管理系统后端 API

基于 FastAPI 的访客记录管理系统后端服务。

## 功能特性

- ✅ 记录访客访问信息
- ✅ 分页查询访客列表
- ✅ 搜索访客记录
- ✅ 统计访客数据（总数、今日访客）
- ✅ MySQL 数据库存储
- ✅ RESTful API 设计
- ✅ CORS 跨域支持
- ✅ 自动生成 API 文档

## 技术栈

- **FastAPI**: 现代高性能 Web 框架
- **MySQL**: 企业级关系型数据库
- **PyMySQL**: Python MySQL 客户端
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI 服务器

## 前置要求

1. **Python 3.7+**
2. **MySQL 5.7+ 或 MariaDB 10.2+**

## 安装 MySQL

### macOS
```bash
brew install mysql
brew services start mysql
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

### Windows
下载并安装 MySQL Community Server: https://dev.mysql.com/downloads/mysql/

## 配置数据库

### 方式一：使用环境变量

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=visitor_db
```

### 方式二：修改配置文件

编辑 `config.py` 文件，直接修改数据库连接信息：

```python
DB_CONFIG: Dict[str, any] = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'visitor_db',
}
```

### 方式三：创建 MySQL 用户（推荐）

```sql
-- 登录 MySQL
mysql -u root -p

-- 创建数据库和用户
CREATE DATABASE visitor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'visitor_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON visitor_db.* TO 'visitor_user'@'localhost';
FLUSH PRIVILEGES;
```

然后配置对应的用户名和密码。

## 安装 Python 依赖

```bash
# 进入 server 目录
cd server

# 安装依赖
pip install -r requirements.txt
```

## 运行服务

```bash
# 开发模式（自动重载）
python main.py

# 或使用 uvicorn 命令
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后：
- API 地址: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 备用文档: http://localhost:8000/redoc

## API 端点

### 1. 记录访客访问
```
POST /api/visit
```

请求体：
```json
{
  "ip": "192.168.1.1",
  "page": "index.html",
  "browser": "Chrome",
  "os": "Windows 10",
  "user_agent": "Mozilla/5.0...",
  "referrer": "https://google.com"
}
```

### 2. 获取访客列表（分页）
```
GET /api/visitors?page=1&pageSize=10&search=关键词
```

参数：
- `page`: 页码（默认 1）
- `pageSize`: 每页数量（默认 10，最大 100）
- `search`: 搜索关键词（可选）

响应：
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "ip": "192.168.1.1",
      "timestamp": "2024-01-01 12:00:00",
      "page": "index.html",
      "browser": "Chrome",
      "os": "Windows 10",
      "user_agent": "...",
      "referrer": "..."
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 10,
    "total": 100,
    "totalPages": 10
  }
}
```

### 3. 获取统计信息
```
GET /api/stats
```

响应：
```json
{
  "success": true,
  "stats": {
    "total": 1000,
    "today": 50
  }
}
```

### 4. 健康检查
```
GET /health
```

## 数据库

使用 MySQL 数据库存储访客记录，支持高并发和大数据量场景。

### 表结构

**visitors 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键，自增 |
| ip | VARCHAR(45) | IP 地址（支持 IPv4 和 IPv6） |
| timestamp | DATETIME | 访问时间 |
| page | VARCHAR(255) | 访问页面 |
| browser | VARCHAR(100) | 浏览器 |
| os | VARCHAR(100) | 操作系统 |
| user_agent | TEXT | User Agent |
| referrer | VARCHAR(500) | 来源页面 |
| created_at | DATETIME | 记录创建时间 |

### 索引
- `idx_timestamp`: 时间索引，加速按时间查询
- `idx_ip`: IP 索引，加速按 IP 查询

### 数据库特性
- 字符集：`utf8mb4`（支持 Emoji 和特殊字符）
- 排序规则：`utf8mb4_unicode_ci`
- 存储引擎：`InnoDB`（支持事务和外键）

## 项目结构

```
server/
├── main.py           # FastAPI 应用主文件
├── models.py         # Pydantic 数据模型
├── database.py       # 数据库连接和初始化
├── crud.py           # 数据库操作函数
├── config.py         # 数据库配置文件
├── requirements.txt  # Python 依赖
├── README.md         # 项目说明文档
├── start.sh          # Linux/Mac 启动脚本
├── start.bat         # Windows 启动脚本
└── .gitignore        # Git 忽略文件
```

## 开发说明

### 添加新的 API 端点

在 `main.py` 中添加新的路由：

```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"message": "新端点"}
```

### 修改数据模型

在 `models.py` 中添加或修改 Pydantic 模型：

```python
class NewModel(BaseModel):
    field: str
```

### 数据库操作

在 `crud.py` 中添加新的数据库操作函数：

```python
def new_db_function(db):
    cursor = db.cursor()
    # 数据库操作
    pass
```

## 部署建议

### 生产环境配置

1. **数据库安全**
   - 使用独立的数据库用户，避免使用 root
   - 设置强密码
   - 限制数据库访问 IP
   - 定期备份数据库

2. **应用配置**
   - 配置具体的 CORS 允许域名
   - 添加身份验证和授权机制
   - 使用环境变量管理敏感配置
   - 配置日志系统
   - 使用 Gunicorn 作为进程管理器

3. **性能优化**
   - 配置数据库连接池
   - 添加 Redis 缓存层
   - 使用 CDN 加速静态资源
   - 配置负载均衡

### 示例部署命令

```bash
# 使用 Gunicorn + Uvicorn Workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 或使用 systemd 服务
sudo systemctl start visitor-api
```

### Docker 部署

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 注意事项

- ⚠️ 首次运行前请确保 MySQL 服务已启动
- ⚠️ 首次运行会自动创建数据库和表结构
- ⚠️ 自动插入 100 条测试数据（仅在数据库为空时）
- ⚠️ 开发模式下 CORS 允许所有来源，生产环境需要修改
- ⚠️ 请修改 `config.py` 中的默认数据库密码
- ⚠️ 生产环境建议使用环境变量配置敏感信息

## 许可证

MIT License

