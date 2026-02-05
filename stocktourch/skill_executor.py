"""
股票研究技能执行器
用于响应用户的/stock命令并执行相应的分析功能
"""
import sys
import os
import argparse
from stock_analyzer import StockAnalyzer
from output_formatter import get_default_formatter
from financial_analyzer import get_default_financial_analyzer
from ai_market_analyzer import AIMarketAnalyzer

def execute_skill(args, analyzer=None, output_format='text'):
    """
    执行股票研究技能
    """
    # 如果没有传入analyzer实例，则创建一个新的
    if analyzer is None:
        analyzer = StockAnalyzer()
    
    # 获取格式化器
    formatter = get_default_formatter()
    financial_analyzer = get_default_financial_analyzer()
    
    # 解析命令参数
    if len(args) == 0:
        print("请输入股票代码或名称，例如: /stock 000001")
        return

    command = args[0].lower()

    if command == "ranking":
        # 板块排名分析
        print("正在获取A股各大板块近一年涨跌幅排名...")
        sector_result = analyzer.get_sector_ranking()
        if sector_result is not None:
            sector_report = analyzer.format_sector_report(sector_result)
            print(sector_report)
        else:
            print("未能获取到板块排名数据，请稍后重试。")

    elif command == "fear-greed":
        # 恐慌贪婪指数
        print("数据获取失败：baostock不支持恐慌贪婪指数功能")
        print("提示：该功能需要akshare支持，当前使用baostock作为主要数据源")

    elif len(args) >= 2:
        # 有额外参数的股票分析
        symbol = args[0]
        option = args[1].lower()
        
        # 检查是否是大盘分析
        if symbol.lower() in ["market", "index", "overview"] and option == "report":
            print("正在生成A股市场大盘分析报告...")
            market_analyzer = AIMarketAnalyzer()
            report = market_analyzer.generate_comprehensive_report()
            print(report)
            
            # 保存报告到文件
            filepath = market_analyzer.save_report_to_file(report)
            print(f"\n报告已保存至: {filepath}")
            return
        # 检查是否是指数成分股查询
        elif symbol.lower() in ["hs300", "sz50", "zz500"]:
            index_symbol = symbol.lower()
            if index_symbol == "hs300":
                stocks_df = analyzer.get_hs300_stocks()
                index_name = "沪深300"
            elif index_symbol == "sz50":
                stocks_df = analyzer.get_sz50_stocks()
                index_name = "上证50"
            elif index_symbol == "zz500":
                stocks_df = analyzer.get_zz500_stocks()
                index_name = "中证500"
                
            if stocks_df is not None and not stocks_df.empty:
                formatted_output = formatter.format_index_constituents(stocks_df, index_name, output_format)
                print(formatted_output)
            else:
                print(f"无法获取{index_name}成分股信息")
        else:
            # 正常股票分析
            if option == "info":
                # 获取基本资料
                stock_info = analyzer.get_stock_info(symbol)
                if stock_info:
                    formatted_output = formatter.format_stock_info(stock_info, output_format)
                    print(formatted_output)
                else:
                    print(f"无法获取股票 {symbol} 的基本信息")
            
            elif option == "quote":
                # 获取实时行情
                stock_info = analyzer.get_stock_info(symbol)
                if stock_info:
                    formatted_output = formatter.format_stock_info(stock_info, output_format)
                    print(formatted_output)
                else:
                    print(f"无法获取股票 {symbol} 的行情数据")
            
            elif option == "analysis":
                # 综合分析
                result = analyzer.analyze_stock(symbol)
                if result:
                    formatted_output = formatter.format_comprehensive_report(result, output_format)
                    print(formatted_output)
                else:
                    print(f"无法对股票 {symbol} 进行分析")
            
            elif option in ["technical", "tech"]:
                # 技术分析
                tech_data = analyzer.get_technical_indicators(symbol)
                if tech_data:
                    formatted_output = formatter.format_technical_analysis(tech_data, symbol, output_format)
                    print(formatted_output)
                else:
                    print(f"无法获取股票 {symbol} 的技术指标")
            
            elif option in ["fundamental", "fund"]:
                # 基本面分析
                stock_info = analyzer.get_stock_info(symbol)
                if stock_info:
                    formatted_output = formatter.format_fundamental_analysis(stock_info, output_format)
                    print(formatted_output)
                else:
                    print(f"无法获取股票 {symbol} 的基本面数据")
            
            elif option in ["recommend", "suggest"]:
                # 操作建议
                result = analyzer.analyze_stock(symbol)
                if result:
                    rec = result['recommendation']
                    print(f"【{symbol} 操作建议】")
                    print(f"建议操作: {rec['recommendation']}")
                    print(f"建议理由: {rec['reason']}")
                else:
                    print(f"无法生成股票 {symbol} 的操作建议")
            
            elif option == "sector":
                # 板块分析
                print(f"正在分析板块: {symbol}")
                # 这里可以添加板块分析的具体实现
                print(f"板块分析功能待完善...")
            elif option == "industry":
                # 行业分类分析
                code = symbol
                if code.isdigit() and len(code) == 6:
                    if code.startswith('6'):
                        code = f"sh.{code}"
                    else:
                        code = f"sz.{code}"
                
                industry_info = analyzer.get_stock_industry(code)
                if industry_info:
                    formatted_output = formatter.format_industry_info(industry_info, symbol, output_format)
                    print(formatted_output)
                else:
                    print(f"无法获取股票 {symbol} 的行业分类信息")
            elif option in ["finance", "financial", "财报", "财务"]:
                # 财务数据分析
                print(f"正在获取股票 {symbol} 的财务数据...")
                # 尝试获取财务数据（目前主要是占位符，实际功能将在后续实现）
                balance_sheet = financial_analyzer.get_balance_sheet(symbol)
                if balance_sheet is not None and not balance_sheet.empty:
                    print(f"已获取 {symbol} 的资产负债表数据")
                    print("财务分析功能将在后续版本中完善...")
                else:
                    print(f"暂无 {symbol} 的财务数据或功能尚未完全实现")
            elif option == "cashflow" or option == "现金流量":
                # 现金流量分析
                print(f"正在获取股票 {symbol} 的现金流量表数据...")
                cash_flow = financial_analyzer.get_cash_flow(symbol)
                if cash_flow is not None and not cash_flow.empty:
                    print(f"已获取 {symbol} 的现金流量表数据")
                    print("现金流量分析功能将在后续版本中完善...")
                else:
                    print(f"暂无 {symbol} 的现金流量表数据或功能尚未完全实现")
            elif option == "income" or option == "利润表":
                # 利润表分析
                print(f"正在获取股票 {symbol} 的利润表数据...")
                profit_stmt = financial_analyzer.get_profit_statement(symbol)
                if profit_stmt is not None and not profit_stmt.empty:
                    print(f"已获取 {symbol} 的利润表数据")
                    print("利润表分析功能将在后续版本中完善...")
                else:
                    print(f"暂无 {symbol} 的利润表数据或功能尚未完全实现")
            elif option in ["comprehensive", "compre", "full"]:
                # 综合分析：结合技术数据和网络信息
                print(f"正在进行 {symbol} 的综合分析...")
                print("此功能将结合技术数据和网络信息进行深度分析")
                result = analyzer.analyze_stock(symbol)
                if result:
                    # 生成基本技术分析报告
                    formatted_output = formatter.format_comprehensive_report(result, output_format)
                    print(formatted_output)
                    
                    # 调用AI的内置网络搜索功能来获取相关信息
                    print("\n正在搜索相关网络信息...")
                    print("网络信息将包括公司公告、行业动态、分析师观点等...")
                    
                    # 提示用户AI将执行网络搜索
                    print("\nAI将自动执行以下步骤：")
                    print("1. 获取技术数据（基本信息、技术指标、基本面数据、行业分类等）")
                    print("2. 搜索相关网络信息（公司公告、行业动态、分析师观点等）")
                    print("3. 生成综合投资分析报告")
                    
                    # 执行AI网络搜索 - 这里使用AI内置搜索功能获取与股票相关的网络信息
                    try:
                        # 构建搜索查询
                        stock_name = result['stock_info']['name'] if result['stock_info'] else symbol
                        search_queries = [
                            f"{stock_name} {symbol} 公司公告 最新消息",
                            f"{stock_name} {symbol} 行业动态 发展趋势",
                            f"{stock_name} {symbol} 分析师评级 投资建议",
                            f"{stock_name} {symbol} 新闻报道 市场表现",
                            f"{stock_name} {symbol} 机构调研 持仓变化"
                        ]
                        
                        print(f"\n开始搜索关于 {stock_name}({symbol}) 的相关信息...")
                        
                        # 注意：这里的搜索功能将在AI层面上执行，由AI系统内置的搜索功能完成
                        # 我们在此处提供指导，AI系统将根据这些指令执行搜索
                        for i, query in enumerate(search_queries, 1):
                            print(f"正在准备搜索查询 {i}: {query}")
                        
                        print("\nAI已收到搜索指令，将立即执行网络搜索以获取相关股票信息")
                        print("搜索完成后，AI将结合技术数据和网络信息生成综合分析报告")
                        
                    except Exception as e:
                        print(f"准备网络搜索时出现提示信息: {e}")
                        print("请注意，实际的网络搜索将由AI系统内置功能完成")
                    
                else:
                    print(f"无法对股票 {symbol} 进行综合分析")
            else:
                print(f"未知的选项: {option}")
                print("可用选项: info, quote, analysis, technical, fundamental, recommend, sector, industry, finance, cashflow, income, comprehensive, report")
    
    else:
        # 检查是否是大盘分析
        if args[0].lower() in ["market", "index", "overview"]:
            print("正在生成A股市场大盘分析报告...")
            market_analyzer = AIMarketAnalyzer()
            report = market_analyzer.generate_comprehensive_report()
            print(report)
            
            # 保存报告到文件
            filepath = market_analyzer.save_report_to_file(report)
            print(f"\n报告已保存至: {filepath}")
            return
        # 检查是否是指数成分股查询
        elif args[0].lower() in ["hs300", "sz50", "zz500"]:
            index_symbol = args[0].lower()
            if index_symbol == "hs300":
                stocks_df = analyzer.get_hs300_stocks()
                index_name = "沪深300"
            elif index_symbol == "sz50":
                stocks_df = analyzer.get_sz50_stocks()
                index_name = "上证50"
            elif index_symbol == "zz500":
                stocks_df = analyzer.get_zz500_stocks()
                index_name = "中证500"
                
            if stocks_df is not None and not stocks_df.empty:
                formatted_output = formatter.format_index_constituents(stocks_df, index_name, output_format)
                print(formatted_output)
            else:
                print(f"无法获取{index_name}成分股信息")
        else:
            # 简单股票分析
            symbol = args[0]
            print(f"正在分析股票: {symbol}")
            
            # 执行综合分析
            result = analyzer.analyze_stock(symbol)
            if result:
                formatted_output = formatter.format_comprehensive_report(result, output_format)
                print(formatted_output)
            else:
                print(f"无法对股票 {symbol} 进行分析")


if __name__ == "__main__":
    # 获取命令行参数（跳过脚本名称）
    args = sys.argv[1:]
    execute_skill(args)