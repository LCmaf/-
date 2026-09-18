"""
标准搜索服务器 - 使用Playwright实时查询全国标准信息公共服务平台
"""
import asyncio
import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright

app = FastAPI(title="标准搜索服务器")

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def search_standards_from_sac(keyword: str):
    """从全国标准信息公共服务平台搜索标准"""
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 访问全国标准信息公共服务平台
            url = f"https://std.samr.gov.cn/search/std?q={keyword}"
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # 等待搜索结果加载
            await page.wait_for_selector(".result-item, .search-result, .std-item", timeout=10000)
            
            # 提取搜索结果
            items = await page.query_selector_all(".result-item, .search-result, .std-item")
            
            for item in items[:10]:  # 最多取10条
                try:
                    # 提取标准号
                    std_id_elem = await item.query_selector(".std-id, .standard-id, a[href*='std']")
                    std_id = await std_id_elem.inner_text() if std_id_elem else ""
                    
                    # 提取标准名称
                    std_name_elem = await item.query_selector(".std-name, .standard-name, .title")
                    std_name = await std_name_elem.inner_text() if std_name_elem else ""
                    
                    # 提取状态
                    status_elem = await item.query_selector(".status, .std-status")
                    status = await status_elem.inner_text() if status_elem else ""
                    
                    # 提取发布日期和实施日期
                    date_elem = await item.query_selector(".date, .std-date")
                    date_text = await date_elem.inner_text() if date_elem else ""
                    
                    if std_id or std_name:
                        results.append({
                            "id": std_id.strip(),
                            "title": std_name.strip(),
                            "status": status.strip(),
                            "date": date_text.strip(),
                            "source": "全国标准信息公共服务平台"
                        })
                except Exception as e:
                    continue
            
            # 如果没有找到结果，尝试其他选择器
            if not results:
                # 尝试更通用的选择器
                all_links = await page.query_selector_all("a[href*='std'], a[href*='gbDetailed']")
                for link in all_links[:10]:
                    try:
                        text = await link.inner_text()
                        href = await link.get_attribute("href")
                        if text and len(text) > 5:
                            results.append({
                                "id": text.strip(),
                                "title": "",
                                "status": "",
                                "date": "",
                                "source": "全国标准信息公共服务平台",
                                "url": href
                            })
                    except:
                        continue
        
        except Exception as e:
            print(f"搜索出错: {e}")
        
        finally:
            await browser.close()
    
    return results

@app.get("/api/search")
async def search_standards(keyword: str = Query(..., description="搜索关键词")):
    """搜索标准API"""
    results = await search_standards_from_sac(keyword)
    return {
        "keyword": keyword,
        "count": len(results),
        "results": results
    }

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
