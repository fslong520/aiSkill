#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出格式化模块
负责将分析结果格式化为不同的输出格式
"""

import json
import pandas as pd
from utils import format_number, format_large_number


class OutputFormatter:
    """输出格式化器"""
    
    def __init__(self):
        self.supported_formats = ['text', 'json', 'csv']
    
    def format_stock_info(self, stock_info, output_format='text'):
        """格式化股票基本信息"""
        if output_format == 'json':
            return json.dumps(stock_info, ensure_ascii=False, indent=2)
        elif output_format == 'csv':
            df = pd.DataFrame([stock_info])
            return df.to_csv(index=False)
        else:  # text format
            lines = [
                "【股票信息】",
                f"股票代码: {stock_info.get('code', 'N/A')}",
                f"股票名称: {stock_info.get('name', 'N/A')}",
                f"当前价格: {format_number(stock_info.get('price', 0))}",
                f"涨跌幅: {format_number(stock_info.get('change', 0))}%",
                f"涨跌金额: {format_number(stock_info.get('change_amount', 0))}",
                f"成交量: {format_large_number(stock_info.get('volume', 0))}",
                f"成交金额: {format_large_number(stock_info.get('amount', 0))}",
                f"昨日收盘: {format_number(stock_info.get('close_yesterday', 0))}",
            ]
            return "\n".join(lines)
    
    def format_technical_analysis(self, tech_data, symbol, output_format='text'):
        """格式化技术分析结果"""
        if output_format == 'json':
            return json.dumps({
                'symbol': symbol,
                'indicators': {
                    'rsi': tech_data.get('latest_rsi'),
                    'macd': tech_data.get('latest_macd'),
                    'k': tech_data.get('latest_k'),
                    'd': tech_data.get('latest_d'),
                    'j': tech_data.get('latest_j'),
                    'support': tech_data.get('support'),
                    'resistance': tech_data.get('resistance')
                },
                'moving_averages': {
                    'ma5': tech_data['data']['ma5'].iloc[-1] if 'data' in tech_data and 'ma5' in tech_data['data'] else None,
                    'ma10': tech_data['data']['ma10'].iloc[-1] if 'data' in tech_data and 'ma10' in tech_data['data'] else None,
                    'ma20': tech_data['data']['ma20'].iloc[-1] if 'data' in tech_data and 'ma20' in tech_data['data'] else None,
                }
            }, ensure_ascii=False, indent=2)
        elif output_format == 'csv':
            # 创建技术指标的DataFrame
            indicators = {
                'Symbol': [symbol],
                'RSI': [tech_data.get('latest_rsi')],
                'MACD': [tech_data.get('latest_macd')],
                'K': [tech_data.get('latest_k')],
                'D': [tech_data.get('latest_d')],
                'J': [tech_data.get('latest_j')],
                'Support': [tech_data.get('support')],
                'Resistance': [tech_data.get('resistance')]
            }
            df = pd.DataFrame(indicators)
            return df.to_csv(index=False)
        else:  # text format
            latest_data = tech_data['data'].iloc[-1] if 'data' in tech_data and not tech_data['data'].empty else None
            ma5_trend = ''
            ma10_trend = ''
            ma20_trend = ''
            
            if latest_data is not None and len(tech_data['data']) > 1:
                prev_data = tech_data['data'].iloc[-2]
                ma5_trend = '↑' if latest_data['ma5'] > prev_data['ma5'] else '↓'
                ma10_trend = '↑' if latest_data['ma10'] > prev_data['ma10'] else '↓'
                ma20_trend = '↑' if latest_data['ma20'] > prev_data['ma20'] else '↓'
            else:
                ma5_trend = '?'
                ma10_trend = '?'
                ma20_trend = '?'
                
            lines = [
                f"【{symbol} 技术分析】",
                f"MA5: {format_number(latest_data['ma5'] if latest_data is not None and 'ma5' in latest_data else 0)}({ma5_trend}) | MA10: {format_number(latest_data['ma10'] if latest_data is not None and 'ma10' in latest_data else 0)}({ma10_trend}) | MA20: {format_number(latest_data['ma20'] if latest_data is not None and 'ma20' in latest_data else 0)}({ma20_trend})",
                f"MA30: {format_number(latest_data['ma30'] if latest_data is not None and 'ma30' in latest_data else 0)}",
                f"RSI(14): {format_number(tech_data.get('latest_rsi', 0))} | MACD_DIF: {format_number(tech_data.get('latest_macd', 0))}",
                f"KDJ_K: {format_number(tech_data.get('latest_k', 0))} | KDJ_D: {format_number(tech_data.get('latest_d', 0))} | KDJ_J: {format_number(tech_data.get('latest_j', 0))}",
                f"布林带上轨: {format_number(latest_data['bb_upper'] if latest_data is not None and 'bb_upper' in latest_data else 0)} | 布林带中轨: {format_number(latest_data['bb_middle'] if latest_data is not None and 'bb_middle' in latest_data else 0)} | 布林带下轨: {format_number(latest_data['bb_lower'] if latest_data is not None and 'bb_lower' in latest_data else 0)}",
                f"支撑位: {format_number(tech_data.get('support', 0))} | 压力位: {format_number(tech_data.get('resistance', 0))}",
            ]
            return "\n".join(lines)
    
    def format_fundamental_analysis(self, stock_info, output_format='text'):
        """格式化基本面分析结果"""
        if output_format == 'json':
            fundamentals = {
                'pe': stock_info.get('pe'),
                'pb': stock_info.get('pb'),
                'turnover_rate': stock_info.get('turnover_rate')
            }
            return json.dumps(fundamentals, ensure_ascii=False, indent=2)
        elif output_format == 'csv':
            fundamentals = {
                'PE': [stock_info.get('pe')],
                'PB': [stock_info.get('pb')],
                'Turnover_Rate': [stock_info.get('turnover_rate')]
            }
            df = pd.DataFrame(fundamentals)
            return df.to_csv(index=False)
        else:  # text format
            lines = [
                f"【{stock_info.get('code', 'N/A')} 基本面分析】",
                f"市盈率(PE): {format_number(stock_info.get('pe', 0))}",
                f"市净率(PB): {format_number(stock_info.get('pb', 0))}",
                f"换手率: {format_number(stock_info.get('turnover_rate', 0))}"
            ]
            return "\n".join(lines)
    
    def format_financial_analysis(self, financial_data, symbol, output_format='text'):
        """格式化财务分析结果"""
        if output_format == 'json':
            return json.dumps(financial_data, ensure_ascii=False, indent=2)
        elif output_format == 'csv':
            # 财务数据可能来自多个表，需要合并为一个DataFrame
            if financial_data:
                financial_summary = {
                    'Symbol': [symbol],
                    'ROE': [financial_data.get('roe', 0)],
                    'ROA': [financial_data.get('roa', 0)],
                    'Gross_Margin': [financial_data.get('gross_margin', 0)],
                    'Net_Margin': [financial_data.get('net_margin', 0)],
                    'Debt_to_Asset_Ratio': [financial_data.get('debt_to_asset_ratio', 0)],
                    'Current_Ratio': [financial_data.get('current_ratio', 0)],
                    'Quick_Ratio': [financial_data.get('quick_ratio', 0)],
                    'Receivables_Turnover': [financial_data.get('receivables_turnover', 0)],
                    'Inventory_Turnover': [financial_data.get('inventory_turnover', 0)],
                    'Total_Assets_Turnover': [financial_data.get('total_assets_turnover', 0)],
                    'Net_Profit_Growth': [financial_data.get('net_profit_growth', 0)],
                    'Operating_Income_Growth': [financial_data.get('operating_income_growth', 0)],
                    'Total_Assets_Growth': [financial_data.get('total_assets_growth', 0)]
                }
                df = pd.DataFrame(financial_summary)
                return df.to_csv(index=False)
            else:
                df = pd.DataFrame({'Symbol': [symbol]})
                return df.to_csv(index=False)
        else:  # text format
            if financial_data:
                lines = [
                    f"【{symbol} 财务分析】",
                    f"盈利能力:",
                    f"  - ROE(净资产收益率): {format_number(financial_data.get('roe', 0))}%",
                    f"  - ROA(总资产报酬率): {format_number(financial_data.get('roa', 0))}%",
                    f"  - 销售毛利率: {format_number(financial_data.get('gross_margin', 0))}%",
                    f"  - 销售净利率: {format_number(financial_data.get('net_margin', 0))}%",
                    f"偿债能力:",
                    f"  - 资产负债率: {format_number(financial_data.get('debt_to_asset_ratio', 0))}%",
                    f"  - 流动比率: {format_number(financial_data.get('current_ratio', 0))}",
                    f"  - 速动比率: {format_number(financial_data.get('quick_ratio', 0))}",
                    f"营运能力:",
                    f"  - 应收账款周转率: {format_number(financial_data.get('receivables_turnover', 0))}",
                    f"  - 存货周转率: {format_number(financial_data.get('inventory_turnover', 0))}",
                    f"  - 总资产周转率: {format_number(financial_data.get('total_assets_turnover', 0))}",
                    f"成长能力:",
                    f"  - 净利润增长率: {format_number(financial_data.get('net_profit_growth', 0))}%",
                    f"  - 营业收入增长率: {format_number(financial_data.get('operating_income_growth', 0))}%",
                    f"  - 总资产增长率: {format_number(financial_data.get('total_assets_growth', 0))}%"
                ]
            else:
                lines = [
                    f"【{symbol} 财务分析】",
                    "暂无财务数据"
                ]
            return "\n".join(lines)
    
    def format_comprehensive_report(self, analysis_result, output_format='text'):
        """格式化综合分析报告"""
        if output_format == 'json':
            # 为了JSON序列化，需要处理DataFrame对象
            import copy
            json_result = copy.deepcopy(analysis_result)
            if 'technical_data' in json_result and json_result['technical_data'] and 'data' in json_result['technical_data']:
                # 只保留必要的技术指标值，而不是整个DataFrame
                tech_data = json_result['technical_data']
                simplified_tech = {
                    'latest_rsi': tech_data.get('latest_rsi', 0),
                    'latest_macd': tech_data.get('latest_macd', 0),
                    'latest_k': tech_data.get('latest_k', 0),
                    'latest_d': tech_data.get('latest_d', 0),
                    'latest_j': tech_data.get('latest_j', 0),
                    'support': tech_data.get('support', 0),
                    'resistance': tech_data.get('resistance', 0)
                }
                # 添加最近的技术指标值
                if tech_data.get('data') is not None and not tech_data['data'].empty:
                    latest_row = tech_data['data'].iloc[-1]
                    simplified_tech.update({
                        'ma5': latest_row.get('ma5', 0),
                        'ma10': latest_row.get('ma10', 0),
                        'ma20': latest_row.get('ma20', 0),
                        'ma30': latest_row.get('ma30', 0),
                        'bb_upper': latest_row.get('bb_upper', 0),
                        'bb_middle': latest_row.get('bb_middle', 0),
                        'bb_lower': latest_row.get('bb_lower', 0),
                        'macd_dif': latest_row.get('macd_dif', 0),
                        'macd_dea': latest_row.get('macd_dea', 0),
                        'macd_bar': latest_row.get('macd_bar', 0),
                        'current_price': latest_row.get('close', 0),
                        'high': latest_row.get('high', 0),
                        'low': latest_row.get('low', 0),
                        'open': latest_row.get('open', 0),
                        'volume': latest_row.get('volume', 0)
                    })
                json_result['technical_data'] = simplified_tech
            
            # 添加财务数据
            if 'financial_data' in json_result:
                # financial_data通常是字典，可以直接序列化
                pass  # 不需要特殊处理
            
            return json.dumps(json_result, ensure_ascii=False, indent=2, default=str)
        elif output_format == 'csv':
            # 将综合报告转换为CSV格式
            report_data = {
                'Code': [analysis_result.get('stock_info', {}).get('code', 'N/A')],
                'Name': [analysis_result.get('stock_info', {}).get('name', 'N/A')],
                'Price': [analysis_result.get('stock_info', {}).get('price', 0)],
                'Change': [analysis_result.get('stock_info', {}).get('change', 0)],
                'MA5': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['ma5'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'ma5' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'MA10': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['ma10'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'ma10' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'MA20': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['ma20'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'ma20' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'MA30': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['ma30'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'ma30' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'BB_Upper': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['bb_upper'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'bb_upper' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'BB_Middle': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['bb_middle'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'bb_middle' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'BB_Lower': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['bb_lower'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'bb_lower' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'MACD_DIF': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['macd_dif'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'macd_dif' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'MACD_DEA': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['macd_dea'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'macd_dea' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'MACD_Bar': [analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).iloc[-1]['macd_bar'] if analysis_result.get('technical_data', {}).get('data') is not None and not analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).empty and 'macd_bar' in analysis_result.get('technical_data', {}).get('data', pd.DataFrame()).columns else 0],
                'RSI': [analysis_result.get('technical_data', {}).get('latest_rsi', 0)],
                'Support': [analysis_result.get('technical_data', {}).get('support', 0)],
                'Resistance': [analysis_result.get('technical_data', {}).get('resistance', 0)],
                'Fundamental_Score': [analysis_result.get('scores', {}).get('basic_score', 0)],
                'Technical_Score': [analysis_result.get('scores', {}).get('tech_score', 0)],
                'Sentiment_Score': [analysis_result.get('scores', {}).get('market_score', 0)],
                'Financial_Score': [analysis_result.get('scores', {}).get('financial_score', 0)],  # 新增财务评分
                'Total_Score': [analysis_result.get('scores', {}).get('overall_score', 0)],
                'Recommendation': [analysis_result.get('recommendation', {}).get('recommendation', 'N/A')],
                # 财务指标列
                'ROE': [analysis_result.get('financial_data', {}).get('roe', 0)],
                'ROA': [analysis_result.get('financial_data', {}).get('roa', 0)],
                'Gross_Margin': [analysis_result.get('financial_data', {}).get('gross_margin', 0)],
                'Net_Margin': [analysis_result.get('financial_data', {}).get('net_margin', 0)],
                'Debt_to_Asset_Ratio': [analysis_result.get('financial_data', {}).get('debt_to_asset_ratio', 0)],
                'Current_Ratio': [analysis_result.get('financial_data', {}).get('current_ratio', 0)],
                'Quick_Ratio': [analysis_result.get('financial_data', {}).get('quick_ratio', 0)],
                'Receivables_Turnover': [analysis_result.get('financial_data', {}).get('receivables_turnover', 0)],
                'Inventory_Turnover': [analysis_result.get('financial_data', {}).get('inventory_turnover', 0)],
                'Total_Assets_Turnover': [analysis_result.get('financial_data', {}).get('total_assets_turnover', 0)],
                'Net_Profit_Growth': [analysis_result.get('financial_data', {}).get('net_profit_growth', 0)],
                'Operating_Income_Growth': [analysis_result.get('financial_data', {}).get('operating_income_growth', 0)],
                'Total_Assets_Growth': [analysis_result.get('financial_data', {}).get('total_assets_growth', 0)]
            }
            df = pd.DataFrame(report_data)
            return df.to_csv(index=False)
        else:  # text format
            stock_info = analysis_result.get('stock_info', {})
            technical_data = analysis_result.get('technical_data', {})
            financial_data = analysis_result.get('financial_data', {})
            scoring = analysis_result.get('scores', {})
            recommendation = analysis_result.get('recommendation', {})
            
            lines = [
                "="*60,
                "                           股票综合分析报告",
                "="*60,
                "【股票信息】",
                f"股票代码: {stock_info.get('code', 'N/A'):15} 股票名称: {stock_info.get('name', 'N/A')}",
                f"当前价格: {format_number(stock_info.get('price', 0)):15} 涨跌幅: {format_number(stock_info.get('change', 0))}%",
                f"涨跌金额: {format_number(stock_info.get('change_amount', 0)):15} 成交量: {format_large_number(stock_info.get('volume', 0))}",
                f"成交金额: {format_large_number(stock_info.get('amount', 0)):14} 昨日收盘: {format_number(stock_info.get('close_yesterday', 0))}",
                "",
                "【技术分析】",
                f"MA5: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['ma5'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'ma5' in technical_data.get('data', pd.DataFrame()).columns else 0)} | MA10: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['ma10'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'ma10' in technical_data.get('data', pd.DataFrame()).columns else 0)} | MA20: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['ma20'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'ma20' in technical_data.get('data', pd.DataFrame()).columns else 0)} | MA30: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['ma30'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'ma30' in technical_data.get('data', pd.DataFrame()).columns else 0)}",
                f"RSI(14): {format_number(technical_data.get('latest_rsi', 0))} | MACD_DIF: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['macd_dif'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'macd_dif' in technical_data.get('data', pd.DataFrame()).columns else 0)}",
                f"KDJ_K: {format_number(technical_data.get('latest_k', 0))} | KDJ_D: {format_number(technical_data.get('latest_d', 0))} | KDJ_J: {format_number(technical_data.get('latest_j', 0))}",
                f"布林带上轨: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['bb_upper'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'bb_upper' in technical_data.get('data', pd.DataFrame()).columns else 0)} | 布林带中轨: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['bb_middle'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'bb_middle' in technical_data.get('data', pd.DataFrame()).columns else 0)} | 布林带下轨: {format_number(technical_data.get('data', pd.DataFrame()).iloc[-1]['bb_lower'] if technical_data.get('data') is not None and not technical_data.get('data', pd.DataFrame()).empty and 'bb_lower' in technical_data.get('data', pd.DataFrame()).columns else 0)}",
                f"支撑位: {format_number(technical_data.get('support', 0))} | 压力位: {format_number(technical_data.get('resistance', 0))}",
                "",
                "【财务分析】",
            ]
            
            # 添加财务分析内容
            if financial_data:
                lines.extend([
                    f"盈利能力:",
                    f"  - ROE(净资产收益率): {format_number(financial_data.get('roe', 0))}%",
                    f"  - ROA(总资产报酬率): {format_number(financial_data.get('roa', 0))}%",
                    f"  - 销售毛利率: {format_number(financial_data.get('gross_margin', 0))}%",
                    f"  - 销售净利率: {format_number(financial_data.get('net_margin', 0))}%",
                    f"偿债能力:",
                    f"  - 资产负债率: {format_number(financial_data.get('debt_to_asset_ratio', 0))}%",
                    f"  - 流动比率: {format_number(financial_data.get('current_ratio', 0))}",
                    f"  - 速动比率: {format_number(financial_data.get('quick_ratio', 0))}",
                    f"营运能力:",
                    f"  - 应收账款周转率: {format_number(financial_data.get('receivables_turnover', 0))}",
                    f"  - 存货周转率: {format_number(financial_data.get('inventory_turnover', 0))}",
                    f"  - 总资产周转率: {format_number(financial_data.get('total_assets_turnover', 0))}",
                    f"成长能力:",
                    f"  - 净利润增长率: {format_number(financial_data.get('net_profit_growth', 0))}%",
                    f"  - 营业收入增长率: {format_number(financial_data.get('operating_income_growth', 0))}%",
                    f"  - 总资产增长率: {format_number(financial_data.get('total_assets_growth', 0))}%",
                    ""
                ])
            else:
                lines.extend(["  暂无财务数据", ""])
            
            # 评分详情
            lines.extend([
                "【评分详情】",
                f"基本面评分: {format_number(scoring.get('basic_score', 0), 1)}/10.0",
                f"技术面评分: {format_number(scoring.get('tech_score', 0), 1)}/10.0",
                f"情绪面评分: {format_number(scoring.get('market_score', 0), 1)}/10.0",
                f"财务面评分: {format_number(scoring.get('financial_score', 0), 1)}/10.0",  # 新增财务评分
                f"综合评分: {format_number(scoring.get('overall_score', 0), 1)}/10.0",
                "",
                "【操作建议】",
                f"建议操作: {recommendation.get('recommendation', 'N/A')}",
                f"建议理由: {recommendation.get('reason', 'N/A')}",
                "="*60,
            ])
            return "\n".join(str(line) for line in lines if line is not None)
    
    def format_industry_info(self, industry_info, symbol, output_format='text'):
        """格式化行业分类信息"""
        if output_format == 'json':
            return json.dumps(industry_info, ensure_ascii=False, indent=2)
        elif output_format == 'csv':
            df = pd.DataFrame([industry_info])
            return df.to_csv(index=False)
        else:  # text format
            lines = [
                f"【{symbol} 行业分类】",
                f"股票代码: {industry_info.get('code', 'N/A')}",
                f"行业名称: {industry_info.get('industry', 'N/A')}",
                f"行业代码: {industry_info.get('industry_code', 'N/A')}",
                f"分类标准: {industry_info.get('classification', 'N/A')}",
                f"更新日期: {industry_info.get('update_date', 'N/A')}"
            ]
            return "\n".join(lines)
    
    def format_index_constituents(self, stocks_df, index_name, output_format='text'):
        """格式化指数成分股信息"""
        if output_format == 'json':
            return stocks_df.to_json(orient='records', ensure_ascii=False, indent=2)
        elif output_format == 'csv':
            return stocks_df.to_csv(index=False)
        else:  # text format
            lines = [
                f"【{index_name}成分股列表】",
                f"成分股总数: {len(stocks_df)}",
            ]
            # 显示前10只成分股
            for idx, (_, row) in enumerate(stocks_df.head(10).iterrows()):
                lines.append(f"{row['日期']} {row['证券代码']} {row['证券名称']}")
            
            if len(stocks_df) > 10:
                lines.append(f"... 还有 {len(stocks_df) - 10} 只成分股")
            
            return "\n".join(lines)


def get_default_formatter():
    """获取默认格式化器"""
    return OutputFormatter()