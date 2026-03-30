#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供股票分析相关的通用工具函数
"""

from datetime import datetime, timedelta


def format_number(num, decimal_places=2):
    """格式化数字"""
    if num is None:
        return "N/A"
    try:
        return f"{num:.{decimal_places}f}"
    except:
        return str(num)


def format_large_number(num):
    """格式化大数字（如成交量、成交额）"""
    if num is None:
        return "N/A"
    try:
        if num >= 1_0000_0000:
            return f"{num/1_0000_0000:.2f}亿"
        elif num >= 1_0000:
            return f"{num/1_0000:.2f}万"
        else:
            return f"{num:.0f}"
    except:
        return str(num)


def calculate_change_percent(current, previous):
    """计算涨跌幅百分比"""
    if previous == 0 or previous is None:
        return 0
    try:
        return ((current - previous) / abs(previous)) * 100
    except:
        return 0


def get_trading_days(start_date, end_date):
    """获取交易日数量（简单估算）"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        # 简单估算：假设每年250个交易日
        return int(delta.days * 0.7)  # 大约70%是工作日
    except:
        return 0


def is_market_open():
    """判断当前是否为交易时间（简单判断）"""
    now = datetime.now()
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    hour = now.hour
    minute = now.minute
    
    # 周一到周五
    if weekday < 5:
        # 上午交易时间: 9:30-11:30
        if hour == 9 and minute >= 30:
            return True
        elif 10 <= hour <= 11:
            return True
        # 下午交易时间: 13:00-15:00
        elif hour == 13 or hour == 14 or (hour == 15 and minute == 0):
            return True
    
    return False


def get_stock_type(symbol):
    """根据股票代码判断股票类型"""
    if isinstance(symbol, str):
        if symbol.startswith(('00', '30', '15', '16', '18')):
            return 'sz'  # 深圳证券交易所
        elif symbol.startswith('6'):
            return 'sh'  # 上海证券交易所
        elif symbol.startswith('8'):
            return 'bj'  # 北京证券交易所
    return 'unknown'


def normalize_symbol(symbol):
    """标准化股票代码"""
    if isinstance(symbol, str):
        # 如果已经有交易所标识，直接返回小写
        if '.' in symbol:
            return symbol.lower()
        
        # 根据代码长度和开头数字判断交易所
        if len(symbol) == 6:
            stock_type = get_stock_type(symbol)
            if stock_type != 'unknown':
                return f"{stock_type}.{symbol}"
    
    return symbol


def get_current_date():
    """获取当前日期字符串"""
    return datetime.now().strftime('%Y-%m-%d')


def get_date_range(days=30):
    """获取日期范围"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def get_stock_code_by_name(stock_name):
    """
    通过股票名称获取股票代码（使用东方财富接口）
    
    Args:
        stock_name: 股票名称（如"中国建筑"）
        
    Returns:
        dict: 包含代码和名称的字典，如 {'code': '601668', 'name': '中国建筑'}
              如果找不到返回 None
    """
    import requests
    
    try:
        # 东方财富股票搜索接口
        url = f"https://searchapi.eastmoney.com/api/suggest/get"
        params = {
            "input": stock_name,
            "type": "14",  # 股票类型
            "token": "D43BF72245F0E329CA1F8B6F80E520",
            "count": "5"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://data.eastmoney.com/"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 解析 JSONP 格式响应
            import re
            import json
            
            text = response.text
            # 匹配 JSON 数组
            match = re.search(r'jQuery.*?\((\[.*?\])\)', text)
            if match:
                arr = json.loads(match.group(1))
                for item in arr[:3]:
                    code = item.get('Code', '')
                    name = item.get('Name', '')
                    market_code = item.get('MktNum', '')  # 市场代码
                    
                    # 过滤掉非A股股票（如港股、美股）
                    if market_code in ['1', '2']:  # 1=沪市, 2=深市
                        # 去掉交易所前缀
                        if '.' in code:
                            code = code.split('.')[1]
                        return {'code': code, 'name': name, 'market': 'sh' if market_code == '1' else 'sz'}
        
        # 如果上面的接口失败，尝试另一个接口
        url2 = "https://push2.eastmoney.com/api/qt/clist/get"
        params2 = {
            "pn": "1",
            "pz": "10",
            "po": "1",
            "np": "1",
            "fields": "f12,f14",
            "fid": "f3",
            "fs": "b:MK0021,b:MK0022,b:MK0023,b:MK0024",  # A股市场
        }
        
        # 添加搜索条件
        params2["ut"] = "b1f7f7f7f7f7f7f7f7f7f7f7f7f7f7"
        
        response2 = requests.get(url2, params=params2, headers=headers, timeout=10)
        if response2.status_code == 200:
            data2 = response2.json()
            if 'data' in data2 and 'diff' in data2['data']:
                for item in data2['data']['diff']:
                    code = item.get('f12', '')
                    name = item.get('f14', '')
                    if stock_name.lower() in name.lower() or name.lower() in stock_name.lower():
                        return {'code': code, 'name': name}
        
        return None
        
    except Exception as e:
        print(f"股票代码搜索失败: {e}")
        return None