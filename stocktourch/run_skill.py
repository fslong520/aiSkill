#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票研究技能运行脚本
用于测试和执行股票分析功能
支持多种输出格式和参数配置
"""

import argparse
import sys
import os
from pathlib import Path

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, str(Path(__file__).parent))

from skill_executor import execute_skill
from stock_analyzer import StockAnalyzer
from config import print_config_summary

def main():
    """
    主函数，解析命令行参数并执行相应功能
    """
    parser = argparse.ArgumentParser(
        description="Stock Research Skill - 股票研究技能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析单只股票
  python3 run_skill.py 000001
  
  # 获取股票技术分析
  python3 run_skill.py 000001 technical
  
  # 获取沪深300成分股
  python3 run_skill.py hs300
  
  # 指定输出格式
  python3 run_skill.py 000001 --format json
  
  # 禁用缓存
  python3 run_skill.py 000001 --no-cache
  
  # 设置缓存TTL为12小时
  python3 run_skill.py 000001 --cache-ttl 12
        """
    )

    # 位置参数
    parser.add_argument('args', nargs='*', help='命令参数（股票代码、选项等）')

    # 缓存参数
    parser.add_argument('--no-cache', action='store_true',
                       help='禁用智能缓存')
    parser.add_argument('--cache-ttl', type=int, default=24,
                       help='缓存生存时间（小时，默认：24）')

    # 输出格式
    parser.add_argument('--format', '-f', choices=['text', 'json', 'csv'],
                       default='text', help='输出格式（默认：text）')

    # 详细输出
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细日志输出')
    
    # 配置查看
    parser.add_argument('--show-config', action='store_true',
                       help='显示当前配置')

    args = parser.parse_args()
    
    if args.show_config:
        print_config_summary()
        return

    if not args.args:
        print("股票研究技能使用说明:")
        print("用法: python3 run_skill.py [股票代码或命令] [选项] [参数...]")
        print("")
        print("基本命令:")
        print("  python3 run_skill.py 000001                    # 分析平安银行")
        print("  python3 run_skill.py 000001 analysis          # 深度分析")
        print("  python3 run_skill.py 000001 quote             # 获取实时行情")
        print("  python3 run_skill.py 000001 info              # 获取基本资料")
        print("  python3 run_skill.py 000001 technical         # 技术分析")
        print("  python3 run_skill.py 000001 fundamental       # 基本面分析")
        print("  python3 run_skill.py 000001 recommend         # 操作建议")
        print("")
        print("高级命令:")
        print("  python3 run_skill.py ranking                   # 板块涨跌幅排名")
        print("  python3 run_skill.py fear-greed              # 恐慌贪婪指数")
        print("")
        print("参数选项:")
        print("  --format {text,json,csv}                     # 输出格式")
        print("  --no-cache                                   # 禁用缓存")
        print("  --cache-ttl HOURS                           # 缓存TTL（小时）")
        print("  --limit NUM                                 # 文章数量限制")
        print("  --deep                                      # 深度分析")
        print("  --sentiment                                 # 情感分析")
        print("  --show-config                                # 显示当前配置")
        print("  --verbose                                    # 详细日志输出")
        print("")
        print("示例:")
        print("  python3 run_skill.py 000001 --format json     # JSON格式输出")
        print("  python3 run_skill.py hs300 --format csv       # CSV格式输出成分股")
        print("  python3 run_skill.py 000001 technical --no-cache  # 不使用缓存")
        print("  python3 run_skill.py market report --sources sina,eastmoney --limit 8  # 指定数据源和限制")
        print("  python3 run_skill.py --show-config            # 显示当前配置")
        return

    # 创建分析器实例
    cache_enabled = not args.no_cache
    analyzer = StockAnalyzer(cache_enabled=cache_enabled, cache_ttl_hours=args.cache_ttl)
    
    # 执行技能
    execute_skill(args.args, analyzer=analyzer, output_format=args.format)

if __name__ == "__main__":
    main()