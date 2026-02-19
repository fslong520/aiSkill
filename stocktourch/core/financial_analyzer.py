#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务分析模块
负责处理股票的财务数据相关分析功能
支持两种数据源：
1. baostock - 提供财务比率和增长率数据
2. AKShare - 提供完整的财务报表绝对值数据
"""

import baostock as bs
import akshare as ak
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
                        print(f"找到 {code} 在 {try_year} 年 {try_quarter} 季度的资产负债表数据...")
                        df = pd.DataFrame(balance_data, columns=rs.fields)
                                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
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
                        print(f"找到 {code} 在 {try_year} 年 {try_quarter} 季度的现金流量表数据...")
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
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
                        print(f"找到 {code} 在 {try_year} 年 {try_quarter} 季度的利润表数据...")
                        df = pd.DataFrame(profit_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
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
                        print(f"找到 {code} 在 {try_year} 年 {try_quarter} 季度的运营能力数据...")
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df 
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
                        print(f"找到 {code} 在 {try_year} 年 {try_quarter} 季度的成长能力数据...")
                        df = pd.DataFrame(growth_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
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
                        print(f"找到 {code} 在 {try_year} 年 {try_quarter} 季度的杜邦分析数据...")
                        df = pd.DataFrame(dupont_data, columns=rs.fields)
                        
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df       
            return None
        except Exception as e:
            print(f"获取杜邦分析失败: {e}")
            return None
    
    def get_dividend_data(self, symbol, year=None):
        """获取分红数据"""
        try:
            # 格式化股票代码为 baostock 格式
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
                for i in range(5):  # 尝试最近 5 年的分红数据
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
                        # 转换为 DataFrame
                        print(f"找到 {code} 在 {try_year} 年的分红数据...")
                        df = pd.DataFrame(dividend_data, columns=rs.fields)
                            
                        # 缓存数据
                        self.cache_manager.set_cached_data(cache_key, df)
                        return df
            return None
        except Exception as e:
            print(f"获取分红数据失败：{e}")
            return None
    
    def get_akshare_financial_report(self, stock_input):
        """
        使用 AKShare 获取完整的财务报表数据（绝对值）
        
        Args:
            stock_input: 股票输入（名称或代码）
            
        Returns:
            dict: 包含三大报表的字典
        """
        print(f"\n📊 使用 AKShare 获取 {stock_input} 的完整财务数据...")
        
        try:
            # 格式化股票代码
            if stock_input.isdigit() and len(stock_input) == 6:
                if stock_input.startswith('6'):
                    stock_code = f"sh{stock_input}"
                else:
                    stock_code = f"sz{stock_input}"
            else:
                if stock_input.startswith('sh') or stock_input.startswith('sz'):
                    stock_code = stock_input
                else:
                    stock_code = f"sh{stock_input}"
            
            # 获取三大报表
            print(f"\n正在获取资产负债表...")
            balance_sheet = ak.stock_financial_report_sina(stock=stock_code, symbol="资产负债表")
            
            print(f"正在获取利润表...")
            profit_statement = ak.stock_financial_report_sina(stock=stock_code, symbol="利润表")
            
            print(f"正在获取现金流量表...")
            cash_flow = ak.stock_financial_report_sina(stock=stock_code, symbol="现金流量表")
            
            # 检查是否成功
            if all(v is None for v in [balance_sheet, profit_statement, cash_flow]):
                print("❌ AKShare 所有报表获取失败")
                return None
            
            print(f"✅ AKShare 财报获取成功")
            print(f"   资产负债表：{len(balance_sheet)}行 x {len(balance_sheet.columns)}列")
            print(f"   利润表：{len(profit_statement)}行 x {len(profit_statement.columns)}列")
            print(f"   现金流量表：{len(cash_flow)}行 x {len(cash_flow.columns)}列")
            
            return {
                'balance_sheet': balance_sheet,
                'profit_statement': profit_statement,
                'cash_flow': cash_flow,
                'stock_code': stock_code
            }
            
        except Exception as e:
            print(f"AKShare 获取财报失败：{e}")
            import traceback
            traceback.print_exc()
            return None
        
    def get_comprehensive_financial_report(self, symbol, year=None, quarter=None, use_akshare=True):
        """
        获取综合财务报告数据包（用于替代 PDF 财报分析）
        包含《读财报.md》方法论所需的所有关键数据
        
        Args:
            symbol: 股票代码或名称
            year: 年份（可选）
            quarter: 季度（可选）
            use_akshare: 是否使用 AKShare 获取完整财报数据（默认 True）
            
        Returns:
            dict: 包含三大报表、关键指标和分析数据的字典
        """
        print(f"\n📊 开始获取 {symbol} 的综合财务数据...")
        
        # 优先使用 AKShare 获取完整财报数据
        akshare_data = None
        if use_akshare:
            akshare_data = self.get_akshare_financial_report(symbol)
        
        # 使用 baostock 获取比率和增长率数据
        print(f"\n📊 使用 baostock 获取财务比率和增长率数据...")
        bs.login()
        
        balance_sheet_bs = self.get_balance_sheet(symbol, year, quarter)
        cash_flow_bs = self.get_cash_flow(symbol, year, quarter)
        profit_statement_bs = self.get_profit_statement(symbol, year, quarter)
        operation_data = self.get_operation_analysis(symbol, year, quarter)
        growth_data = self.get_growth_analysis(symbol, year, quarter)
        dupont_data = self.get_dupont_analysis(symbol, year, quarter)
        bs.logout()
        
        # 提取关键指标
        key_metrics = self._extract_key_metrics(
            balance_sheet_bs, cash_flow_bs, profit_statement_bs,
            operation_data, growth_data, dupont_data
        )
        
        # 如果 AKShare 获取成功，补充绝对值数据
        if akshare_data:
            key_metrics = self._merge_akshare_data(key_metrics, akshare_data)
        
        return {
            'balance_sheet': balance_sheet_bs,
            'cash_flow': cash_flow_bs,
            'profit_statement': profit_statement_bs,
            'operation_data': operation_data,
            'growth_data': growth_data,
            'dupont_data': dupont_data,
            'key_metrics': key_metrics,
            'akshare_data': akshare_data  # 保存原始 AKShare 数据
        }
    
    def _merge_akshare_data(self, metrics, akshare_data):
        """
        将 AKShare 的绝对值数据合并到指标字典中
        
        Args:
            metrics: baostock 提取的指标字典
            akshare_data: AKShare 获取的原始财报数据
            
        Returns:
            dict: 合并后的指标字典
        """
        try:
            # 从 AKShare 资产负债表提取
            if akshare_data.get('balance_sheet') is not None:
                df = akshare_data['balance_sheet']
                if len(df) > 0:
                    latest = df.iloc[0]  # 最新一期
                    
                    # 提取关键科目（单位：元）
                    metrics['总资产'] = float(latest.get('资产总计', 0) or 0)
                    metrics['总负债'] = float(latest.get('负债合计', 0) or 0)
                    metrics['货币资金'] = float(latest.get('货币资金', 0) or 0)
                    metrics['应收账款'] = float(latest.get('应收账款', 0) or 0)
                    metrics['应收票据'] = float(latest.get('应收票据', 0) or 0)
                    metrics['存货'] = float(latest.get('存货', 0) or 0)
                    metrics['固定资产'] = float(latest.get('固定资产', 0) or 0)
                    metrics['在建工程'] = float(latest.get('在建工程', 0) or 0)
                    metrics['无形资产'] = float(latest.get('无形资产', 0) or 0)
                    metrics['商誉'] = float(latest.get('商誉', 0) or 0)
                    metrics['短期借款'] = float(latest.get('短期借款', 0) or 0)
                    metrics['长期借款'] = float(latest.get('长期借款', 0) or 0)
                    metrics['应付账款'] = float(latest.get('应付账款', 0) or 0)
                    metrics['预收款项'] = float(latest.get('预收款项', 0) or 0)
                    
                    # 计算有息负债
                    metrics['有息负债'] = (
                        (metrics.get('短期借款') or 0) +
                        (metrics.get('长期借款') or 0)
                    )
                    
                    # 计算生产资产占比
                    production_assets = sum([
                        metrics.get('固定资产', 0) or 0,
                        metrics.get('在建工程', 0) or 0,
                        metrics.get('无形资产', 0) or 0
                    ])
                    if metrics.get('总资产') and metrics['总资产'] > 0:
                        metrics['生产资产占比'] = round(production_assets / metrics['总资产'] * 100, 2)
                    
                    # 计算应收款项占比
                    receivables = sum([
                        metrics.get('应收账款', 0) or 0,
                        metrics.get('应收票据', 0) or 0
                    ])
                    if metrics.get('总资产') and metrics['总资产'] > 0:
                        metrics['应收款项占比'] = round(receivables / metrics['总资产'] * 100, 2)
                    
                    # 资金充裕度判断
                    if metrics.get('货币资金') and metrics.get('有息负债'):
                        metrics['资金充裕度'] = (
                            '充裕' if metrics['货币资金'] >= metrics['有息负债'] else '紧张'
                        )
            
            # 从 AKShare 利润表提取
            if akshare_data.get('profit_statement') is not None:
                df = akshare_data['profit_statement']
                if len(df) > 0:
                    latest = df.iloc[0]
                    
                    metrics['营业收入'] = float(latest.get('营业收入', 0) or 0)
                    metrics['营业成本'] = float(latest.get('营业成本', 0) or 0)
                    metrics['销售费用'] = float(latest.get('销售费用', 0) or 0)
                    metrics['管理费用'] = float(latest.get('管理费用', 0) or 0)
                    metrics['财务费用'] = float(latest.get('财务费用', 0) or 0)
                    metrics['研发费用'] = float(latest.get('研发费用', 0) or 0)
                    metrics['营业利润'] = float(latest.get('营业利润', 0) or 0)
                    metrics['净利润'] = float(latest.get('归属于母公司所有者的净利润', 0) or metrics.get('净利润', 0) or 0)
                    metrics['扣非净利润'] = float(latest.get('扣除非经常性损益后的净利润', 0) or 0)
                    metrics['营业外收入'] = float(latest.get('营业外收入', 0) or 0)
                    
                    # 计算毛利润和毛利率
                    if metrics.get('营业收入') and metrics.get('营业成本'):
                        metrics['毛利润'] = metrics['营业收入'] - metrics['营业成本']
                        if metrics['营业收入'] > 0:
                            metrics['毛利率'] = round(metrics['毛利润'] / metrics['营业收入'] * 100, 2)
                    
                    # 期间费用率
                    total_expenses = sum([
                        metrics.get('销售费用', 0) or 0,
                        metrics.get('管理费用', 0) or 0,
                        metrics.get('财务费用', 0) or 0
                    ])
                    if metrics.get('营业收入') and metrics['营业收入'] > 0:
                        metrics['期间费用率'] = round(total_expenses / metrics['营业收入'] * 100, 2)
                    
                    # 营业外收入占比
                    if metrics.get('营业利润') and metrics['营业利润'] > 0:
                        metrics['营业外收入占比'] = round(metrics['营业外收入'] / metrics['营业利润'] * 100, 2)
            
            # 从 AKShare 现金流量表提取
            if akshare_data.get('cash_flow') is not None:
                df = akshare_data['cash_flow']
                if len(df) > 0:
                    latest = df.iloc[0]
                    
                    metrics['经营现金流净额'] = float(latest.get('经营活动产生的现金流量净额', 0) or 0)
                    metrics['投资现金流净额'] = float(latest.get('投资活动产生的现金流量净额', 0) or 0)
                    metrics['筹资现金流净额'] = float(latest.get('筹资活动产生的现金流量净额', 0) or 0)
                    metrics['销售商品收到的现金'] = float(latest.get('销售商品、提供劳务收到的现金', 0) or 0)
                    
                    # 净利润含金量
                    if metrics.get('净利润') and metrics['净利润'] > 0:
                        metrics['净利润现金含量'] = round(
                            metrics['经营现金流净额'] / metrics['净利润'] * 100, 2
                        )
                    
                    # 现金流肖像判断（使用绝对值）
                    metrics['现金流肖像'] = self._judge_cash_flow_pattern(
                        metrics.get('经营现金流净额', 0),
                        metrics.get('投资现金流净额', 0),
                        metrics.get('筹资现金流净额', 0)
                    )
            
            # 重新执行五大黄金标准和快速排雷检查（现在有完整数据了）
            metrics['五大黄金标准'] = self._check_golden_standards(metrics)
            metrics['快速排雷清单'] = self._quick_risk_check(metrics)
            
            print(f"\n✅ AKShare 数据已合并到指标中")
            
        except Exception as e:
            print(f"⚠️ 合并 AKShare 数据时出错：{e}")
            import traceback
            traceback.print_exc()
        
        return metrics
        
    def _extract_key_metrics(self, balance_sheet, cash_flow, profit_statement,
                            operation_data, growth_data, dupont_data):
        """
        从三大报表中提取《读财报.md》所需的关键指标
        注意：baostock 返回的是财务比率和增长率，不是完整的科目金额
            
        Returns:
            dict: 关键财务指标字典
        """
        metrics = {}
            
        try:
            # ========== 资产负债表指标（比率类）==========
            if balance_sheet is not None and len(balance_sheet) > 0:
                df = balance_sheet
                # 使用最后一行数据（最新季度）
                latest = df.iloc[-1] if len(df) > 0 else None
                    
                if latest is not None:
                    # 偿债能力比率
                    metrics['流动比率'] = self._get_column_value(latest, 'currentRatio')
                    metrics['速动比率'] = self._get_column_value(latest, 'quickRatio')
                    metrics['现金比率'] = self._get_column_value(latest, 'cashRatio')
                    metrics['资产负债率'] = self._get_column_value(latest, 'liabilityToAsset')
                    if metrics['资产负债率']:
                        metrics['资产负债率'] = round(metrics['资产负债率'] * 100, 2)
                    
                    # 负债同比增长率
                    metrics['负债同比增长率'] = self._get_column_value(latest, 'YOYLiability')
                    # 资产乘数
                    metrics['权益乘数'] = self._get_column_value(latest, 'assetToEquity')
                
            # ========== 利润表指标 ==========
            if profit_statement is not None and len(profit_statement) > 0:
                df = profit_statement
                latest = df.iloc[-1] if len(df) > 0 else None
                    
                if latest is not None:
                    # 盈利能力
                    metrics['ROE'] = self._get_column_value(latest, 'roeAvg')
                    if metrics['ROE']:
                        metrics['ROE'] = round(metrics['ROE'] * 100, 2)
                    
                    metrics['销售净利率'] = self._get_column_value(latest, 'npMargin')
                    if metrics['销售净利率']:
                        metrics['销售净利率'] = round(metrics['销售净利率'] * 100, 2)
                    
                    metrics['销售毛利率'] = self._get_column_value(latest, 'gpMargin')
                    if metrics['销售毛利率']:
                        metrics['销售毛利率'] = round(metrics['销售毛利率'] * 100, 2)
                    
                    # 净利润（绝对值）
                    metrics['净利润'] = self._get_column_value(latest, 'netProfit')
                    
                    # 每股收益
                    metrics['EPS_TTM'] = self._get_column_value(latest, 'epsTTM')
                    
                    # 总股本
                    metrics['总股本'] = self._get_column_value(latest, 'totalShare')
                    
                    # 营业收入（通过利润率和净利润反推）
                    if metrics.get('净利润') and metrics.get('销售净利率'):
                        metrics['营业收入'] = metrics['净利润'] / (metrics['销售净利率'] / 100)
                
            # ========== 现金流量表指标（比率类）==========
            if cash_flow is not None and len(cash_flow) > 0:
                df = cash_flow
                latest = df.iloc[-1] if len(df) > 0 else None
                    
                if latest is not None:
                    # 现金流相关比率
                    metrics['经营现金流占比营收'] = self._get_column_value(latest, 'CFOToOR')
                    metrics['经营现金流占净利润'] = self._get_column_value(latest, 'CFOToNP')
                    
                    # 推断现金流肖像（基于比率）
                    if metrics.get('经营现金流占净利润'):
                        # 如果经营现金流占净利润为正，说明经营现金流为正
                        if metrics['经营现金流占净利润'] > 0:
                            metrics['经营现金流状态'] = '正'
                        else:
                            metrics['经营现金流状态'] = '负'
                
            # ========== 运营能力指标 ==========
            if operation_data is not None and len(operation_data) > 0:
                df = operation_data
                latest = df.iloc[-1] if len(df) > 0 else None
                    
                if latest is not None:
                    # 周转率指标
                    metrics['应收账款周转率'] = self._get_column_value(latest, 'NRTurnRatio')
                    metrics['应收账款周转天数'] = self._get_column_value(latest, 'NRTurnDays')
                    metrics['存货周转率'] = self._get_column_value(latest, 'INVTurnRatio')
                    metrics['存货周转天数'] = self._get_column_value(latest, 'INVTurnDays')
                    metrics['流动资产周转率'] = self._get_column_value(latest, 'CATurnRatio')
                    metrics['总资产周转率'] = self._get_column_value(latest, 'AssetTurnRatio')
                
            # ========== 成长能力指标 ==========
            if growth_data is not None and len(growth_data) > 0:
                df = growth_data
                latest = df.iloc[-1] if len(df) > 0 else None
                    
                if latest is not None:
                    # 增长率指标
                    metrics['净资产同比增长率'] = self._get_column_value(latest, 'YOYEquity')
                    metrics['总资产同比增长率'] = self._get_column_value(latest, 'YOYAsset')
                    metrics['净利润同比增长率'] = self._get_column_value(latest, 'YOYNI')
                    metrics['基本 EPS 同比增长率'] = self._get_column_value(latest, 'YOYEPSBasic')
                    metrics['归母净利润同比增长率'] = self._get_column_value(latest, 'YOYPNI')
                    
                    # 统一使用归母净利润同比增长率作为净利润增长率
                    if metrics.get('归母净利润同比增长率'):
                        metrics['净利润增长率'] = metrics['归母净利润同比增长率']
                    elif metrics.get('净利润同比增长率'):
                        metrics['净利润增长率'] = metrics['净利润同比增长率']
                    
                    # 营收增长率（如果有 MBRevenue 数据）
                    metrics['营收增长率'] = self._get_column_value(latest, 'MBRevenue')
                
            # ========== 杜邦分析指标 ==========
            if dupont_data is not None and len(dupont_data) > 0:
                df = dupont_data
                latest = df.iloc[-1] if len(df) > 0 else None
                    
                if latest is not None:
                    # ROE（再次确认）
                    roe_dupont = self._get_column_value(latest, 'dupontROE')
                    if roe_dupont:
                        metrics['ROE_杜邦'] = round(roe_dupont * 100, 2)
                    
                    # 杜邦分解三因子
                    metrics['销售净利率_杜邦'] = self._get_column_value(latest, 'dupontPnitoni')
                    metrics['总资产周转率_杜邦'] = self._get_column_value(latest, 'dupontAssetTurn')
                    metrics['权益乘数_杜邦'] = self._get_column_value(latest, 'dupontAssetStoEquity')
                    
                    # 其他杜邦指标
                    metrics['税收负担'] = self._get_column_value(latest, 'dupontTaxBurden')
                    metrics['利息负担'] = self._get_column_value(latest, 'dupontIntburden')
                    metrics['息税前利润占营收'] = self._get_column_value(latest, 'dupontEbittogr')
                
            # ========== 现金流肖像判断（基于可用数据推断）==========
            # 由于 baostock 不返回现金流绝对值，只能基于比率推断
            metrics['现金流肖像'] = self._judge_cash_flow_pattern_baostock(
                metrics.get('经营现金流占净利润'),
                metrics.get('总资产同比增长率'),
                metrics.get('负债同比增长率')
            )
                
            # ========== 五大黄金标准检验（简化版）==========
            metrics['五大黄金标准'] = self._check_golden_standards_baostock(metrics)
                
            # ========== 快速排雷清单（简化版）==========
            metrics['快速排雷清单'] = self._quick_risk_check_baostock(metrics)
                
        except Exception as e:
            print(f"提取关键指标时出错：{e}")
            import traceback
            traceback.print_exc()
            
        return metrics
        
    def _get_column_value(self, row, column_name):
        """安全获取列值，处理不同的列名情况"""
        try:
            if column_name in row.index:
                value = row[column_name]
                if pd.isna(value):
                    return None
                return float(value)
            return None
        except:
            return None
        
    def _judge_cash_flow_pattern(self, operating, investing, financing):
        """判断现金流肖像类型（基于绝对值）"""
        if operating is None or investing is None or financing is None:
            return '未知'
            
        # 转为正负号
        op_sign = '+' if operating > 0 else '-'
        in_sign = '+' if investing > 0 else '-'
        fi_sign = '+' if financing > 0 else '-'
            
        patterns = {
            ('+', '-', '-'): '🐄 奶牛型（最优）',
            ('+', '+', '-'): '🐔 老母鸡型（成熟）',
            ('+', '-', '+'): '🐂 蛮牛型（有风险）',
            ('+', '+', '+'): '👻 妖精型（警惕）',
            ('-', '+', '+'): '🩸 失血型（危险）',
            ('-', '-', '+'): '🎰 赌徒型（高风险）',
            ('-', '+', '-'): '⬇️ 衰退型（末路）',
            ('-', '-', '-'): '💀 濒死型（崩溃）'
        }
            
        return patterns.get((op_sign, in_sign, fi_sign), '未知型')
    
    def _judge_cash_flow_pattern_baostock(self, cfo_to_np, asset_growth, liability_growth):
        """基于 baostock 的比率数据推断现金流肖像"""
        if cfo_to_np is None:
            return '未知'
        
        # 经营现金流状态判断
        op_sign = '+' if cfo_to_np > 0 else '-'
        
        # 资产增长判断投资活动
        if asset_growth:
            in_sign = '-' if asset_growth > 0 else '+'  # 资产增长说明有投资支出
        else:
            in_sign = '?'
        
        # 负债增长判断筹资活动
        if liability_growth:
            fi_sign = '+' if liability_growth > 0 else '-'  # 负债增长说明有筹资流入
        else:
            fi_sign = '?'
        
        # 简化判断
        if op_sign == '+':
            if in_sign == '-' and fi_sign == '-':
                return '🐄 奶牛型（推断）'
            elif in_sign == '+' and fi_sign == '-':
                return '🐔 老母鸡型（推断）'
            elif in_sign == '-' and fi_sign == '+':
                return '🐂 蛮牛型（推断）'
            else:
                return '👻 妖精型（推断）'
        else:
            return '🩸 失血型（推断）'
        
    def _check_golden_standards(self, metrics):
        """检查五大黄金标准（完整版，需要绝对值数据）"""
        standards = {
            '标准 1_经营现金流净额>净利润': False,
            '标准 2_销售商品收到现金≥营业收入': False,
            '标准 3_投资现金流净额<0': False,
            '标准 4_现金及等价物增加>0': False,
            '标准 5_期末现金余额≥有息负债': False
        }
            
        # 标准 1: 经营现金流净额 > 净利润
        if (metrics.get('经营现金流净额', 0) and metrics.get('净利润', 0) and
                metrics['经营现金流净额'] > metrics['净利润'] > 0):
            standards['标准 1_经营现金流净额>净利润'] = True
            
        # 标准 2: 销售商品收到的现金 ≥ 营业收入
        if (metrics.get('销售商品收到的现金', 0) and metrics.get('营业收入', 0) and
                metrics['销售商品收到的现金'] >= metrics['营业收入']):
            standards['标准 2_销售商品收到现金≥营业收入'] = True
            
        # 标准 3: 投资现金流净额 < 0
        if metrics.get('投资现金流净额', 0) and metrics['投资现金流净额'] < 0:
            standards['标准 3_投资现金流净额<0'] = True
            
        # 标准 4: 现金及等价物净增加额 > 0
        total_change = sum([
            metrics.get('经营现金流净额', 0) or 0,
            metrics.get('投资现金流净额', 0) or 0,
            metrics.get('筹资现金流净额', 0) or 0
        ])
        if total_change > 0:
            standards['标准 4_现金及等价物增加>0'] = True
            
        # 标准 5: 期末现金余额 ≥ 有息负债
        if (metrics.get('货币资金', 0) and metrics.get('有息负债', 0) and
                metrics['货币资金'] >= metrics['有息负债']):
            standards['标准 5_期末现金余额≥有息负债'] = True
            
        passed = sum(standards.values())
        standards['通过数量'] = f"{passed}/5"
        standards['评价'] = '优秀' if passed >= 4 else '良好' if passed >= 3 else '一般' if passed >= 2 else '较差'
            
        return standards
    
    def _check_golden_standards_baostock(self, metrics):
        """检查五大黄金标准（baostock 简化版，基于比率数据）"""
        standards = {
            '标准 1_经营现金流>净利润': False,
            '标准 2_盈利质量': False,
            '标准 3_扩张意愿': False,
            '标准 4_财务安全': False,
            '标准 5_成长健康': False
        }
        
        # 标准 1: 经营现金流占净利润 > 100%（净利润含金量）
        if metrics.get('经营现金流占净利润', 0) and metrics['经营现金流占净利润'] > 1:
            standards['标准 1_经营现金流>净利润'] = True
        
        # 标准 2: 经营现金流占营收 > 0（有真实现金流）
        if metrics.get('经营现金流占比营收', 0) and metrics['经营现金流占比营收'] > 0:
            standards['标准 2_盈利质量'] = True
        
        # 标准 3: 总资产同比增长（有扩张意愿）
        if metrics.get('总资产同比增长率', 0) and metrics['总资产同比增长率'] > 0:
            standards['标准 3_扩张意愿'] = True
        
        # 标准 4: 资产负债率 < 70%（财务安全）
        if metrics.get('资产负债率', 0) and metrics['资产负债率'] < 70:
            standards['标准 4_财务安全'] = True
        
        # 标准 5: 净利润同比增长 > 0（成长健康）
        if metrics.get('净利润增长率', 0) and metrics['净利润增长率'] > 0:
            standards['标准 5_成长健康'] = True
            
        passed = sum(standards.values())
        standards['通过数量'] = f"{passed}/5"
        standards['评价'] = '优秀' if passed >= 4 else '良好' if passed >= 3 else '一般' if passed >= 2 else '较差'
            
        return standards
        
    def _quick_risk_check(self, metrics):
        """快速排雷清单（8 项）（完整版）"""
        checklist = {
            '审计意见': '未知（需从其他来源获取）',
            '经营现金流连续 3 年为正': '需多年数据',
            '商誉/净资产<30%': '需计算',
            '无存贷双高': True,
            '应收增速<营收增速×2': '需多年数据',
            '资产负债率<70%': True,
            '非农林牧渔行业': '需行业数据',
            '未更换会计师事务所': '未知'
        }
            
        # 检查资产负债率
        if metrics.get('资产负债率'):
            if metrics['资产负债率'] >= 70:
                checklist['资产负债率<70%'] = False
                checklist['风险提示'] = '⚠️ 资产负债率超过 70%，需警惕'
            else:
                checklist['资产负债率<70%'] = True
            
        # 检查存贷双高
        if (metrics.get('货币资金', 0) and metrics.get('有息负债', 0)):
            if metrics['货币资金'] > 100 and metrics['有息负债'] > 100:
                ratio = metrics['货币资金'] / max(metrics['有息负债'], 1)
                if 0.5 < ratio < 2:
                    checklist['无存贷双高'] = False
                    checklist['风险提示'] = '⚠️ 疑似存贷双高，高度警惕'
            
        # 检查商誉风险
        if metrics.get('商誉') and metrics.get('总资产'):
            goodwill_ratio = metrics['商誉'] / metrics['总资产']
            if goodwill_ratio > 0.3:
                checklist['商誉/净资产<30%'] = False
                checklist['风险提示'] = '⚠️ 商誉占比过高，有减值风险'
            
        passed = sum(1 for v in checklist.values() if v is True)
        checklist['通过数量'] = f"{passed}/8"
        checklist['结论'] = '继续分析' if passed >= 6 else '谨慎关注' if passed >= 4 else '建议排除'
            
        return checklist
    
    def _quick_risk_check_baostock(self, metrics):
        """快速排雷清单（baostock 简化版，8 项）"""
        checklist = {
            'ROE>6%': False,
            '资产负债率<70%': False,
            '净利润增长>0': False,
            '经营现金流为正': False,
            '毛利率稳定': False,
            '应收账款周转正常': False,
            '存货周转正常': False,
            '非 ST 股票': '需额外数据'
        }
        
        # 检查 ROE
        if metrics.get('ROE', 0) and metrics['ROE'] > 6:
            checklist['ROE>6%'] = True
        
        # 检查资产负债率
        if metrics.get('资产负债率', 0) and metrics['资产负债率'] < 70:
            checklist['资产负债率<70%'] = True
        elif not metrics.get('资产负债率'):
            checklist['资产负债率<70%'] = True  # 如果没数据，默认通过
        
        # 检查净利润增长
        if metrics.get('净利润增长率', 0) and metrics['净利润增长率'] > 0:
            checklist['净利润增长>0'] = True
        
        # 检查经营现金流
        if metrics.get('经营现金流占净利润', 0) and metrics['经营现金流占净利润'] > 0:
            checklist['经营现金流为正'] = True
        
        # 检查毛利率
        if metrics.get('销售毛利率', 0) and metrics['销售毛利率'] > 20:
            checklist['毛利率稳定'] = True
        
        # 检查应收账款周转
        if metrics.get('应收账款周转率', 0) and metrics['应收账款周转率'] > 2:
            checklist['应收账款周转正常'] = True
        
        # 检查存货周转
        if metrics.get('存货周转率', 0) and metrics['存货周转率'] > 1:
            checklist['存货周转正常'] = True
            
        passed = sum(1 for v in checklist.values() if v is True)
        checklist['通过数量'] = f"{passed}/8"
        checklist['结论'] = '优质' if passed >= 6 else '良好' if passed >= 5 else '关注' if passed >= 4 else '谨慎'
            
        return checklist


def get_default_financial_analyzer():
    """获取默认财务分析器"""
    return FinancialAnalyzer()