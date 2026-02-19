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
import json
from pathlib import Path

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, str(Path(__file__).parent))

from executor.skill_executor import execute_skill
from core.stock_analyzer import StockAnalyzer
from utils.config import print_config_summary
from utils.output_formatter import get_default_formatter


def analyze_stock_with_financial_report(stock_input: str, analyzer: StockAnalyzer, output_format: str = 'text'):
    """
    完整的股票分析：包含三部分
    第一部分：最新财务指标（baostock数据）
    第二部分：财报AI分析（巨潮资讯网财报）
    第三部分：消息面分析（AI联网搜索）
    """
    print(f"\n{'='*70}")
    print(f"🔍 开始深度分析: {stock_input}")
    print(f"{'='*70}\n")

    formatter = get_default_formatter()

    # 初始化股票名称
    stock_name = stock_input  # 默认使用输入

    # ========== 第一部分：最新财务指标 ==========
    print("📊 第一部分：最新财务指标分析")
    print("-" * 50)

    # 获取股票基本信息和技术数据
    stock_info = analyzer.get_stock_info(stock_input)
    if not stock_info:
        print(f"❌ 无法获取股票 {stock_input} 的信息")
        return

    # 获取技术指标
    tech_data = analyzer.get_technical_indicators(stock_input)

    # 获取综合分析结果
    analysis_result = analyzer.analyze_stock(stock_input)

    # 输出格式化结果
    if analysis_result:
        output = formatter.format_comprehensive_report(analysis_result, output_format)
        print(output)

    # 保存第一部分结果供AI综合使用，并提取股票名称
    part1_data = {
        "stock_info": stock_info,
        "tech_data": tech_data,
        "analysis_result": analysis_result,
    }

    # 提取股票名称
    if stock_info and 'name' in stock_info:
        stock_name = stock_info['name']
    elif analysis_result and 'stock_info' in analysis_result:
        stock_name = analysis_result.get('stock_info', {}).get('name', stock_input)

    print(f"\n{'='*70}")
    print("📄 第二部分：财报AI深度分析（巨潮资讯网）")
    print("-" * 50)

    # ========== 第二部分：财报AI分析 ==========
    try:
        from report.cninfo_downloader import download_reports
        from report.report_reader import get_report_summary

        print(f"\n📥 正在下载 {stock_input} 的财报...")

        result = download_reports(stock_input)

        if "error" in result:
            print(f"⚠️ 财报下载失败: {result['error']}")
            print("\n" + "="*70)
            print("💡 可单独运行以下命令进行财报分析:")
            print(f"   python3 run_skill.py {stock_input} report")
            print("="*70)
            # 即使财报下载失败，也输出第一部分结果
            print("\n" + "="*70)
            print("✅ 第一部分分析完成（最新财务指标）")
            print("="*70)
            return

        print(f"✅ 找到股票: {result['stock_name']} ({result['stock_code']})")
        print(f"📄 下载财报: {len(result['files'])} 份\n")

        # 提取财报内容
        reports_data = []
        for pdf_file in result["files"]:
            print(f"  提取中: {os.path.basename(pdf_file)[:40]}...")
            report_data = get_report_summary(pdf_file, result["stock_name"])
            reports_data.append(report_data)

        print(f"\n✅ 财报提取完成，共 {len(reports_data)} 份")

        # 输出财报摘要
        print("\n" + "="*70)
        print("📋 财报内容摘要")
        print("="*70)

        for i, report in enumerate(reports_data, 1):
            year = report.get('year', '未知')
            highlights = report.get('highlights', {})
            print(f"\n【{year}年财报】关键指标:")
            if highlights:
                for k, v in highlights.items():
                    print(f"  • {k}: {v}")
            else:
                print("  (指标提取中...)")

        # 构建AI分析提示
        ai_prompt = f"""
{'='*70}
📈 第二部分：财报AI深度分析
{'='*70}

股票: {result['stock_name']}({result['stock_code']})

已获取财报数据 ({len(reports_data)}份):
"""

        for report in reports_data:
            year = report.get('year', '未知')
            highlights = report.get('highlights', {})
            ai_prompt += f"\n【{year}年财报】\n"
            if highlights:
                for k, v in highlights.items():
                    ai_prompt += f"  - {k}: {v}\n"
            ai_prompt += f"\n内容要点:\n{report.get('text_preview', '')[:2000]}\n"

        ai_prompt += f"""
{'='*70}
请基于以上数据，进行专业的财务分析:
1. 营收和利润趋势分析
2. 盈利能力评估 (毛利率、净利率、ROE)
3. 资产负债状况和偿债能力
4. 现金流分析
5. 主要风险点识别
6. 综合投资建议

请用专业的财务分析方法进行分析，给出明确的买入/卖出/持有建议。
{'='*70}
"""

        print(ai_prompt)

    except Exception as e:
        print(f"⚠️ 财报分析出错: {e}")
        import traceback
        traceback.print_exc()

    # ========== 第三部分：消息面分析（联网搜索） ==========
    print("\n" + "="*70)
    print("📰 第三部分：消息面分析（AI联网搜索）")
    print("-" * 50)

    # 构建搜索提示，引导AI进行联网搜索
    search_queries = [
        f"{stock_name} {stock_input} 股票 最新消息",
        f"{stock_name} {stock_input} 公告 研报",
        f"{stock_name} 行业动态 政策",
    ]

    news_analysis_prompt = f"""
{'='*70}
📰 第三部分：消息面分析
{'='*70}

股票: {stock_name}({stock_input})

请AI调用内置搜索工具，搜索以下关键词的最新新闻和消息：

1. 公司最新公告和重大事项
2. 行业动态和政策变化
3. 分析师评级和投资建议
4. 机构持仓和调研情况
5. 相关板块走势

建议搜索关键词:
"""

    for i, query in enumerate(search_queries, 1):
        news_analysis_prompt += f"  • {query}\n"

    news_analysis_prompt += f"""
{'='*70}
请基于搜索结果，进行消息面分析:
1. 近期重大利好/利空消息
2. 市场情绪和资金流向
3. 机构观点和评级变化
4. 行业政策和趋势影响
5. 综合消息面评估

注意: 请实际调用搜索工具获取最新信息，不要假设。
{'='*70}
"""

    print(news_analysis_prompt)

    print("\n" + "="*70)
    print("✅ 完整分析完成（技术面+财务面+消息面）")
    print("="*70)


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
        print("财报分析命令:")
        print("  python3 run_skill.py 000001 report           # 下载财报并AI分析")
        print("  python3 run_skill.py 600519 report          # 下载茅台财报并分析")
        print("  python3 run_skill.py 贵州茅台 report        # 按名称下载并分析")
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

    # 处理财报分析命令
    if len(args.args) >= 2 and args.args[1].lower() in ["report", "财报", "download", "analysis"]:
        # 下载财报并用AI分析
        stock_input = args.args[0]

        print(f"\n{'='*60}")
        print(f"📥 开始分析股票财报: {stock_input}")
        print(f"{'='*60}\n")

        from report.cninfo_downloader import download_reports
        result = download_reports(stock_input)

        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            return

        print(f"📊 找到股票: {result['stock_name']} ({result['stock_code']}) [{result['market_display']}]")
        print(f"📄 下载财报: {len(result['files'])} 份\n")

        # 提取财报内容
        from report_reader import get_report_summary
        reports_data = []
        
        for pdf_file in result["files"]:
            print(f"  正在提取: {os.path.basename(pdf_file)[:50]}...")
            report_data = get_report_summary(pdf_file, result["stock_name"])
            reports_data.append(report_data)

        print(f"\n{'='*60}")
        print(f"✅ 财报内容提取完成")
        print(f"  股票: {result['stock_name']} ({result['stock_code']})")
        print(f"  财报数量: {len(reports_data)} 份")
        print(f"{'='*60}\n")

        # 输出详细的财报摘要供AI分析
        print("="*60)
        print("📋 财报内容摘要")
        print("="*60)
        
        for i, report in enumerate(reports_data, 1):
            print(f"\n--- 财报 {i}: {report['file']} ---")
            print(f"年份: {report['year']}")
            if report['highlights']:
                print("关键指标:")
                for k, v in report['highlights'].items():
                    print(f"  - {k}: {v}")
            if report['text_preview']:
                print(f"\n内容预览 (前3000字):")
                print(report['text_preview'][:3000])
            print("\n" + "-"*40)

        print(f"\n{'='*60}")
        print("💡 AI将基于以上财报内容进行深度分析...")
        print("="*60)
        
        # 构建提示给AI
        ai_prompt = f"""请分析 {result['stock_name']}({result['stock_code']}) 的财务状况。

已获取的财报数据:
"""
        for report in reports_data:
            ai_prompt += f"\n【{report['file']}】\n"
            ai_prompt += f"年份: {report['year']}\n"
            if report['highlights']:
                ai_prompt += "关键财务指标:\n"
                for k, v in report['highlights'].items():
                    ai_prompt += f"  - {k}: {v}\n"
            ai_prompt += f"\n内容预览:\n{report['text_preview'][:3000]}\n"

        ai_prompt += f"""

请进行以下分析:
1. 营收和利润趋势分析
2. 盈利能力评估 (毛利率、净利率、ROE)
3. 资产负债状况
4. 现金流分析
5. 主要风险点识别
6. 综合投资建议

请用专业的财务分析方法进行分析，给出明确的买入/卖出/持有建议。
"""

        # 输出提示，AI会继续处理
        print("\n" + "="*60)
        print("🔍 财务分析报告")
        print("="*60)
        print(f"\n{ai_prompt}")
        return

    # 判断是否为简单的股票代码分析命令
    # 如果只有一个参数（股票代码），自动执行完整分析（两部分财务分析）
    if len(args.args) == 1 and args.args[0].isdigit() and len(args.args[0]) == 6:
        # 用户输入的是6位股票代码，执行完整分析
        analyze_stock_with_financial_report(args.args[0], analyzer, args.format)
        return

    # 其他情况执行原有技能
    execute_skill(args.args, analyzer=analyzer, output_format=args.format)

if __name__ == "__main__":
    main()