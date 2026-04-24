#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巨潮资讯网财报下载器 - Playwright 版本
使用浏览器自动化技术，模拟真实用户行为
"""

import os
import json
import datetime
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class CnInfoPlaywrightDownloader:
    """使用 Playwright 从巨潮资讯网下载财报"""

    def __init__(self, headless: bool = True):
        """
        初始化
        
        Args:
            headless: 是否无头模式（默认 True）
        """
        self.headless = headless
        self.base_url = "http://www.cninfo.com.cn/"
        self.search_url = "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index"
        
    def _detect_market(self, stock_code: str) -> str:
        """根据股票代码自动检测市场"""
        if len(stock_code) == 5 and stock_code.startswith(("00", "01", "02", "09")):
            return "hke"
        if len(stock_code) == 6:
            if stock_code.startswith("6") or stock_code.startswith("9"):
                return "sse"  # 上交所
            else:
                return "szse"  # 深交所
        return "szse"
    
    def _get_org_id(self, stock_code: str, market: str) -> str:
        """获取股票的 orgId"""
        if market == "sse":
            return f"gssh0{stock_code}"
        elif market == "szse":
            return f"ssessz{stock_code}"
        elif market == "hke":
            return f"hke{stock_code}"
        return f"ssessz{stock_code}"
    
    def search_announcements(self, stock_code: str, years: list = None, report_types: list = None):
        """
        使用浏览器搜索公告
        
        Args:
            stock_code: 股票代码
            years: 年份列表（如 [2020, 2021, 2022, 2023, 2024]）
            report_types: 报告类型（['年报', '一季报', '中报', '三季报']）
            
        Returns:
            announcements: 公告列表
        """
        if years is None:
            current_year = datetime.datetime.now().year
            years = list(range(current_year - 5, current_year))
        
        if report_types is None:
            report_types = ['年报', '一季报', '中报', '三季报']
        
        all_announcements = []
        
        with sync_playwright() as p:
            # 启动浏览器
            print("🚀 启动浏览器...")
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            try:
                # 1. 访问首页
                print(f"📡 访问巨潮资讯网...")
                page.goto(self.search_url, timeout=60000)
                time.sleep(3)  # 等待页面完全加载
                
                # 2. 点击搜索框，输入股票代码
                print(f"🔍 搜索股票：{stock_code}...")
                
                # 查找搜索输入框
                search_input = page.locator('input[placeholder*="证券代码"]').first
                if not search_input.count():
                    search_input = page.locator('input[type="text"]').first
                
                search_input.fill(stock_code)
                time.sleep(1)
                
                # 3. 按回车键搜索
                search_input.press("Enter")
                time.sleep(3)  # 等待搜索结果加载
                
                # 4. 检查是否找到股票
                stock_element = page.locator(f'text={stock_code}').first
                if stock_element.count():
                    print(f"✅ 找到股票 {stock_code}")
                    stock_element.click()
                    time.sleep(2)
                else:
                    print(f"❌ 未找到股票 {stock_code}")
                    return []
                
                # 5. 设置时间范围（查询近 5 年）
                start_year = min(years)
                end_year = max(years) + 1
                
                print(f"📅 设置时间范围：{start_year} 年到 {end_year} 年...")
                
                # 查找日期选择器并设置
                try:
                    date_start = page.locator('input[placeholder*="开始日期"]').first
                    date_end = page.locator('input[placeholder*="结束日期"]').first
                    
                    date_start.fill(f"{start_year}-01-01")
                    date_end.fill(f"{end_year}-12-31")
                    time.sleep(1)
                    
                    # 点击搜索按钮
                    search_btn = page.locator('button:has-text("搜索"), button:has-text("查询")').first
                    if search_btn.count():
                        search_btn.click()
                        time.sleep(3)
                except Exception as e:
                    print(f"⚠️ 设置日期失败：{e}")
                
                # 6. 收集所有公告
                print("📊 收集公告信息...")
                
                for page_num in range(1, 6):  # 最多翻 5 页
                    try:
                        # 等待公告列表加载
                        page.wait_for_selector('.announcement-list tr, .result-item', timeout=10000)
                        
                        # 查找所有公告项
                        announcement_items = page.locator('.announcement-list tr').all()
                        if not announcement_items:
                            announcement_items = page.locator('.result-item').all()
                        
                        if not announcement_items:
                            print(f"  ⚠️ 第{page_num}页没有找到公告")
                            break
                        
                        print(f"  📄 第{page_num}页，找到{len(announcement_items)}条公告")
                        
                        for item in announcement_items:
                            try:
                                title_elem = item.locator('.announcement-title, .title-link, a').first
                                if title_elem.count():
                                    title = title_elem.inner_text().strip()
                                    
                                    # 检查是否是目标报告类型
                                    is_target = any(rt in title for rt in report_types)
                                    if is_target:
                                        # 提取其他信息
                                        date_elem = item.locator('.date, .time, td:last-child').first
                                        pub_date = date_elem.inner_text().strip() if date_elem.count() else ""
                                        
                                        # 尝试获取 PDF 链接
                                        pdf_link = None
                                        try:
                                            link_elem = item.locator('a[href*=".pdf"]').first
                                            if link_elem.count():
                                                pdf_link = link_elem.get_attribute('href')
                                        except:
                                            pass
                                        
                                        announcement = {
                                            'title': title,
                                            'pubDate': pub_date,
                                            'pdfLink': pdf_link,
                                            'secCode': stock_code,
                                        }
                                        all_announcements.append(announcement)
                            except Exception as e:
                                continue
                        
                        # 尝试翻页
                        if page_num < 5:
                            next_btn = page.locator('a:has-text("下一页"), button:has-text("下一页"), .next-page').first
                            if next_btn.count() and "disabled" not in next_btn.get_attribute("class", ""):
                                next_btn.click()
                                time.sleep(2)
                            else:
                                print("  已经是最后一页")
                                break
                    except PlaywrightTimeout:
                        print(f"  ⚠️ 第{page_num}页超时")
                        break
                
            except Exception as e:
                print(f"❌ 浏览过程中出错：{e}")
                import traceback
                traceback.print_exc()
            finally:
                browser.close()
        
        print(f"✅ 共收集到{len(all_announcements)}条公告")
        return all_announcements
    
    def download_pdf(self, announcement: dict, output_dir: str) -> str:
        """
        下载 PDF 文件
        
        Args:
            announcement: 公告信息
            output_dir: 输出目录
            
        Returns:
            文件路径或 None
        """
        if not announcement.get('pdfLink'):
            return None
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context(
                    accept_downloads=True,
                    viewport={"width": 1920, "height": 1080}
                )
                page = context.new_page()
                
                # 设置下载路径
                page.set_default_timeout(60000)
                
                # 访问 PDF 链接
                pdf_url = announcement['pdfLink']
                if not pdf_url.startswith('http'):
                    pdf_url = f"http://static.cninfo.com.cn{pdf_url}"
                
                print(f"  下载中：{announcement['title'][:50]}...")
                
                # 导航到 PDF URL
                response = page.goto(pdf_url)
                
                if response and response.status == 200:
                    # 保存文件
                    filename = f"{announcement['secCode']}_{announcement['title'][:100]}.pdf"
                    filename = "".join(c for c in filename if c.isalnum() or c in "._-")
                    filepath = os.path.join(output_dir, filename)
                    
                    # 保存 PDF
                    pdf_content = response.body()
                    with open(filepath, 'wb') as f:
                        f.write(pdf_content)
                    
                    print(f"  ✅ 已下载：{os.path.basename(filepath)}")
                    return filepath
                else:
                    print(f"  ⚠️ 下载失败：{response.status if response else 'Unknown'}")
                    return None
                    
        except Exception as e:
            print(f"  ❌ 下载出错：{e}")
            return None
        finally:
            if 'browser' in locals():
                browser.close()


def download_reports_playwright(stock_input: str, output_dir: str = None, headless: bool = True) -> dict:
    """
    使用 Playwright 下载股票财报
    
    Args:
        stock_input: 股票代码或名称
        output_dir: 输出目录
        headless: 是否无头模式
        
    Returns:
        包含下载结果的字典
    """
    if output_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "reports", "financial_reports")
        os.makedirs(output_dir, exist_ok=True)
    
    downloader = CnInfoPlaywrightDownloader(headless=headless)
    
    # 检测市场
    market = downloader._detect_market(stock_input)
    
    # 搜索公告
    print(f"\n🔍 开始搜索 {stock_input} 的公告...")
    announcements = downloader.search_announcements(stock_input)
    
    if not announcements:
        return {"error": f"未找到股票 {stock_input} 的公告"}
    
    # 下载报告
    print(f"\n📥 开始下载 PDF 文件...")
    downloaded_files = []
    
    for ann in announcements:
        filepath = downloader.download_pdf(ann, output_dir)
        if filepath:
            downloaded_files.append(filepath)
    
    return {
        "stock_code": stock_input,
        "stock_name": stock_input,
        "market": market,
        "output_dir": output_dir,
        "files": downloaded_files,
        "total_found": len(announcements),
        "total_downloaded": len(downloaded_files),
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python cninfo_playwright.py <股票代码> [输出目录]")
        print("示例：python cninfo_playwright.py 603501")
        sys.exit(1)
    
    stock_input = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = download_reports_playwright(stock_input, output_dir, headless=True)
    
    if "error" in result:
        print(f"❌ 错误：{result['error']}")
    else:
        print(f"\n{'='*60}")
        print(f"✅ 下载完成")
        print(f"   找到公告：{result['total_found']} 条")
        print(f"   成功下载：{result['total_downloaded']} 份")
        print(f"   保存位置：{result['output_dir']}")
        if result['files']:
            print(f"\n文件列表:")
            for f in result['files']:
                print(f"  {os.path.basename(f)}")
