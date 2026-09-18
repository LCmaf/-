# 医疗器械产品技术要求生成器

## 功能特点

1. **实时标准查询**：通过Playwright自动查询全国标准信息公共服务平台，确保标准信息准确、最新
2. **智能表单填写**：根据产品信息自动匹配相关标准
3. **文档预览**：实时预览生成的产品技术要求文档
4. **多格式导出**：支持导出PDF和Word格式

## 系统架构

```
┌─────────────────────────────────────┐
│           前端HTML页面              │
│  (product-requirement-generator.html)│
└──────────────┬──────────────────────┘
               │ API调用
               ▼
┌─────────────────────────────────────┐
│         Python后端服务              │
│    (standard_search_server.py)      │
└──────────────┬──────────────────────┘
               │ Playwright自动化
               ▼
┌─────────────────────────────────────┐
│    全国标准信息公共服务平台         │
│      (https://std.samr.gov.cn)      │
└─────────────────────────────────────┘
```

## 安装步骤

### 1. 安装Python依赖

```bash
pip install fastapi uvicorn playwright
playwright install chromium
```

### 2. 启动后端服务

**Windows用户：**
双击运行 `start_server.bat`

**Mac/Linux用户：**
```bash
python standard_search_server.py
```

### 3. 打开前端页面

直接在浏览器中打开 `product-requirement-generator.html`

## 使用方法

1. **填写产品信息**：在左侧表单中填写产品名称、型号规格、性能指标等信息
2. **搜索适用标准**：点击"🔍 搜索适用标准"按钮，系统会自动查询全国标准信息公共服务平台
3. **查看搜索结果**：点击标准链接可查看详细信息
4. **预览文档**：右侧会实时显示生成的产品技术要求文档
5. **导出文档**：点击"导出PDF"或"导出Word"按钮保存文档

## 文件说明

- `product-requirement-generator.html` - 前端页面
- `standard_search_server.py` - Python后端服务
- `start_server.bat` - Windows启动脚本
- `README.md` - 本文档

## 注意事项

1. 后端服务需要在本地运行（http://localhost:8000）
2. 首次运行会自动安装Playwright浏览器
3. 查询结果来自全国标准信息公共服务平台，确保数据权威性
4. 如果查询失败，请检查网络连接或稍后重试

## 技术栈

- **前端**：HTML + CSS + JavaScript
- **后端**：Python + FastAPI + Playwright
- **数据源**：全国标准信息公共服务平台（https://std.samr.gov.cn）

## 许可证

MIT License
