# 访客记录管理后台

访客记录管理系统的前端管理界面。

## API 配置

当前已配置的后端 API 地址：
```
http://122.51.104.18:18888
```

如需修改 API 地址，请编辑 `index.html` 文件中的 `API_BASE_URL` 变量：

```javascript
// API 基础 URL
const API_BASE_URL = 'http://your-api-address:port';
```

## 功能特性

### 📊 数据统计
- **总访客数**: 显示所有访客记录总数
- **今日访客**: 显示当天的访客数量
- 数据实时从后端 API 获取

### 📋 访客列表
- **字段显示**: 
  - 序号
  - IP 地址
  - 访问时间
  - 访问页面
  - 浏览器
  - 操作系统

### 🔍 搜索功能
- 支持按以下字段搜索：
  - IP 地址
  - 访问页面
  - 浏览器
  - 操作系统
- 支持回车键快速搜索

### 📄 分页功能
- 可自定义每页显示数量：10/20/50/100 条
- 完整的分页控制：首页、上一页、页码、下一页、尾页
- 智能省略号显示（页数过多时）
- 显示当前记录范围和总记录数

### 🎨 界面特点
- 现代化渐变色设计
- 响应式布局，支持移动端
- 加载动画效果
- 错误状态提示
- 表格行悬停效果

## API 接口

### 1. 获取统计信息
```
GET /api/stats
```

**响应示例:**
```json
{
  "success": true,
  "stats": {
    "total": 1000,
    "today": 50
  }
}
```

### 2. 获取访客列表
```
GET /api/visitors?page=1&pageSize=10&search=关键词
```

**参数:**
- `page`: 页码（默认 1）
- `pageSize`: 每页数量（默认 10）
- `search`: 搜索关键词（可选）

**响应示例:**
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
      "os": "Windows 10"
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

## 使用方法

### 本地访问
直接在浏览器中打开 `index.html` 文件即可。

### 服务器部署
将文件上传到 Web 服务器，通过浏览器访问对应的 URL。

### CORS 配置
如果遇到跨域问题，需要确保后端 API 已配置正确的 CORS 设置：
- 允许来源: `*` 或特定域名
- 允许方法: `GET, POST, OPTIONS`
- 允许头: `Content-Type`

## 故障排除

### 问题 1: 无法连接到服务器

**可能原因:**
1. API 地址配置错误
2. 后端服务未启动
3. 网络连接问题
4. CORS 配置问题

**解决方法:**
1. 检查 `API_BASE_URL` 配置
2. 确认后端服务正在运行
3. 打开浏览器开发者工具（F12）查看网络请求
4. 检查后端 CORS 配置

### 问题 2: 数据显示为 "-"

**可能原因:**
统计接口请求失败

**解决方法:**
1. 检查后端 `/api/stats` 接口是否正常
2. 查看浏览器控制台错误信息

### 问题 3: 搜索无结果

**可能原因:**
1. 搜索关键词不匹配
2. 数据库中确实没有匹配的记录

**解决方法:**
1. 尝试使用更通用的关键词
2. 清空搜索框查看全部数据

## 开发说明

### 修改样式
在 `<style>` 标签中修改 CSS 样式。

主要颜色变量：
```css
background: #c79b5c;           /* 页面背景色 */
background: #b36901;           /* 顶部导航栏背景色 */
background: #667eea;           /* 按钮主色调 */
```

### 添加新字段
如果后端 API 返回了新的字段，需要：

1. 修改表头：
```html
<th>新字段名</th>
```

2. 修改表格渲染逻辑：
```javascript
<td>${visitor.newField}</td>
```

### 自定义分页数量
在 HTML 中添加新的选项：
```html
<select id="page-size" onchange="changePageSize()">
    <option value="10">每页 10 条</option>
    <option value="20">每页 20 条</option>
    <option value="50">每页 50 条</option>
    <option value="100">每页 100 条</option>
    <option value="200">每页 200 条</option> <!-- 新增 -->
</select>
```

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

建议使用现代浏览器以获得最佳体验。

## 技术栈

- **HTML5**: 页面结构
- **CSS3**: 样式和动画
- **JavaScript ES6+**: 交互逻辑
- **Fetch API**: 数据请求
- **Font Awesome 5**: 图标库

## 更新日志

### v1.1.0 (2025-01-30)
- ✅ 连接真实后端 API
- ✅ 移除模拟数据
- ✅ 添加加载状态
- ✅ 添加错误处理
- ✅ 优化分页逻辑

### v1.0.0 (2025-01-29)
- ✅ 初始版本
- ✅ 基础功能实现
- ✅ 使用模拟数据

## 许可证

MIT License

