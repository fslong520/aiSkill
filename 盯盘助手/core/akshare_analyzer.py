#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare 财务数据获取模块
提供完整的资产负债表、利润表、现金流量表数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


class AKShareFinancialAnalyzer:
    """基于 AKShare 的财务数据分析器"""
    
    def __init__(self):
        """初始化 AKShare 分析器"""
        self.current_date = datetime.now().strftime("%Y%m%d")
    
    def get_stock_code(self, stock_name_or_code):
        """
        获取股票代码（支持名称和代码输入）
        
        Args:
            stock_name_or_code: 股票名称或代码（如"重庆百货"或"600729"）
            
        Returns:
            str: 完整的股票代码（如"sh600729"）
        """
        try:
            # 如果输入是纯数字，假设是股票代码
            if stock_name_or_code.isdigit() and len(stock_name_or_code) == 6:
                if stock_name_or_code.startswith('6'):
                    return f"sh{stock_name_or_code}"
                else:
                    return f"sz{stock_name_or_code}"
            
            # 如果输入是名称，需要查询股票代码
            # 这里简化处理，直接返回格式化的代码
            if stock_name_or_code.startswith('sh') or stock_name_or_code.startswith('sz'):
                return stock_name_or_code
            
            # 其他情况默认加上 sh 前缀
            return f"sh{stock_name_or_code}"
            
        except Exception as e:
            print(f"获取股票代码失败：{e}")
            return None
    
    def get_balance_sheet(self, stock_code):
        """
        获取资产负债表数据
        
        Args:
            stock_code: 股票代码（如"sh600729"）
            
        Returns:
            DataFrame: 资产负债表数据
        """
        try:
            print(f"\n正在获取 {stock_code} 的资产负债表数据...")
            
            # 使用 AKShare 获取东方财富网的资产负债表数据
            df = ak.stock_financial_report_sina(stock=stock_code, symbol="资产负债表")
            
            if df is not None and len(df) > 0:
                print(f"✅ 成功获取资产负债表数据，共 {len(df)} 行")
                return df
            else:
                print("❌ 未获取到资产负债表数据")
                return None
                
        except Exception as e:
            print(f"获取资产负债表失败：{e}")
            return None
    
    def get_profit_statement(self, stock_code):
        """
        获取利润表数据
        
        Args:
            stock_code: 股票代码（如"sh600729"）
            
        Returns:
            DataFrame: 利润表数据
        """
        try:
            print(f"\n正在获取 {stock_code} 的利润表数据...")
            
            df = ak.stock_financial_report_sina(stock=stock_code, symbol="利润表")
            
            if df is not None and len(df) > 0:
                print(f"✅ 成功获取利润表数据，共 {len(df)} 行")
                return df
            else:
                print("❌ 未获取到利润表数据")
                return None
                
        except Exception as e:
            print(f"获取利润表失败：{e}")
            return None
    
    def get_cash_flow(self, stock_code):
        """
        获取现金流量表数据
        
        Args:
            stock_code: 股票代码（如"sh600729"）
            
        Returns:
            DataFrame: 现金流量表数据
        """
        try:
            print(f"\n正在获取 {stock_code} 的现金流量表数据...")
            
            df = ak.stock_financial_report_sina(stock=stock_code, symbol="现金流量表")
            
            if df is not None and len(df) > 0:
                print(f"✅ 成功获取现金流量表数据，共 {len(df)} 行")
                return df
            else:
                print("❌ 未获取到现金流量表数据")
                return None
                
        except Exception as e:
            print(f"获取现金流量表失败：{e}")
            return None
    
    def get_comprehensive_financial_report(self, stock_input):
        """
        获取综合财务报告（三大报表完整版）
        
        Args:
            stock_input: 股票输入（名称或代码）
            
        Returns:
            dict: 包含三大报表的字典
        """
        print(f"\n{'='*70}")
        print(f"📊 开始获取 {stock_input} 的完整财务数据（AKShare 版本）")
        print(f"{'='*70}\n")
        
        # 转换股票代码
        stock_code = self.get_stock_code(stock_input)
        if not stock_code:
            print(f"❌ 无法解析股票代码：{stock_input}")
            return None
        
        print(f"股票代码：{stock_code}\n")
        
        # 获取三大报表
        balance_sheet = self.get_balance_sheet(stock_code)
        profit_statement = self.get_profit_statement(stock_code)
        cash_flow = self.get_cash_flow(stock_code)
        
        # 检查是否至少有一个报表获取成功
        if all(v is None for v in [balance_sheet, profit_statement, cash_flow]):
            print("\n❌ 错误：所有报表获取失败")
            return None
        
        print(f"\n{'='*70}")
        print("✅ 财务报表获取完成")
        print(f"{'='*70}")
        
        return {
            'balance_sheet': balance_sheet,
            'profit_statement': profit_statement,
            'cash_flow': cash_flow,
            'stock_code': stock_code
        }
    
    def display_report_summary(self, report_data):
        """
        显示财报数据摘要
        
        Args:
            report_data: 综合财务报告数据
        """
        if not report_data:
            return
        
        print("\n【财报数据摘要】")
        
        # 资产负债表摘要
        if report_data.get('balance_sheet') is not None:
            df = report_data['balance_sheet']
            print(f"\n资产负债表列名（共{len(df.columns)}列）:")
            print(df.columns.tolist()[:20])  # 只显示前 20 个列名
        
        # 利润表摘要
        if report_data.get('profit_statement') is not None:
            df = report_data['profit_statement']
            print(f"\n利润表列名（共{len(df.columns)}列）:")
            print(df.columns.tolist()[:20])
        
        # 现金流量表摘要
        if report_data.get('cash_flow') is not None:
            df = report_data['cash_flow']
            print(f"\n现金流量表列名（共{len(df.columns)}列）:")
            print(df.columns.tolist()[:20])


def test_akshare_financial_data():
    """测试 AKShare 财务数据获取"""
    analyzer = AKShareFinancialAnalyzer()
    
    # 测试重庆百货
    result = analyzer.get_comprehensive_financial_report("600729")
    
    if result:
        analyzer.display_report_summary(result)
        
        # 显示具体数据示例
        if result['balance_sheet'] is not None:
            print("\n【资产负债表前 3 行数据示例】")
            print(result['balance_sheet'].head(3))
        
        if result['profit_statement'] is not None:
            print("\n【利润表前 3 行数据示例】")
            print(result['profit_statement'].head(3))
        
        if result['cash_flow'] is not None:
            print("\n【现金流量表前 3 行数据示例】")
            print(result['cash_flow'].head(3))


if __name__ == "__main__":
    test_akshare_financial_data()
