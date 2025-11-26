from datetime import datetime
from models import VisitorCreate, VisitorResponse
from typing import List, Tuple

def create_visitor(db, visitor: VisitorCreate) -> int:
    """创建新的访客记录"""
    cursor = db.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO visitors (ip, timestamp, page, browser, os, user_agent, referrer, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        visitor.ip,
        now,
        visitor.page,
        visitor.browser,
        visitor.os,
        visitor.user_agent,
        visitor.referrer,
        now
    ))
    
    db.commit()
    return cursor.lastrowid

def get_visitors_paginated(db, page: int, page_size: int) -> Tuple[List[VisitorResponse], int]:
    """获取分页的访客列表"""
    cursor = db.cursor()
    
    # 获取总数
    cursor.execute('SELECT COUNT(*) as count FROM visitors')
    result = cursor.fetchone()
    total = result['count'] if result else 0
    
    # 获取分页数据
    offset = (page - 1) * page_size
    cursor.execute('''
        SELECT id, ip, timestamp, page, browser, os, user_agent, referrer
        FROM visitors
        ORDER BY timestamp DESC
        LIMIT %s OFFSET %s
    ''', (page_size, offset))
    
    rows = cursor.fetchall()
    visitors = [
        VisitorResponse(
            id=row['id'],
            ip=row['ip'],
            timestamp=str(row['timestamp']),
            page=row['page'],
            browser=row['browser'],
            os=row['os'],
            user_agent=row['user_agent'],
            referrer=row['referrer']
        )
        for row in rows
    ]
    
    return visitors, total

def search_visitors(db, search_term: str, page: int, page_size: int) -> Tuple[List[VisitorResponse], int]:
    """搜索访客记录"""
    cursor = db.cursor()
    
    search_pattern = f"%{search_term}%"
    
    # 获取搜索结果总数
    cursor.execute('''
        SELECT COUNT(*) as count FROM visitors
        WHERE ip LIKE %s OR page LIKE %s OR browser LIKE %s OR os LIKE %s
    ''', (search_pattern, search_pattern, search_pattern, search_pattern))
    
    result = cursor.fetchone()
    total = result['count'] if result else 0
    
    # 获取分页搜索结果
    offset = (page - 1) * page_size
    cursor.execute('''
        SELECT id, ip, timestamp, page, browser, os, user_agent, referrer
        FROM visitors
        WHERE ip LIKE %s OR page LIKE %s OR browser LIKE %s OR os LIKE %s
        ORDER BY timestamp DESC
        LIMIT %s OFFSET %s
    ''', (search_pattern, search_pattern, search_pattern, search_pattern, page_size, offset))
    
    rows = cursor.fetchall()
    visitors = [
        VisitorResponse(
            id=row['id'],
            ip=row['ip'],
            timestamp=str(row['timestamp']),
            page=row['page'],
            browser=row['browser'],
            os=row['os'],
            user_agent=row['user_agent'],
            referrer=row['referrer']
        )
        for row in rows
    ]
    
    return visitors, total

def get_total_visitors(db) -> int:
    """获取总访客数"""
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM visitors')
    result = cursor.fetchone()
    return result['count'] if result else 0

def get_today_visitors(db) -> int:
    """获取今日访客数"""
    cursor = db.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COUNT(*) as count FROM visitors
        WHERE timestamp >= %s AND timestamp < DATE_ADD(%s, INTERVAL 1 DAY)
    ''', (today, tomorrow))
    result = cursor.fetchone()
    return result['count'] if result else 0

def get_visitor_by_id(db, visitor_id: int) -> VisitorResponse:
    """根据 ID 获取访客记录"""
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, ip, timestamp, page, browser, os, user_agent, referrer
        FROM visitors
        WHERE id = %s
    ''', (visitor_id,))
    
    row = cursor.fetchone()
    if row:
        return VisitorResponse(
            id=row['id'],
            ip=row['ip'],
            timestamp=str(row['timestamp']),
            page=row['page'],
            browser=row['browser'],
            os=row['os'],
            user_agent=row['user_agent'],
            referrer=row['referrer']
        )
    return None

def delete_visitor(db, visitor_id: int) -> bool:
    """删除访客记录"""
    cursor = db.cursor()
    cursor.execute('DELETE FROM visitors WHERE id = %s', (visitor_id,))
    db.commit()
    return cursor.rowcount > 0

