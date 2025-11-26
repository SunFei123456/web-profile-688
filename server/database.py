import pymysql
from datetime import datetime
from config import DB_CONFIG

# MySQL 连接配置（添加额外的连接选项）
MYSQL_CONFIG = {
    **DB_CONFIG,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,  # 返回字典格式
    'autocommit': False
}

def get_db():
    """获取数据库连接"""
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        return conn
    except pymysql.Error as e:
        print(f"数据库连接失败: {e}")
        raise

def init_db():
    """初始化数据库和表"""
    try:
        # 首先连接到 MySQL 服务器（不指定数据库）
        temp_config = MYSQL_CONFIG.copy()
        db_name = temp_config.pop('database')
        
        conn = pymysql.connect(**temp_config)
        cursor = conn.cursor()
        
        # 创建数据库（如果不存在）
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {db_name}")
        print(f"✓ 数据库 '{db_name}' 已准备就绪")
        
        # 创建访客表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip VARCHAR(45) NOT NULL,
                timestamp DATETIME NOT NULL,
                page VARCHAR(255) NOT NULL,
                browser VARCHAR(100) NOT NULL,
                os VARCHAR(100) NOT NULL,
                user_agent TEXT,
                referrer VARCHAR(500),
                created_at DATETIME NOT NULL,
                INDEX idx_timestamp (timestamp),
                INDEX idx_ip (ip)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        conn.commit()
        print("✓ 数据表创建成功")
        
        # 检查是否需要插入测试数据
        cursor.execute('SELECT COUNT(*) as count FROM visitors')
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        if count == 0:
            print("📦 插入测试数据...")
            insert_sample_data(conn)
            # 重新获取数量
            cursor.execute('SELECT COUNT(*) as count FROM visitors')
            result = cursor.fetchone()
            count = result['count'] if result else 0
        
        conn.close()
        print(f"✓ 数据库初始化完成，当前记录数: {count}")
        
    except pymysql.Error as e:
        print(f"❌ 数据库初始化失败: {e}")
        raise

def insert_sample_data(conn):
    """插入示例数据"""
    import random
    from datetime import timedelta
    
    cursor = conn.cursor()
    
    pages = ['index.html', 'cv.html', 'research.html', 'design.html', 'contact.html']
    browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
    os_list = ['Windows 10', 'macOS', 'Linux', 'iOS', 'Android']
    
    now = datetime.now()
    
    # 生成 100 条测试数据
    for i in range(100):
        # 随机生成过去30天内的时间
        random_days = random.randint(0, 30)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        
        visit_time = now - timedelta(
            days=random_days,
            hours=random_hours,
            minutes=random_minutes
        )
        
        ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        page = random.choice(pages)
        browser = random.choice(browsers)
        os = random.choice(os_list)
        
        cursor.execute('''
            INSERT INTO visitors (ip, timestamp, page, browser, os, user_agent, referrer, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ip,
            visit_time.strftime('%Y-%m-%d %H:%M:%S'),
            page,
            browser,
            os,
            f"Mozilla/5.0 ({os}) {browser}",
            "https://google.com" if random.random() > 0.5 else "直接访问",
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
    
    conn.commit()
    print("测试数据插入完成")

