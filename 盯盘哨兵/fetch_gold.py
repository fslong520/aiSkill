#!/usr/bin/env python3
"""
黄金价格获取脚本
从东方财富网页获取沪金主连实时行情
"""

import json
import subprocess
import sys
from datetime import datetime

def get_gold_price_from_browser():
    """通过 Playwright 浏览器获取黄金价格"""
    try:
        # 使用 copaw 内置的 browser 工具
        # 这里我们返回一个提示，让 AI 知道需要用 browser_use 工具
        return {
            "method": "browser",
            "url": "http://quote.eastmoney.com/unify/r/113.aum",
            "instructions": "使用 browser_use 工具访问上述 URL，然后获取页面上的价格数据"
        }
    except Exception as e:
        return {"error": str(e)}

def get_gold_price_api():
    """尝试通过 API 获取黄金价格（备用方案）"""
    import requests
    
    try:
        # 东方财富期货行情 API
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
        params = {
            "fltt": 2,
            "invt": 2,
            "fields": "f1,f2,f3,f4,f5,f6,f7,f12,f14,f15,f16,f17,f18",
            "secids": "113.aum"  # 沪金主连
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://quote.eastmoney.com/"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("data") and data["data"].get("diff"):
            item = data["data"]["diff"][0]
            return {
                "name": item.get("f14", "沪金主连"),
                "code": item.get("f12", "aum"),
                "price": item.get("f2", 0),
                "change_pct": item.get("f3", 0),
                "change": item.get("f4", 0),
                "volume": item.get("f5", 0),
                "amount": item.get("f6", 0),
                "high": item.get("f15", 0),
                "low": item.get("f16", 0),
                "open": item.get("f17", 0),
                "prev_close": item.get("f18", 0),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {"error": "API 返回数据为空"}
            
    except Exception as e:
        return {"error": str(e)}

def format_report(data):
    """格式化简报"""
    if "error" in data:
        return f"❌ 获取数据失败: {data['error']}"
    
    return f"""📊 【{data['name']} {data['code']}】实时行情

💰 当前价格：{data['price']} 元/克
📈 涨跌幅：{data['change_pct']}% ({'+' if data['change'] > 0 else ''}{data['change']}元)
📅 今日区间：{data['low']} - {data['high']}
📊 成交量：{data['volume']}手
💵 成交额：{data['amount']}万

💡 简要分析：
【{'上涨' if data['change'] > 0 else '下跌'}】{'金价走强' if data['change'] > 0 else '金价走弱'}，{'涨幅明显' if abs(data['change_pct']) > 1 else '波动较小'}。

⏰ 查询时间：{data['time']}"""

if __name__ == "__main__":
    print("=== 黄金价格获取 ===\n")
    
    # 先尝试 API
    print("方法1: 尝试 API 获取...")
    result = get_gold_price_api()
    
    if "error" in result:
        print(f"API 失败: {result['error']}")
        print("\n方法2: 使用浏览器获取...")
        browser_result = get_gold_price_from_browser()
        print(f"请使用 browser_use 访问: {browser_result['url']}")
    else:
        print("API 获取成功!\n")
        print(format_report(result))
