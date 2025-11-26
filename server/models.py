from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# 访客创建模型
class VisitorCreate(BaseModel):
    ip: str = Field(..., description="IP 地址")
    page: str = Field(..., description="访问页面")
    browser: str = Field(..., description="浏览器")
    os: str = Field(..., description="操作系统")
    user_agent: Optional[str] = Field(None, description="User Agent")
    referrer: Optional[str] = Field(None, description="来源页面")

    class Config:
        json_schema_extra = {
            "example": {
                "ip": "192.168.1.1",
                "page": "index.html",
                "browser": "Chrome",
                "os": "Windows 10",
                "user_agent": "Mozilla/5.0...",
                "referrer": "https://google.com"
            }
        }

# 访客响应模型
class VisitorResponse(BaseModel):
    id: int
    ip: str
    timestamp: str
    page: str
    browser: str
    os: str
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

    class Config:
        from_attributes = True

# 分页信息模型
class PaginationInfo(BaseModel):
    page: int
    pageSize: int
    total: int
    totalPages: int

# 访客列表响应模型
class VisitorListResponse(BaseModel):
    success: bool
    data: List[VisitorResponse]
    pagination: PaginationInfo

# 统计信息模型
class Stats(BaseModel):
    total: int
    today: int

# 统计响应模型
class StatsResponse(BaseModel):
    success: bool
    stats: Stats

