from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
import uvicorn

from database import init_db, get_db
from models import VisitorCreate, VisitorResponse, VisitorListResponse, StatsResponse
from crud import (
    create_visitor,
    get_visitors_paginated,
    get_total_visitors,
    get_today_visitors,
    search_visitors
)

# 创建 FastAPI 应用
app = FastAPI(
    title="访客记录管理系统",
    description="个人网站访客记录管理 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()
    print("数据库初始化完成")

# 根路径
@app.get("/")
async def root():
    return {
        "message": "访客记录管理系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# 记录访客访问
@app.post("/api/visit", response_model=dict)
async def record_visit(visitor: VisitorCreate):
    """记录新的访客访问"""
    db = get_db()
    visitor_id = create_visitor(db, visitor)
    db.close()
    
    return {
        "success": True,
        "message": "访问记录成功",
        "visitor_id": visitor_id
    }

# 获取访客列表（分页）
@app.get("/api/visitors", response_model=VisitorListResponse)
async def get_visitors(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词")
):
    """获取访客列表，支持分页和搜索"""
    db = get_db()
    
    if search:
        visitors, total = search_visitors(db, search, page, pageSize)
    else:
        visitors, total = get_visitors_paginated(db, page, pageSize)
    
    db.close()
    
    total_pages = (total + pageSize - 1) // pageSize
    
    return {
        "success": True,
        "data": visitors,
        "pagination": {
            "page": page,
            "pageSize": pageSize,
            "total": total,
            "totalPages": total_pages
        }
    }

# 获取统计信息
@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """获取访客统计信息"""
    db = get_db()
    
    total = get_total_visitors(db)
    today = get_today_visitors(db)
    
    db.close()
    
    return {
        "success": True,
        "stats": {
            "total": total,
            "today": today
        }
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    # 运行服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式，自动重载
        log_level="info"
    )

