#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务分析模块
负责处理股票的财务数据相关分析功能
"""

import baostock as bs
import pandas as pd
from datetime import datetime
import sys
import os
from pathlib import Path

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, str(Path(__file__).parent))

from utils.cache_manager import get_default_cache_manager
from utils import get_current_date


class FinancialAnalyzer:
    """财务数据分析器"""
    
    def __init__(self, cache_enabled=True, cache_ttl_hours=24):
        """初始化财务分析器"""
        self.current_date = get_current_date()
        self.cache_manager = get_default_cache_manager()
        # 如果需要特定配置，可以创建新的CacheManager实例
        if cache_enabled != self.cache_manager.cache_enabled or cache_ttl_hours != self.cache_manager.cache_ttl_hours:
            from utils.cache_manager import CacheManager
            self.cache_manager = CacheManager(cache_enabled, cache_ttl_hours)
    
    def _get_recent_quarters(self, max_quarters=8):
        """获取最近几个季度的年份和季度列表，用于处理财报发布时间延迟"""
        current_year = datetime.now().year
        current_quarter = (datetime.now().month - 1) // 3 + 1
        
        quarters = []
        for i in range(max_quarters):
            target_quarter = current_quarter - i
            target_year = current_year
            
            # 处理跨年情况
            while target_quarter <= 0:
                target_quarter += 4
                target_year -= 1
            
            quarters.append((target_year, target_quarter))
        
        return quarters
    
    def get_balance_sheet(self, symbol, year=None, quarter=None):
        """获取资产负债表数据"""
        try:
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                else:
                    code = f"sz.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    else:
                        code = f"sz.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 如果没有指定年份和季度，使用最新可用数据
            if year is None or quarter is None:
                # 尝试获取最近几个季度的数据，因为财报发布时间可能延迟
                current_year = datetime.now().year
                current_quarter = (datetime.now().month - 1) // 3 + 1
                
                # 按照时间倒序尝试，先查最近的，再查更早的
                quarters_to_try = []
                for i in range(5):  # 尝试最近5个季度的数据
                    q = current_quarter - i
                    y = current_year
                    while q <= 0:
                        q += 4
                        y -= 1
                    quarters_to_try.append((y, q))
            else:
                quarters_to_try = [(year, quarter)]
            
            for try_year, try_quarter in quarters_to_try:
                # 检查缓存
                cache_key = f"balance_sheet_{symbol}_{try_year}_{try_quarter}_{self.current_date}"
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    return cached_data
                
                # 查询资产负债表数据
                rs = bs.query_balance_data(code=code, year=str(try_year), quarter=str(try_quarter))
                
                balance_data = []
                if rs.error_code == '0':
                    while (rs.error_code == '0') & (rs.next()):
                        balance_data.append(rs.get_row_data())
                    
                    if len(balance_data) > 0:
                        # 转换为DataFrame
                        df = pd.DataFrame(balance_data, columns=rs.fields)
                                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
                    else:
                        print(f"警告: 未找到 {code} 在 {try_year} 年 {try_quarter} 季度的资产负债表数据，尝试下一季度...")
                else:
                    print(f"错误: 查询资产负债表失败，错误码: {rs.error_code}，尝试下一季度...")
            
            print(f"警告: 未找到 {code} 的资产负债表数据")
            return None
        except Exception as e:
            print(f"获取资产负债表失败: {e}")
            return None
    
    def get_cash_flow(self, symbol, year=None, quarter=None):
        """获取现金流量表数据"""
        try:
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                else:
                    code = f"sz.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    else:
                        code = f"sz.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 如果没有指定年份和季度，使用最新可用数据
            if year is None or quarter is None:
                # 尝试获取最近几个季度的数据，因为财报发布时间可能延迟
                current_year = datetime.now().year
                current_quarter = (datetime.now().month - 1) // 3 + 1
                
                # 按照时间倒序尝试，先查最近的，再查更早的
                quarters_to_try = []
                for i in range(5):  # 尝试最近5个季度的数据
                    q = current_quarter - i
                    y = current_year
                    while q <= 0:
                        q += 4
                        y -= 1
                    quarters_to_try.append((y, q))
            else:
                quarters_to_try = [(year, quarter)]
            
            for try_year, try_quarter in quarters_to_try:
                # 检查缓存
                cache_key = f"cash_flow_{symbol}_{try_year}_{try_quarter}_{self.current_date}"
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    return cached_data
                
                # 查询现金流量表数据
                rs = bs.query_cash_flow_data(code=code, year=str(try_year), quarter=str(try_quarter))
                
                cash_flow_data = []
                if rs.error_code == '0':
                    while (rs.error_code == '0') & (rs.next()):
                        cash_flow_data.append(rs.get_row_data())
                    
                    if len(cash_flow_data) > 0:
                        # 转换为DataFrame
                        df = pd.DataFrame(cash_flow_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
                    else:
                        print(f"警告: 未找到 {code} 在 {try_year} 年 {try_quarter} 季度的现金流量表数据，尝试下一季度...")
                else:
                    print(f"错误: 查询现金流量表失败，错误码: {rs.error_code}，尝试下一季度...")
            
            print(f"警告: 未找到 {code} 的现金流量表数据")
            return None
        except Exception as e:
            print(f"获取现金流量表失败: {e}")
            return None
    
    def get_profit_statement(self, symbol, year=None, quarter=None):
        """获取利润表数据"""
        try:
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                else:
                    code = f"sz.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    else:
                        code = f"sz.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 如果没有指定年份和季度，使用最新可用数据
            if year is None or quarter is None:
                # 尝试获取最近几个季度的数据，因为财报发布时间可能延迟
                current_year = datetime.now().year
                current_quarter = (datetime.now().month - 1) // 3 + 1
                
                # 按照时间倒序尝试，先查最近的，再查更早的
                quarters_to_try = []
                for i in range(5):  # 尝试最近5个季度的数据
                    q = current_quarter - i
                    y = current_year
                    while q <= 0:
                        q += 4
                        y -= 1
                    quarters_to_try.append((y, q))
            else:
                quarters_to_try = [(year, quarter)]
            
            for try_year, try_quarter in quarters_to_try:
                # 检查缓存
                cache_key = f"profit_statement_{symbol}_{try_year}_{try_quarter}_{self.current_date}"
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    return cached_data
                
                # 查询利润表数据
                rs = bs.query_profit_data(code=code, year=str(try_year), quarter=str(try_quarter))
                
                profit_data = []
                if rs.error_code == '0':
                    while (rs.error_code == '0') & (rs.next()):
                        profit_data.append(rs.get_row_data())
                    
                    if len(profit_data) > 0:
                        # 转换为DataFrame
                        df = pd.DataFrame(profit_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
                    else:
                        print(f"警告: 未找到 {code} 在 {try_year} 年 {try_quarter} 季度的利润表数据，尝试下一季度...")
                else:
                    print(f"错误: 查询利润表失败，错误码: {rs.error_code}，尝试下一季度...")
            
            print(f"警告: 未找到 {code} 的利润表数据")
            return None
        except Exception as e:
            print(f"获取利润表失败: {e}")
            return None
    
    def get_operation_analysis(self, symbol, year=None, quarter=None):
        """获取运营能力分析数据"""
        try:
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                else:
                    code = f"sz.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    else:
                        code = f"sz.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 如果没有指定年份和季度，使用最新可用数据
            if year is None or quarter is None:
                # 尝试获取最近几个季度的数据，因为财报发布时间可能延迟
                current_year = datetime.now().year
                current_quarter = (datetime.now().month - 1) // 3 + 1
                
                # 按照时间倒序尝试，先查最近的，再查更早的
                quarters_to_try = []
                for i in range(5):  # 尝试最近5个季度的数据
                    q = current_quarter - i
                    y = current_year
                    while q <= 0:
                        q += 4
                        y -= 1
                    quarters_to_try.append((y, q))
            else:
                quarters_to_try = [(year, quarter)]
            
            for try_year, try_quarter in quarters_to_try:
                # 检查缓存
                cache_key = f"operation_analysis_{symbol}_{try_year}_{try_quarter}_{self.current_date}"
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    return cached_data
                
                # 查询运营能力数据
                rs = bs.query_operation_data(code=code, year=str(try_year), quarter=str(try_quarter))
                
                operation_data = []
                if rs.error_code == '0':
                    while (rs.error_code == '0') & (rs.next()):
                        operation_data.append(rs.get_row_data())
                    
                    if len(operation_data) > 0:
                        # 转换为DataFrame
                        df = pd.DataFrame(operation_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
                    else:
                        print(f"警告: 未找到 {code} 在 {try_year} 年 {try_quarter} 季度的运营能力数据，尝试下一季度...")
                else:
                    print(f"错误: 查询运营能力数据失败，错误码: {rs.error_code}，尝试下一季度...")
            
            print(f"警告: 未找到 {code} 的运营能力数据")
            return None
        except Exception as e:
            print(f"获取运营能力分析失败: {e}")
            return None
    
    def get_growth_analysis(self, symbol, year=None, quarter=None):
        """获取成长能力分析数据"""
        try:
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                else:
                    code = f"sz.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    else:
                        code = f"sz.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 如果没有指定年份和季度，使用最新可用数据
            if year is None or quarter is None:
                # 尝试获取最近几个季度的数据，因为财报发布时间可能延迟
                current_year = datetime.now().year
                current_quarter = (datetime.now().month - 1) // 3 + 1
                
                # 按照时间倒序尝试，先查最近的，再查更早的
                quarters_to_try = []
                for i in range(5):  # 尝试最近5个季度的数据
                    q = current_quarter - i
                    y = current_year
                    while q <= 0:
                        q += 4
                        y -= 1
                    quarters_to_try.append((y, q))
            else:
                quarters_to_try = [(year, quarter)]
            
            for try_year, try_quarter in quarters_to_try:
                # 检查缓存
                cache_key = f"growth_analysis_{symbol}_{try_year}_{try_quarter}_{self.current_date}"
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    return cached_data
                
                # 查询成长能力数据
                rs = bs.query_growth_data(code=code, year=str(try_year), quarter=str(try_quarter))
                
                growth_data = []
                if rs.error_code == '0':
                    while (rs.error_code == '0') & (rs.next()):
                        growth_data.append(rs.get_row_data())
                    
                    if len(growth_data) > 0:
                        # 转换为DataFrame
                        df = pd.DataFrame(growth_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
                    else:
                        print(f"警告: 未找到 {code} 在 {try_year} 年 {try_quarter} 季度的成长能力数据，尝试下一季度...")
                else:
                    print(f"错误: 查询成长能力数据失败，错误码: {rs.error_code}，尝试下一季度...")
            
            print(f"警告: 未找到 {code} 的成长能力数据")
            return None
        except Exception as e:
            print(f"获取成长能力分析失败: {e}")
            return None
    
    def get_dupont_analysis(self, symbol, year=None, quarter=None):
        """获取杜邦分析数据"""
        try:
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                else:
                    code = f"sz.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    else:
                        code = f"sz.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 如果没有指定年份和季度，使用最新可用数据
            if year is None or quarter is None:
                # 尝试获取最近几个季度的数据，因为财报发布时间可能延迟
                current_year = datetime.now().year
                current_quarter = (datetime.now().month - 1) // 3 + 1
                
                # 按照时间倒序尝试，先查最近的，再查更早的
                quarters_to_try = []
                for i in range(5):  # 尝试最近5个季度的数据
                    q = current_quarter - i
                    y = current_year
                    while q <= 0:
                        q += 4
                        y -= 1
                    quarters_to_try.append((y, q))
            else:
                quarters_to_try = [(year, quarter)]
            
            for try_year, try_quarter in quarters_to_try:
                # 检查缓存
                cache_key = f"dupont_analysis_{symbol}_{try_year}_{try_quarter}_{self.current_date}"
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    return cached_data
                
                # 查询杜邦分析数据
                rs = bs.query_dupont_data(code=code, year=str(try_year), quarter=str(try_quarter))
                
                dupont_data = []
                if rs.error_code == '0':
                    while (rs.error_code == '0') & (rs.next()):
                        dupont_data.append(rs.get_row_data())
                    
                    if len(dupont_data) > 0:
                        # 转换为DataFrame
                        df = pd.DataFrame(dupont_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
                    else:
                        print(f"警告: 未找到 {code} 在 {try_year} 年 {try_quarter} 季度的杜邦分析数据，尝试下一季度...")
                else:
                    print(f"错误: 查询杜邦分析数据失败，错误码: {rs.error_code}，尝试下一季度...")
            
            print(f"警告: 未找到 {code} 的杜邦分析数据")
            return None
        except Exception as e:
            print(f"获取杜邦分析失败: {e}")
            return None
    
    def get_dividend_data(self, symbol, year=None):
        """获取分红数据"""
        try:
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                else:
                    code = f"sz.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    else:
                        code = f"sz.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 如果没有指定年份，尝试获取最近几年的分红数据
            if year is None:
                years_to_try = []
                current_year = datetime.now().year
                for i in range(5):  # 尝试最近5年的分红数据
                    years_to_try.append(current_year - i)
            else:
                years_to_try = [year]
            
            for try_year in years_to_try:
                # 检查缓存
                cache_key = f"dividend_data_{symbol}_{try_year}_{self.current_date}"
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    return cached_data
                
                # 查询分红数据
                rs = bs.query_dividend_data(code=code, year=str(try_year))
                
                dividend_data = []
                if rs.error_code == '0':
                    while (rs.error_code == '0') & (rs.next()):
                        dividend_data.append(rs.get_row_data())
                    
                    if len(dividend_data) > 0:
                        # 转换为DataFrame
                        df = pd.DataFrame(dividend_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
                    else:
                        print(f"警告: 未找到 {code} 在 {try_year} 年的分红数据，尝试下一年...")
                else:
                    print(f"错误: 查询 {try_year} 年分红数据失败，错误码: {rs.error_code}，尝试下一年...")
            
            print(f"警告: 未找到 {code} 的分红数据")
            return None
        except Exception as e:
            print(f"获取分红数据失败: {e}")
            return None


def get_default_financial_analyzer():
    """获取默认财务分析器"""
    return FinancialAnalyzer()