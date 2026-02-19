#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票研究技能运行脚本 - 更新版本
使用 AKShare 财务数据获取完整财务报表
"""

import argparse
import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from executor.skill_executor import execute_skill
from core.stock_analyzer import StockAnalyzer


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="Stock Research Skill - 股票研究技能")
    
    parser.add_argument('args', nargs='*', help='命令参数（股票代码、选项等）')
    parser.add_argument('--no-cache', action='store_true', help='禁用智能缓存')
    parser.add_argument('--cache-ttl', type=int, default=24, help='缓存生存时间（小时，默认：24）')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'csv'], default='text', help='输出格式（默认：text）')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细日志输出')
    parser.add_argument('--show-config', action='store_true', help='显示当前配置')

    args = parser.parse_args()
    
    if args.show_config:
        from utils.config import print_config_summary
        print_config_summary()
        return

    if not args.args:
        print("股票研究技能使用说明:")
        print("用法：python3 run_skill.py [股票代码或命令] [选项] [参数...]")
        print("")
        print("基本命令:")
        print("  python3 run_skill.py 000001                    # 分析平安银行")
        print("  python3 run_skill.py 000001 finance            # 获取财务数据并 AI 分析")
        print("  python3 run_skill.py 000001 technical          # 技术分析")
        print("")
        print("高级命令:")
        print("  python3 run_skill.py hs300                     # 沪深 300 成分股")
        print("  python3 run_skill.py market report             # 大盘分析报告")
        print("")
        return

    # 创建分析器实例
    cache_enabled = not args.no_cache
    analyzer = StockAnalyzer(cache_enabled=cache_enabled, cache_ttl_hours=args.cache_ttl)

    # 处理财务分析命令
    if len(args.args) >= 2 and args.args[1].lower() in ["finance", "财务"]:
        stock_input = args.args[0]
        print(f"\n{'='*60}")
        print(f"📊 开始获取股票财务数据：{stock_input}")
        print(f"{'='*60}\n")
        
        from core.financial_analyzer import FinancialAnalyzer
        financial_analyzer = FinancialAnalyzer()
        report_data = financial_analyzer.get_comprehensive_financial_report(stock_input)
        
        if not report_data:
            print(f"❌ 错误：财报数据获取失败")
            return
        
        key_metrics = report_data.get('key_metrics', {})
        print(f"✅ 成功获取 {stock_input} 的财务数据（数据来源：AKShare）")
        print("\n💡 完整分析请使用：analyze_stock_with_financial_report 函数")
        return
    
    # 简单股票代码 - 执行完整分析
    if len(args.args) == 1 and args.args[0].isdigit() and len(args.args[0]) == 6:
        from utils.output_formatter import get_default_formatter
        
        stock_input = args.args[0]
        formatter = get_default_formatter()
        
        print(f"\n{'='*70}")
        print(f"🔍 开始深度分析：{stock_input}")
        print(f"{'='*70}\n")
        
        # 获取股票信息
        stock_info = analyzer.get_stock_info(stock_input)
        if not stock_info:
            print(f"❌ 无法获取股票 {stock_input} 的信息")
            return
        
        # 获取技术数据
        tech_data = analyzer.get_technical_indicators(stock_input)
        analysis_result = analyzer.analyze_stock(stock_input)
        
        if analysis_result:
            output = formatter.format_comprehensive_report(analysis_result, args.format)
            print(output)
        
        print("\n" + "="*70)
        print("📄 第二部分：财务数据深度分析（数据来源：AKShare）")
        print("="*70)
        
        from core.financial_analyzer import FinancialAnalyzer
        financial_analyzer = FinancialAnalyzer()
        report_data = financial_analyzer.get_comprehensive_financial_report(stock_input)
        
        if report_data and report_data.get('key_metrics'):
            key_metrics = report_data['key_metrics']
            print("\n【关键财务指标】")
            for k, v in key_metrics.items():
                if not isinstance(v, dict):
                    print(f"  • {k}: {v}")
            
            print("\n💡 AI 将基于以上数据进行深度财务分析")
        
        print("\n" + "="*70)
        print("✅ 分析完成")
        print("="*70)
        return
    
    # 其他情况执行原有技能
    execute_skill(args.args, analyzer=analyzer, output_format=args.format)


if __name__ == "__main__":
    main()
