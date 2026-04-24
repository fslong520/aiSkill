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

# 获取技能根目录的绝对路径 (无论从哪里执行)
SKILL_ROOT = Path(__file__).resolve().parent

# 将技能根目录添加到 Python 搜索路径
# 这样即使从工作目录执行，也能正确导入技能模块
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

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
            return 0  # 明确返回 0，表示成功退出
        
        key_metrics = report_data.get('key_metrics', {})
        multi_year_data = report_data.get('multi_year_data', [])  # 获取多年数据
        print(f"✅ 成功获取 {stock_input} 的财务数据（数据来源：AKShare）")
        if multi_year_data:
            print(f"   包含 {len(multi_year_data)} 个季度的历史数据")
        
        # 格式化输出所有关键数据给 AI
        print("\n" + "="*70)
        print("📋 完整财务数据包（供 AI 分析使用）")
        print("="*70)
        
        # 首先输出最新季度的详细数据
        print("\n【零、最新季度核心数据】")
        print(f"  • 报告期：{key_metrics.get('报告期', '最新季度')}")
        
        print("\n【一、资产负债表指标】")
        balance_items = [
            ('总资产', '总资产'),
            ('总负债', '总负债'),
            ('货币资金', '货币资金'),
            ('应收账款', '应收账款'),
            ('应收票据', '应收票据'),
            ('存货', '存货'),
            ('固定资产', '固定资产'),
            ('在建工程', '在建工程'),
            ('无形资产', '无形资产'),
            ('商誉', '商誉'),
            ('短期借款', '短期借款'),
            ('长期借款', '长期借款'),
            ('应付账款', '应付账款'),
            ('预收款项', '预收款项'),
            ('有息负债', '有息负债'),
            ('生产资产占比', '生产资产占比'),
            ('应收款项占比', '应收款项占比'),
            ('资金充裕度', '资金充裕度')
        ]
        for cn, en in balance_items:
            value = key_metrics.get(cn)
            if value is not None:
                if isinstance(value, float):
                    print(f"  • {cn}: {value:,.2f}")
                else:
                    print(f"  • {cn}: {value}")
        
        print("\n【二、利润表指标】")
        profit_items = [
            ('营业收入', '营业收入'),
            ('营业成本', '营业成本'),
            ('毛利润', '毛利润'),
            ('毛利率', '毛利率'),
            ('销售费用', '销售费用'),
            ('管理费用', '管理费用'),
            ('财务费用', '财务费用'),
            ('研发费用', '研发费用'),
            ('期间费用率', '期间费用率'),
            ('营业利润', '营业利润'),
            ('净利润', '净利润'),
            ('扣非净利润', '扣非净利润'),
            ('营业外收入', '营业外收入'),
            ('营业外收入占比', '营业外收入占比')
        ]
        for cn, en in profit_items:
            value = key_metrics.get(cn)
            if value is not None:
                if isinstance(value, float):
                    # 将金额从元转换为亿元
                    if cn in ['营业收入', '营业成本', '毛利润', '销售费用', '管理费用', '财务费用', '研发费用', '营业利润', '净利润', '扣非净利润', '营业外收入']:
                        value_in_yi = value / 100000000  # 转换为亿元
                        print(f"  • {cn}: {value_in_yi:,.2f}亿元")
                    elif cn == '毛利率':
                        print(f"  • {cn}: {value:.2f}%")
                    else:
                        print(f"  • {cn}: {value:,.2f}")
                else:
                    print(f"  • {cn}: {value}")
        
        print("\n【三、现金流量表指标】")
        cashflow_items = [
            ('经营现金流净额', '经营现金流净额'),
            ('投资现金流净额', '投资现金流净额'),
            ('筹资现金流净额', '筹资现金流净额'),
            ('销售商品收到的现金', '销售商品收到的现金'),
            ('净利润现金含量', '净利润现金含量'),
            ('现金流肖像', '现金流肖像')
        ]
        for cn, en in cashflow_items:
            value = key_metrics.get(cn)
            if value is not None:
                if isinstance(value, float):
                    # 将金额从元转换为亿元
                    if cn in ['经营现金流净额', '投资现金流净额', '筹资现金流净额', '销售商品收到的现金']:
                        value_in_yi = value / 100000000  # 转换为亿元
                        print(f"  • {cn}: {value_in_yi:,.2f}亿元")
                    elif cn == '净利润现金含量':
                        print(f"  • {cn}: {value:.2f}%")
                    else:
                        print(f"  • {cn}: {value:,.2f}")
                else:
                    print(f"  • {cn}: {value}")
        
        print("\n【四、财务比率指标】")
        ratio_items = [
            ('流动比率', '流动比率'),
            ('速动比率', '速动比率'),
            ('现金比率', '现金比率'),
            ('资产负债率', '资产负债率'),
            ('ROE', 'ROE'),
            ('销售净利率', '销售净利率'),
            ('销售毛利率', '销售毛利率'),
            ('EPS_TTM', 'EPS_TTM'),
            ('总股本', '总股本'),
            ('应收账款周转率', '应收账款周转率'),
            ('应收账款周转天数', '应收账款周转天数'),
            ('存货周转率', '存货周转率'),
            ('存货周转天数', '存货周转天数'),
            ('流动资产周转率', '流动资产周转率'),
            ('总资产周转率', '总资产周转率')
        ]
        for cn, en in ratio_items:
            value = key_metrics.get(cn)
            if value is not None:
                if isinstance(value, float):
                    print(f"  • {cn}: {value:,.2f}")
                else:
                    print(f"  • {cn}: {value}")
        
        print("\n【五、成长能力指标】")
        growth_items = [
            ('营收增长率', '营收增长率'),
            ('净利润增长率', '净利润增长率'),
            ('净资产同比增长率', '净资产同比增长率'),
            ('总资产同比增长率', '总资产同比增长率'),
            ('基本 EPS 同比增长率', '基本 EPS 同比增长率'),
            ('归母净利润同比增长率', '归母净利润同比增长率')
        ]
        for cn, en in growth_items:
            value = key_metrics.get(cn)
            if value is not None:
                if isinstance(value, float):
                    print(f"  • {cn}: {value:.2f}%")
                else:
                    print(f"  • {cn}: {value}")
        
        print("\n【六、杜邦分析指标】")
        dupont_items = [
            ('ROE_杜邦', 'ROE_杜邦'),
            ('销售净利率_杜邦', '销售净利率_杜邦'),
            ('总资产周转率_杜邦', '总资产周转率_杜邦'),
            ('权益乘数_杜邦', '权益乘数_杜邦'),
            ('税收负担', '税收负担'),
            ('利息负担', '利息负担'),
            ('息税前利润占营收', '息税前利润占营收')
        ]
        for cn, en in dupont_items:
            value = key_metrics.get(cn)
            if value is not None:
                if isinstance(value, float):
                    print(f"  • {cn}: {value:.4f}")
                else:
                    print(f"  • {cn}: {value}")
        
        print("\n【七、风险评估结果】")
        if '五大黄金标准' in key_metrics:
            standards = key_metrics['五大黄金标准'][0]
            print(f"  五大黄金标准：{standards.get('通过数量', 'N/A')} - {standards.get('评价', 'N/A')}")
            for k, v in standards.items():
                if not k.startswith('标准') and k not in ['通过数量', '评价']:
                    print(f"    - {k}: {v}")
        
        if '快速排雷清单' in key_metrics:
            checklist = key_metrics['快速排雷清单'][0]
            print(f"  快速排雷清单：{checklist.get('通过数量', 'N/A')} - {checklist.get('结论', 'N/A')}")
            for k, v in checklist.items():
                if k not in ['通过数量', '结论', '风险提示']:
                    print(f"    - {k}: {v}")
            if '风险提示' in checklist:
                print(f"    ⚠️ 风险提示：{checklist['风险提示']}")
        
        if '现金流肖像' in key_metrics:
            print(f"  现金流肖像：{key_metrics['现金流肖像'][0]}")
        
        print("\n" + "="*70)
        print("💡 AI 将基于以上完整数据进行深度财务分析")
        print("="*70)
        
        # 输出多年趋势数据（用于《读财报.md》中的趋势分析）
        print("\n" + "="*70)
        print("📈 多年财务趋势数据（用于 5 年对比分析）")
        print("="*70)
        
        if multi_year_data and len(multi_year_data) > 0:
            print(f"\n✅ 获取到 {len(multi_year_data)} 个季度的历史数据")
            
            # 按年度汇总关键指标
            yearly_summary = {}
            for data in multi_year_data:
                year = data.get('year')
                quarter = data.get('quarter')
                year_key = f"{year}年"
                
                if year_key not in yearly_summary:
                    yearly_summary[year_key] = {
                        'quarters': [],
                        'revenue': [],
                        'net_profit': [],
                        'roe': [],
                        'gross_margin': [],
                        'debt_ratio': []
                    }
                
                yearly_summary[year_key]['quarters'].append(f"Q{quarter}")
                
                # 提取关键指标 (单位：元)
                if data.get('profit_statement') is not None and len(data['profit_statement']) > 0:
                    try:
                        latest = data['profit_statement'].iloc[-1]
                        revenue = float(latest.get('MBRevenue', 0) or 0)  # 元
                        net_profit = float(latest.get('netProfit', 0) or 0)  # 元
                        roe = float(latest.get('roeAvg', 0) or 0)
                        gp_margin = float(latest.get('gpMargin', 0) or 0)
                        
                        # 转换为亿元存储
                        yearly_summary[year_key]['revenue'].append(revenue / 100000000)
                        yearly_summary[year_key]['net_profit'].append(net_profit / 100000000)
                        yearly_summary[year_key]['roe'].append(roe * 100 if roe else 0)
                        yearly_summary[year_key]['gross_margin'].append(gp_margin * 100 if gp_margin else 0)
                    except Exception as e:
                        pass
                
                if data.get('balance_sheet') is not None and len(data['balance_sheet']) > 0:
                    try:
                        latest = data['balance_sheet'].iloc[-1]
                        debt_ratio = float(latest.get('liabilityToAsset', 0) or 0)
                        yearly_summary[year_key]['debt_ratio'].append(debt_ratio * 100 if debt_ratio else 0)
                    except Exception as e:
                        pass
            
            # 输出年度汇总
            print("\n【年度核心指标汇总】")
            for year_key in sorted(yearly_summary.keys(), reverse=True):
                data = yearly_summary[year_key]
                print(f"\n{year_key}:")
                print(f"  季度：{', '.join(data['quarters'])}")
                
                if data['revenue']:
                    avg_revenue = sum(data['revenue']) / len(data['revenue'])
                    print(f"  平均营业收入：{avg_revenue:,.2f} 亿元")
                
                if data['net_profit']:
                    avg_profit = sum(data['net_profit']) / len(data['net_profit'])
                    print(f"  平均净利润：{avg_profit:,.2f} 亿元")
                
                if data['roe']:
                    avg_roe = sum(data['roe']) / len(data['roe'])
                    print(f"  平均 ROE: {avg_roe:.2f}%")
                
                if data['gross_margin']:
                    avg_margin = sum(data['gross_margin']) / len(data['gross_margin'])
                    print(f"  平均毛利率：{avg_margin:.2f}%")
                
                if data['debt_ratio']:
                    avg_debt = sum(data['debt_ratio']) / len(data['debt_ratio'])
                    print(f"  平均资产负债率：{avg_debt:.2f}%")
            
            # 输出趋势分析提示
            print("\n【五年趋势分析要点】")
            years_list = list(yearly_summary.keys())
            if len(years_list) >= 2:
                latest_year = years_list[0]
                oldest_year = years_list[-1]
                
                # 营收增长趋势
                if yearly_summary[latest_year]['revenue'] and yearly_summary[oldest_year]['revenue']:
                    latest_rev = sum(yearly_summary[latest_year]['revenue']) / len(yearly_summary[latest_year]['revenue'])
                    oldest_rev = sum(yearly_summary[oldest_year]['revenue']) / len(yearly_summary[oldest_year]['revenue'])
                    rev_growth = ((latest_rev - oldest_rev) / abs(oldest_rev) * 100) if oldest_rev != 0 else 0
                    print(f"  • 营收 {oldest_year[:4]}→{latest_year[:4]}: {'增长' if rev_growth > 0 else '下降'} {abs(rev_growth):.1f}%")
                
                # 利润增长趋势
                if yearly_summary[latest_year]['net_profit'] and yearly_summary[oldest_year]['net_profit']:
                    latest_profit = sum(yearly_summary[latest_year]['net_profit']) / len(yearly_summary[latest_year]['net_profit'])
                    oldest_profit = sum(yearly_summary[oldest_year]['net_profit']) / len(yearly_summary[oldest_year]['net_profit'])
                    profit_growth = ((latest_profit - oldest_profit) / abs(oldest_profit) * 100) if oldest_profit != 0 else 0
                    print(f"  • 净利润 {oldest_year[:4]}→{latest_year[:4]}: {'增长' if profit_growth > 0 else '下降'} {abs(profit_growth):.1f}%")
                
                # ROE 趋势
                if yearly_summary[latest_year]['roe'] and yearly_summary[oldest_year]['roe']:
                    latest_roe = sum(yearly_summary[latest_year]['roe']) / len(yearly_summary[latest_year]['roe'])
                    oldest_roe = sum(yearly_summary[oldest_year]['roe']) / len(yearly_summary[oldest_year]['roe'])
                    roe_change = latest_roe - oldest_roe
                    print(f"  • ROE {oldest_year[:4]}→{latest_year[:4]}: {'提升' if roe_change > 0 else '下降'} {abs(roe_change):.2f}个百分点")
                
                # 毛利率趋势
                if yearly_summary[latest_year]['gross_margin'] and yearly_summary[oldest_year]['gross_margin']:
                    latest_margin = sum(yearly_summary[latest_year]['gross_margin']) / len(yearly_summary[latest_year]['gross_margin'])
                    oldest_margin = sum(yearly_summary[oldest_year]['gross_margin']) / len(yearly_summary[oldest_year]['gross_margin'])
                    margin_change = latest_margin - oldest_margin
                    print(f"  • 毛利率 {oldest_year[:4]}→{latest_year[:4]}: {'上升' if margin_change > 0 else '下降'} {abs(margin_change):.2f}个百分点")
                
                # 负债率趋势
                if yearly_summary[latest_year]['debt_ratio'] and yearly_summary[oldest_year]['debt_ratio']:
                    latest_debt = sum(yearly_summary[latest_year]['debt_ratio']) / len(yearly_summary[latest_year]['debt_ratio'])
                    oldest_debt = sum(yearly_summary[oldest_year]['debt_ratio']) / len(yearly_summary[oldest_year]['debt_ratio'])
                    debt_change = latest_debt - oldest_debt
                    print(f"  • 资产负债率 {oldest_year[:4]}→{latest_year[:4]}: {'上升' if debt_change > 0 else '下降'} {abs(debt_change):.2f}个百分点")
        else:
            print("⚠️ 未能获取到多年历史数据")
        
        print("\n" + "="*70)
        print("💡 AI 将基于多年趋势数据进行深度财务分析")
        print("    重点分析：营收增长率、利润增长率、ROE 趋势、毛利率变化、负债率变化")
        print("="*70)
        
        # 重要：输出完成后立即返回，避免后续代码继续执行
        # 注意：不要使用 sys.exit(0)，否则会导致 [Errno 9] 错误
        return 0
    
    # 其他情况执行原有技能
    else :
        # 创建分析器实例
        cache_enabled = not args.no_cache
        analyzer = StockAnalyzer(cache_enabled=cache_enabled, cache_ttl_hours=args.cache_ttl)
        execute_skill(args.args, analyzer=analyzer, output_format=args.format)


if __name__ == "__main__":
    main()
