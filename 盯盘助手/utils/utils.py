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