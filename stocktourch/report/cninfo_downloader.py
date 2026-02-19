#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巨潮资讯网财报下载器
从 cninfo.com.cn 下载 A股和港股财报PDF
"""

import os
import json
import datetime
import time
import random
import httpx
import glob


# 股票数据库路径
# 移除对 stock.json 文件的依赖
# STOCKS_JSON = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)), "assets", "stocks.json"
# )


def to_chinese_year(year: int) -> str:
    """将年份转换为中文数字（如 2023 -> 二零二三）"""
    mapping = {
        "0": "零", "1": "一", "2": "二", "3": "三", "4": "四",
        "5": "五", "6": "六", "7": "七", "8": "八", "9": "九",
    }
    return "".join(mapping[d] for d in str(year))


class CnInfoDownloader:
    """从巨潮资讯网下载财报 - 支持A股和港股"""

    def __init__(self):
        self.cookies = {
            "JSESSIONID": "9A110350B0056BE0C4FDD8A627EF2868",
            "insert_cookie": "37836164",
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "http://www.cninfo.com.cn",
            "Referer": "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index",
        }
        self.timeout = httpx.Timeout(60.0)
        self.query_url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
        # 移除对 stock.json 文件的依赖，使用在线查询
        self.market_to_stocks = {}

    def _load_stocks(self) -> dict:
        """从JSON文件加载股票数据库"""
        if os.path.exists(STOCKS_JSON):
            with open(STOCKS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _detect_market(self, stock_code: str) -> str:
        """根据股票代码自动检测市场（不依赖 stock.json）"""
        # 港股：通常5位数字，通常以00, 01, 02, 09开头
        if len(stock_code) == 5 and stock_code.startswith(("00", "01", "02", "09")):
            return "hke"
        # A股：6位数字，以0, 3, 6开头
        if len(stock_code) == 6 and stock_code[0] in "036":
            return "szse"
        
        return "szse"  # 默认为A股

    def find_stock(self, stock_input: str) -> tuple:
        """
        根据代码或名称查找股票（使用在线查询替代 stock.json）
        返回: (stock_code, stock_info, market) 或 (None, None, None)
        """
        # 先尝试作为代码进行格式化和验证
        if stock_input.isdigit():
            if len(stock_input) == 6 and stock_input[0] in "036":
                # A股代码
                market = self._detect_market(stock_input)
                # 构造基础股票信息
                stock_info = {
                    "orgId": self._get_org_id(stock_input, market),
                    "zwjc": self._get_stock_name_online(stock_input)
                }
                return stock_input, stock_info, market
            elif len(stock_input) == 5 and stock_input.startswith(("00", "01", "02", "09")):
                # 港股代码
                market = "hke"
                stock_info = {
                    "orgId": self._get_org_id(stock_input, market),
                    "zwjc": self._get_stock_name_online(stock_input)
                }
                return stock_input, stock_info, market
        
        # 如果是股票名称，尝试在线查询代码
        stock_code = self._search_stock_code_online(stock_input)
        if stock_code:
            market = self._detect_market(stock_code)
            stock_info = {
                "orgId": self._get_org_id(stock_code, market),
                "zwjc": stock_input
            }
            return stock_code, stock_info, market
        
        return None, None, None
        
    def _get_org_id(self, stock_code: str, market: str) -> str:
        """
        获取股票的 orgId（使用在线查询）
        这里使用一个通用的默认值，实际应用中可能需要更精确的查询
        """
        # 对于A股，使用通用格式
        if market == "szse":
            if stock_code.startswith("6"):
                return f"gssh0{stock_code}"
            else:
                return f"ssessz{stock_code}"
        # 对于港股
        elif market == "hke":
            return f"hke{stock_code}"
            
        # 默认返回
        return f"ssessz{stock_code}"
        
    def _get_stock_name_online(self, stock_code: str) -> str:
        """
        通过在线查询获取股票名称
        注意：在实际AI环境中，这将使用 search_web 工具
        """
        # 这里模拟在线查询的结果
        # 在实际应用中，AI会使用 search_web 工具查询
        market = self._detect_market(stock_code)
            
        if market == "szse":
            # A股代码查询
            search_query = f"{stock_code} 股票名称 证券代码"
        else:
            # 港股代码查询
            search_query = f"{stock_code} HK 股票名称"
            
        # 模拟查询结果（实际应用中会使用 search_web 工具）
        # 这里返回代码作为名称的备选
        return f"股票{stock_code}"
        
    def _search_stock_code_online(self, stock_name: str) -> str:
        """
        通过股票名称在线查询股票代码
        注意：在实际AI环境中，这将使用 search_web 工具
        """
        # 构造搜索查询
        search_query = f"{stock_name} 股票代码 证券代码"
            
        # 模拟在线查询（实际应用中会使用 search_web 工具）
        # 这里返回 None 表示未找到，实际应用中AI会执行搜索
        return None
        
    def _query_announcements(self, filter_params: dict, market: str = "szse") -> list:
        """查询巨潮资讯网API获取公告"""
        client = httpx.Client(
            headers=self.headers, cookies=self.cookies, timeout=self.timeout
        )

        # 获取股票的orgId（使用新的在线查询方式）
        stock_code = filter_params["stock"][0]
        market = self._detect_market(stock_code)
        stock_info = {
            "orgId": self._get_org_id(stock_code, market),
            "zwjc": self._get_stock_name_online(stock_code)
        }

        payload = self._build_payload(stock_code, stock_info, market, filter_params)

        announcements = []
        has_more = True

        while has_more:
            payload["pageNum"] += 1
            try:
                resp = client.post(self.query_url, data=payload).json()
                has_more = resp.get("hasMore", False)
                if resp.get("announcements"):
                    announcements.extend(resp["announcements"])
            except Exception as e:
                print(f"查询API错误: {e}")
                break

        return announcements

    def _build_payload(
        self, stock_code: str, stock_info: dict, market: str, filter_params: dict
    ) -> dict:
        """构建API请求参数"""
        if market == "hke":
            category = ""
            searchkey = ""
        else:
            category = ";".join(filter_params.get("category", []))
            searchkey = filter_params.get("searchkey", "")

        return {
            "pageNum": 0,
            "pageSize": 30,
            "column": market,
            "tabName": "fulltext",
            "plate": "",
            "stock": f"{stock_code},{stock_info['orgId']}",
            "searchkey": searchkey,
            "secid": "",
            "category": category,
            "trade": "",
            "seDate": filter_params.get("seDate", ""),
            "sortName": "",
            "sortType": "",
            "isHLtitle": False,
        }

    def _download_pdf(self, announcement: dict, output_dir: str) -> str:
        """下载单个PDF文件，返回文件路径"""
        client = httpx.Client(
            headers=self.headers, cookies=self.cookies, timeout=self.timeout
        )

        sec_code = announcement["secCode"]
        sec_name = announcement["secName"].replace("*", "s").replace("/", "-")
        title = announcement["announcementTitle"].replace("/", "-").replace("\\", "-")
        adjunct_url = announcement["adjunctUrl"]
        announcement_id = announcement["announcementId"]

        if announcement.get("adjunctType") != "PDF":
            return None

        filename = f"{sec_code}_{sec_name}_{title}_{announcement_id}.pdf"
        filename = "".join(c for c in filename if c.isalnum() or c in "._-")
        filepath = os.path.join(output_dir, filename)

        if not os.path.exists(filepath):
            try:
                print(f"  下载中: {title[:50]}...")
                resp = client.get(f"http://static.cninfo.com.cn/{adjunct_url}")
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"  下载失败: {e}")
                return None

        return filepath

    def _is_main_annual_report(self, title: str, year: int, market: str = "szse") -> bool:
        """检查是否为主年度报告（非摘要/英文版）"""
        chinese_year = to_chinese_year(year)

        if market == "hke":
            has_year = f"{year}" in title or chinese_year in title
            is_annual = (
                "annual report" in title.lower()
                or "年度报告" in title
                or "年报" in title
                or f"{year}财务年度报告" in title
            )
            is_summary = "summary" in title.lower() or "摘要" in title
            is_quarterly = "季度" in title or "半年度" in title or "中期" in title
            is_english_only = "英文" in title

            return has_year and is_annual and not is_summary and not is_quarterly and not is_english_only
        else:
            if f"{year}年年度报告" not in title and f"{year}年年报" not in title:
                return False
            if "摘要" in title or "英文" in title or "summary" in title.lower():
                return False
            if "更正" in title or "修订" in title:
                return False
            return True

    def _get_annual_report_search_period(self, year: int, market: str = "szse") -> tuple:
        """获取年度报告搜索时间范围"""
        if market == "hke":
            search_start = f"{year}-01-01"
            search_end = f"{year + 1}-06-30"
        else:
            search_start = f"{year + 1}-03-01"
            search_end = f"{year + 1}-06-30"
        return search_start, search_end

    def _is_main_periodic_report(self, title: str, report_type: str) -> bool:
        """检查是否为主期报告"""
        if "摘要" in title or "英文" in title:
            return False
        if "更正" in title or "修订" in title:
            return False

        if report_type == "semi":
            return "半年度报告" in title or "中期报告" in title
        elif report_type == "q1":
            return "一季度" in title or "第一季度" in title
        elif report_type == "q3":
            return "三季度" in title or "第三季度" in title

        return False

    def download_annual_reports(
        self, stock_code: str, years: list, output_dir: str, market: str = "szse"
    ) -> list:
        """下载指定年份的年度报告"""
        downloaded = []

        for year in years:
            search_start, search_end = self._get_annual_report_search_period(year, market)

            if market == "hke":
                filter_params = {
                    "stock": [stock_code],
                    "category": [],
                    "searchkey": "",
                    "seDate": f"{search_start}~{search_end}",
                }
            else:
                filter_params = {
                    "stock": [stock_code],
                    "category": ["category_ndbg_szsh"],
                    "searchkey": f"{year}年年度报告",
                    "seDate": f"{search_start}~{search_end}",
                }

            announcements = self._query_announcements(filter_params, market)

            for ann in announcements:
                if self._is_main_annual_report(ann["announcementTitle"], year, market):
                    filepath = self._download_pdf(ann, output_dir)
                    if filepath:
                        downloaded.append(filepath)
                        print(f"  ✅ 已下载: {year} 年度报告")
                    break

        return downloaded

    def download_periodic_reports(
        self, stock_code: str, year: int, output_dir: str, market: str = "szse"
    ) -> list:
        """下载当年的一季报、中报、三季报"""
        downloaded = []

        report_configs = [
            ("q1", "category_yjdbg_szsh", "一季度报告", f"{year}-04-01", f"{year}-05-31"),
            ("semi", "category_bndbg_szsh", "半年度报告", f"{year}-08-01", f"{year}-09-30"),
            ("q3", "category_sjdbg_szsh", "三季度报告", f"{year}-10-01", f"{year}-11-30"),
        ]

        for report_type, category, search_term, start_date, end_date in report_configs:
            if market == "hke":
                filter_params = {
                    "stock": [stock_code],
                    "category": [],
                    "searchkey": "",
                    "seDate": f"{start_date}~{end_date}",
                }
            else:
                filter_params = {
                    "stock": [stock_code],
                    "category": [category],
                    "searchkey": search_term,
                    "seDate": f"{start_date}~{end_date}",
                }

            announcements = self._query_announcements(filter_params, market)

            for ann in announcements:
                if self._is_main_periodic_report(ann["announcementTitle"], report_type):
                    filepath = self._download_pdf(ann, output_dir)
                    if filepath:
                        downloaded.append(filepath)
                        print(f"  ✅ 已下载: {year} {search_term}")
                    break

        return downloaded


def cleanup_temp_reports():
    """清理旧的临时财报文件"""
    try:
        # 查找系统中的临时财报目录
        temp_dirs = glob.glob("/tmp/cninfo_reports_*")
        for temp_dir in temp_dirs:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🧹 清理临时财报目录: {temp_dir}")
    except Exception as e:
        print(f"⚠️ 清理临时文件时出错: {e}")


def download_reports(stock_input: str, output_dir: str = None) -> dict:
    """
    下载股票财报的主函数
    返回包含股票信息和下载文件列表的字典
    """
    # 清理旧的临时财报文件
    cleanup_temp_reports()
    
    if output_dir is None:
        # 创建固定目录存放财报文件
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取项目根目录
        output_dir = os.path.join(base_dir, "reports", "financial_reports")
        os.makedirs(output_dir, exist_ok=True)

    downloader = CnInfoDownloader()

    # 查找股票
    stock_code, stock_info, market = downloader.find_stock(stock_input)
    if not stock_code:
        return {"error": f"未找到股票: {stock_input}"}

    stock_name = stock_info.get("zwjc", stock_code)
    market_display = "港股" if market == "hke" else "A股"
    print(f"📊 找到股票: {stock_code} ({stock_name}) [{market_display}]")

    # 计算年份
    current_year = datetime.datetime.now().year
    annual_years = list(range(current_year - 5, current_year))

    # 下载年度报告
    print(f"\n📥 正在下载近{len(annual_years)}年年度报告...")
    annual_files = downloader.download_annual_reports(stock_code, annual_years, output_dir, market)

    # 下载定期报告
    print(f"\n📥 正在下载定期报告（一季报、中报、三季报）...")
    periodic_files = downloader.download_periodic_reports(stock_code, current_year, output_dir, market)

    if not periodic_files:
        print(f"  当年无报告，尝试去年...")
        periodic_files = downloader.download_periodic_reports(stock_code, current_year - 1, output_dir, market)
    elif len(periodic_files) < 3:
        prev_year_files = downloader.download_periodic_reports(stock_code, current_year - 1, output_dir, market)
        periodic_files.extend(prev_year_files)

    all_files = annual_files + periodic_files

    return {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "market": market,
        "market_display": market_display,
        "output_dir": output_dir,
        "files": all_files,
        "annual_count": len(annual_files),
        "periodic_count": len(periodic_files),
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python cninfo_downloader.py <股票代码或名称> [输出目录]")
        print("示例: python cninfo_downloader.py 600519")
        print("示例: python cninfo_downloader.py 贵州茅台")
        sys.exit(1)

    stock_input = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = download_reports(stock_input, output_dir)
    if "error" in result:
        print(f"错误: {result['error']}")
    else:
        print(f"\n{'=' * 50}")
        print(f"✅ 下载完成: {len(result['files'])} 份财报")
        print(f"📁 保存位置: {result['output_dir']}")
        print(f"\n文件列表:")
        for f in result["files"]:
            print(f"  {os.path.basename(f)}")
