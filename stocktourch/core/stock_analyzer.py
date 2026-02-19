"""
股票研究技能主分析器
整合项目中现有的数据处理工具，实现股票分析功能
"""
import baostock as bs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import sys
import warnings
import time
from pathlib import Path

# 导入自定义模块
from utils.cache_manager import get_default_cache_manager
from utils import *
from utils.config import get_default_config
from core.financial_analyzer import get_default_financial_analyzer

warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class StockAnalyzer:
    """股票分析器主类"""
    
    def __init__(self, cache_enabled=True, cache_ttl_hours=24):
        """初始化分析器"""
        self.current_date = get_current_date()
        self.cache_manager = get_default_cache_manager()
        # 如果需要特定配置，可以创建新的CacheManager实例
        if cache_enabled != self.cache_manager.cache_enabled or cache_ttl_hours != self.cache_manager.cache_ttl_hours:
            from utils.cache_manager import CacheManager
            self.cache_manager = CacheManager(cache_enabled, cache_ttl_hours)
        
        # 获取配置
        self.config = get_default_config()
        
        # 初始化财务分析器
        self.financial_analyzer = get_default_financial_analyzer()
        
        # 登录baostock
        bs.login()
        
    def __del__(self):
        """析构函数，登出baostock"""
        try:
            bs.logout()
        except:
            pass
        
    def get_cached_data(self, cache_key):
        """获取缓存数据"""
        return self.cache_manager.get_cached_data(cache_key)
    
    def set_cached_data(self, cache_key, data):
        """设置缓存数据"""
        self.cache_manager.set_cached_data(cache_key, data)
        
    def get_stock_info(self, symbol):
        """获取股票基本信息"""
        try:
            # 检查缓存
            cache_key = f"stock_info_{symbol}_{datetime.now().date()}"
            cached_data = self.get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                # A股代码格式化
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"  # 上海证券交易所
                elif symbol.startswith(('00', '30', '15', '16', '18')):
                    code = f"sz.{symbol}"  # 深圳证券交易所
                else:
                    code = f"sh.{symbol}"  # 默认上海
            else:
                # 已经是格式化的代码
                if '.' not in symbol:
                    # 如果没有点号，可能是未格式化的代码
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    elif symbol.startswith(('00', '30', '15', '16', '18')):
                        code = f"sz.{symbol[:6]}"
                    else:
                        code = f"sh.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 获取股票当日K线数据（用于获取最新价格）
            rs = bs.query_history_k_data_plus(
                code,
                "date,code,open,high,low,close,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                start_date=datetime.now().strftime('%Y-%m-%d'),
                end_date=datetime.now().strftime('%Y-%m-%d'),
                frequency="d",
                adjustflag="3"
            )
            
            if rs.error_code != '0':
                print(f"数据获取失败：获取股票数据失败，错误码: {rs.error_code}")
                return None
            
            data_list = []
            while (rs.error_code == '0') & (rs.next()):
                data_list.append(rs.get_row_data())
            
            if len(data_list) == 0:
                # 如果当天没有数据，获取最近一天的数据
                yesterday = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                rs = bs.query_history_k_data_plus(
                    code,
                    "date,code,open,high,low,close,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                    start_date=yesterday,
                    end_date=datetime.now().strftime('%Y-%m-%d'),
                    frequency="d",
                    adjustflag="3"
                )
                
                while (rs.error_code == '0') & (rs.next()):
                    data_list.append(rs.get_row_data())
            
            if len(data_list) > 0:
                # 获取最新数据
                latest_data = data_list[-1]
                result = {
                    'code': latest_data[1],  # code
                    'name': self.get_stock_name(code),  # 获取股票名称
                    'price': float(latest_data[5]) if latest_data[5] != '' else 0,  # close
                    'change': float(latest_data[11]) if latest_data[11] != '' else 0,  # pctChg
                    'change_amount': float(latest_data[5]) - float(latest_data[2]) if latest_data[5] != '' and latest_data[2] != '' else 0,  # close - open
                    'volume': int(float(latest_data[6])) if latest_data[6] != '' else 0,  # volume
                    'amount': float(latest_data[7]) if latest_data[7] != '' else 0,  # amount
                    'high': float(latest_data[3]) if latest_data[3] != '' else 0,  # high
                    'low': float(latest_data[4]) if latest_data[4] != '' else 0,  # low
                    'open': float(latest_data[2]) if latest_data[2] != '' else 0,  # open
                    'close_yesterday': float(latest_data[5]) - float(latest_data[11])/100*float(latest_data[5])/(1+float(latest_data[11])/100) if latest_data[5] != '' and latest_data[11] != '' else 0,
                    'turnover_rate': float(latest_data[9]) if latest_data[9] != '' else 0,  # turn
                    'pe': float(latest_data[12]) if latest_data[12] != '' else 0,  # peTTM
                    'pb': float(latest_data[13]) if latest_data[13] != '' else 0,  # pbMRQ
                }
                
                # 缓存数据
                self.set_cached_data(cache_key, result)
                
                return result
            else:
                print(f"数据获取失败：未找到股票 {code} 的数据")
                return None
                    
        except Exception as e:
            print(f"获取股票信息时出错: {e}")
            return None
    
    def get_stock_name(self, code):
        """获取股票名称"""
        try:
            rs = bs.query_stock_basic(code=code)
            if rs.error_code == '0':
                data = rs.get_row_data()
                if len(data) > 1:
                    return data[1]  # 返回股票名称
            return code  # 如果获取失败，返回代码
        except:
            return code
    
    def get_stock_industry(self, symbol):
        """获取股票行业分类信息"""
        try:
            # 检查缓存
            cache_key = f"industry_{symbol}_{self.current_date}"
            cached_data = self.get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
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
            
            # 查询股票行业分类信息
            rs = bs.query_stock_industry(code=code, date=self.current_date)
            industry_data = {}
            if rs.error_code == '0':
                industry_list = []
                while (rs.error_code == '0') & (rs.next()):
                    industry_list.append(rs.get_row_data())
                
                if len(industry_list) > 0:
                    # 获取最新的行业信息 - 根据实际数据结构调整索引
                    latest_industry = industry_list[-1]  # 通常是最新的一条记录
                    industry_data = {
                        "code": latest_industry[1],        # 股票代码在第2列 (索引1)
                        "industry": latest_industry[3],    # 行业名称在第4列 (索引3) 
                        "industry_code": latest_industry[2],  # 行业代码在第3列 (索引2)
                        "classification": latest_industry[4], # 分类标准在第5列 (索引4)
                        "update_date": latest_industry[0]  # 更新日期在第1列 (索引0)
                    }
                    
                    # 缓存数据
                    self.set_cached_data(cache_key, industry_data)
                    return industry_data
            
            # 如果没有找到行业信息，返回基本信息作为备选
            stock_info = self.get_stock_info(symbol)
            if stock_info:
                industry_data = {
                    "code": code,
                    "industry": stock_info.get('name', 'Unknown'),  # 如果没有具体行业，使用股票名称
                    "industry_code": "N/A",
                    "classification": "Unknown",  # 确保始终有此字段
                    "update_date": self.current_date
                }
                self.set_cached_data(cache_key, industry_data)
                return industry_data
            
            return None
        except Exception as e:
            print(f"获取行业分类失败: {e}")
            return None
    
    def get_financial_data(self, symbol):
        """获取股票财务数据"""
        try:
            # 检查缓存
            cache_key = f"financial_data_{symbol}_{self.current_date}"
            cached_data = self.get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            from datetime import datetime
            current_year = datetime.now().year
            current_quarter = (datetime.now().month - 1) // 3 + 1
            
            # 按优先级尝试获取最新财务数据
            # 按年份倒序，季度倒序的顺序尝试
            years_quarters = []
            for year in range(current_year, current_year - 3, -1):  # 尝试最近3年的数据
                quarters_to_check = 4 if year < current_year else current_quarter
                for quarter in range(quarters_to_check, 0, -1):
                    years_quarters.append((year, quarter))
            
            # 获取各项财务数据
            balance_sheet = None
            cash_flow = None
            profit_statement = None
            operation_data = None
            growth_data = None
            dupont_data = None
            
            # 尝试获取资产负债表数据
            for year, quarter in years_quarters:
                balance_sheet = self.financial_analyzer.get_balance_sheet(symbol, year=year, quarter=quarter)
                if balance_sheet is not None and not balance_sheet.empty:
                    break
            
            # 尝试获取利润表数据
            for year, quarter in years_quarters:
                profit_statement = self.financial_analyzer.get_profit_statement(symbol, year=year, quarter=quarter)
                if profit_statement is not None and not profit_statement.empty:
                    break
            
            # 尝试获取其他数据
            for year, quarter in years_quarters[:5]:  # 只尝试前5个
                cash_flow = self.financial_analyzer.get_cash_flow(symbol, year=year, quarter=quarter)
                if cash_flow is not None and not cash_flow.empty:
                    break
            
            for year, quarter in years_quarters[:5]:
                operation_data = self.financial_analyzer.get_operation_analysis(symbol, year=year, quarter=quarter)
                if operation_data is not None and not operation_data.empty:
                    break
            
            for year, quarter in years_quarters[:5]:
                growth_data = self.financial_analyzer.get_growth_analysis(symbol, year=year, quarter=quarter)
                if growth_data is not None and not growth_data.empty:
                    break
            
            for year, quarter in years_quarters[:5]:
                dupont_data = self.financial_analyzer.get_dupont_analysis(symbol, year=year, quarter=quarter)
                if dupont_data is not None and not dupont_data.empty:
                    break
            
            # 整合财务数据
            financial_data = {
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow,
                'profit_statement': profit_statement,
                'operation_data': operation_data,
                'growth_data': growth_data,
                'dupont_data': dupont_data
            }
            
            # 缓存数据
            self.set_cached_data(cache_key, financial_data)
            return financial_data
            
        except Exception as e:
            print(f"获取财务数据失败: {e}")
            return None
    
    def extract_financial_indicators(self, symbol):
        """提取关键财务指标"""
        try:
            financial_data = self.get_financial_data(symbol)
            if not financial_data:
                return None
            
            # 提取关键财务指标
            indicators = {}
            
            # 从资产负债表提取数据
            if financial_data['balance_sheet'] is not None and not financial_data['balance_sheet'].empty:
                bs_latest = financial_data['balance_sheet'].iloc[0]  # 最新数据
                # 使用正确的字段名（根据baostock实际返回的字段）
                # 字段: ['code', 'pubDate', 'statDate', 'currentRatio', 'quickRatio', 'cashRatio', 'YOYLiability', 'liabilityToAsset', 'assetToEquity']
                current_ratio = pd.to_numeric(bs_latest.get('currentRatio', 0), errors='coerce')  # 流动比率
                quick_ratio = pd.to_numeric(bs_latest.get('quickRatio', 0), errors='coerce')  # 速动比率
                liability_to_asset = pd.to_numeric(bs_latest.get('liabilityToAsset', 0), errors='coerce')  # 资产负债率
                
                indicators['debt_to_asset_ratio'] = liability_to_asset * 100  # 资产负债率
                indicators['current_ratio'] = current_ratio  # 流动比率
                indicators['quick_ratio'] = quick_ratio  # 速动比率
            
            # 从利润表提取数据
            if financial_data['profit_statement'] is not None and not financial_data['profit_statement'].empty:
                ps_latest = financial_data['profit_statement'].iloc[0]  # 最新数据
                # 使用正确的字段名（根据baostock实际返回的字段）
                # 字段: ['code', 'pubDate', 'statDate', 'roeAvg', 'npMargin', 'gpMargin', 'netProfit', 'epsTTM', 'MBRevenue', 'totalShare', 'liqaShare']
                net_profit = pd.to_numeric(ps_latest.get('netProfit', 0), errors='coerce')
                operating_income = pd.to_numeric(ps_latest.get('MBRevenue', 0), errors='coerce')  # 主营业务收入
                roe_avg = pd.to_numeric(ps_latest.get('roeAvg', 0), errors='coerce')  # 平均净资产收益率
                np_margin = pd.to_numeric(ps_latest.get('npMargin', 0), errors='coerce')  # 净利率
                gp_margin = pd.to_numeric(ps_latest.get('gpMargin', 0), errors='coerce')  # 毛利率
                
                indicators['gross_margin'] = gp_margin * 100  # 销售毛利率
                indicators['net_margin'] = np_margin * 100  # 销售净利率
                indicators['roe'] = roe_avg * 100  # 净资产收益率
                # ROA通常在财务数据中不会直接提供，这里暂时使用0，或者可以用其他方法计算
                indicators['roa'] = 0  # 总资产报酬率（实际ROA需要资产总额，baostock的利润表中未直接提供）
            
            # 从运营能力数据提取
            if financial_data['operation_data'] is not None and not financial_data['operation_data'].empty:
                op_latest = financial_data['operation_data'].iloc[0]  # 最新数据
                # 使用正确的字段名（根据baostock实际返回的字段）
                # 字段: ['code', 'pubDate', 'statDate', 'NRTurnRatio', 'NRTurnDays', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio', 'AssetTurnRatio']
                nr_turn_ratio = pd.to_numeric(op_latest.get('NRTurnRatio', 0), errors='coerce')  # 营业收入周转率
                inv_turn_ratio = pd.to_numeric(op_latest.get('INVTurnRatio', 0), errors='coerce')  # 存货周转率
                asset_turn_ratio = pd.to_numeric(op_latest.get('AssetTurnRatio', 0), errors='coerce')  # 总资产周转率
                
                indicators['receivables_turnover'] = nr_turn_ratio  # 应收账款周转率（使用营业收入周转率近似）
                indicators['inventory_turnover'] = inv_turn_ratio  # 存货周转率
                indicators['total_assets_turnover'] = asset_turn_ratio  # 总资产周转率
            
            # 从成长能力数据提取
            if financial_data['growth_data'] is not None and not financial_data['growth_data'].empty:
                gr_latest = financial_data['growth_data'].iloc[0]  # 最新数据
                # 使用正确的字段名（根据baostock实际返回的字段）
                # 字段: ['code', 'pubDate', 'statDate', 'YOYEquity', 'YOYAsset', 'YOYNI', 'YOYEPSBasic', 'YOYPNI']
                yoy_net_profit = pd.to_numeric(gr_latest.get('YOYPNI', 0), errors='coerce')  # 净利润同比增长率
                yoy_operating_revenue = pd.to_numeric(gr_latest.get('YOYNI', 0), errors='coerce')  # 营业收入同比增长率（使用YOYNI近似）
                yoy_total_assets = pd.to_numeric(gr_latest.get('YOYAsset', 0), errors='coerce')  # 总资产同比增长率
                
                indicators['net_profit_growth'] = yoy_net_profit * 100  # 净利润增长率
                indicators['operating_income_growth'] = yoy_operating_revenue * 100  # 营业收入增长率
                indicators['total_assets_growth'] = yoy_total_assets * 100  # 总资产增长率
            
            # 从杜邦分析数据提取
            if financial_data['dupont_data'] is not None and not financial_data['dupont_data'].empty:
                dp_latest = financial_data['dupont_data'].iloc[0]  # 最新数据
                # 使用正确的字段名（根据baostock实际返回的字段）
                # 字段: ['code', 'pubDate', 'statDate', 'dupontROE', 'dupontAssetStoEquity', 'dupontAssetTurn', 'dupontPnitoni', 'dupontNitogr', 'dupontTaxBurden', 'dupontIntburden', 'dupontEbittogr']
                dupont_roe = pd.to_numeric(dp_latest.get('dupontROE', 0), errors='coerce')  # 杜邦ROE
                dupont_asset_turn = pd.to_numeric(dp_latest.get('dupontAssetTurn', 0), errors='coerce')  # 总资产周转率
                dupont_pni_to_ni = pd.to_numeric(dp_latest.get('dupontPnitoni', 0), errors='coerce')  # 净利润率
                
                indicators['dupont_roe'] = dupont_roe
                # ROA可以通过总资产周转率乘以销售净利率计算得到
                roa_from_dupont = dupont_asset_turn * dupont_pni_to_ni
                indicators['roa'] = roa_from_dupont * 100  # 转换为百分比
                
            return indicators
        except Exception as e:
            print(f"提取财务指标失败: {e}")
            return None
    
    def get_hs300_stocks(self):
        """获取沪深300成分股"""
        try:
            rs = bs.query_hs300_stocks(date=self.current_date)
            if rs.error_code == '0':
                data_list = []
                while (rs.error_code == '0') & (rs.next()):
                    data_list.append(rs.get_row_data())
                
                if len(data_list) > 0:
                    # 转换为DataFrame
                    import pandas as pd
                    df = pd.DataFrame(data_list, columns=['日期', '证券代码', '证券名称'])
                    return df
            return None
        except:
            return None
    
    def get_sz50_stocks(self):
        """获取上证50成分股"""
        try:
            rs = bs.query_sz50_stocks(date=self.current_date)
            if rs.error_code == '0':
                data_list = []
                while (rs.error_code == '0') & (rs.next()):
                    data_list.append(rs.get_row_data())
                
                if len(data_list) > 0:
                    # 转换为DataFrame
                    import pandas as pd
                    df = pd.DataFrame(data_list, columns=['日期', '证券代码', '证券名称'])
                    return df
            return None
        except:
            return None
    
    def get_zz500_stocks(self):
        """获取中证500成分股"""
        try:
            rs = bs.query_zz500_stocks(date=self.current_date)
            if rs.error_code == '0':
                data_list = []
                while (rs.error_code == '0') & (rs.next()):
                    data_list.append(rs.get_row_data())
                
                if len(data_list) > 0:
                    # 转换为DataFrame
                    import pandas as pd
                    df = pd.DataFrame(data_list, columns=['日期', '证券代码', '证券名称'])
                    return df
            return None
        except:
            return None
    
    def get_technical_indicators(self, symbol, period='120'):
        """计算技术指标"""
        try:
            # 检查缓存
            cache_key = f"tech_indicators_{symbol}_{period}_{datetime.now().date()}"
            cached_data = self.get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # 格式化股票代码为baostock格式
            if symbol.isdigit() and len(symbol) == 6:
                if symbol.startswith('6'):
                    code = f"sh.{symbol}"
                elif symbol.startswith(('00', '30', '15', '16', '18')):
                    code = f"sz.{symbol}"
                else:
                    code = f"sh.{symbol}"
            else:
                if '.' not in symbol:
                    if symbol.startswith('6'):
                        code = f"sh.{symbol[:6]}"
                    elif symbol.startswith(('00', '30', '15', '16', '18')):
                        code = f"sz.{symbol[:6]}"
                    else:
                        code = f"sh.{symbol[:6]}"
                else:
                    code = symbol.lower()
            
            # 获取历史K线数据
            start_date = (datetime.now() - timedelta(days=int(period)*2)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            rs = bs.query_history_k_data_plus(
                code,
                "date,open,high,low,close,volume,amount",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="3"
            )
            
            data_list = []
            while (rs.error_code == '0') & (rs.next()):
                data_list.append(rs.get_row_data())
            
            if len(data_list) == 0:
                print(f"数据获取失败：未获取到股票 {code} 的历史数据")
                return None
            
            # 转换为DataFrame
            df = pd.DataFrame(data_list, columns=["date", "open", "high", "low", "close", "volume", "amount"])
            
            # 数据类型转换
            df["open"] = pd.to_numeric(df["open"], errors='coerce')
            df["high"] = pd.to_numeric(df["high"], errors='coerce')
            df["low"] = pd.to_numeric(df["low"], errors='coerce')
            df["close"] = pd.to_numeric(df["close"], errors='coerce')
            df["volume"] = pd.to_numeric(df["volume"], errors='coerce')
            df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
            df["date"] = pd.to_datetime(df["date"])
            
            # 删除包含NaN的行
            df.dropna(inplace=True)
            
            if df.empty:
                print(f"数据获取失败：股票 {code} 的历史数据为空或全部为无效值")
                return None
            
            # 只保留最近period天的数据
            df = df.tail(int(period)).copy()
            df.reset_index(drop=True, inplace=True)
            
            # 设置日期为索引
            df.set_index('date', inplace=True)
            
            # 移动平均线
            df['ma5'] = df['close'].rolling(window=5).mean()
            df['ma10'] = df['close'].rolling(window=10).mean()
            df['ma20'] = df['close'].rolling(window=20).mean()
            df['ma30'] = df['close'].rolling(window=30).mean()
            
            # RSI指标
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD指标
            exp12 = df['close'].ewm(span=12).mean()
            exp26 = df['close'].ewm(span=26).mean()
            df['macd_dif'] = exp12 - exp26
            df['macd_dea'] = df['macd_dif'].ewm(span=9).mean()
            df['macd_bar'] = (df['macd_dif'] - df['macd_dea']) * 2
            
            # 布林带
            df['bb_middle'] = df['close'].rolling(window=20).mean()
            bb_std = df['close'].rolling(window=20).std()
            df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
            df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
            
            # KDJ指标
            low_min = df['low'].rolling(window=9).min()
            high_max = df['high'].rolling(window=9).max()
            df['kd_k'] = 100 * ((df['close'] - low_min) / (high_max - low_min))
            df['kd_d'] = df['kd_k'].rolling(window=3).mean()
            df['kd_j'] = 3 * df['kd_k'] - 2 * df['kd_d']
            
            # 计算支撑位和压力位
            recent_high = df['high'].tail(20).max()
            recent_low = df['low'].tail(20).min()
            
            result = {
                'data': df,
                'support': recent_low,
                'resistance': recent_high,
                'latest_rsi': df['rsi'].iloc[-1] if not pd.isna(df['rsi'].iloc[-1]) else 0,
                'latest_macd': df['macd_dif'].iloc[-1] if not pd.isna(df['macd_dif'].iloc[-1]) else 0,
                'latest_k': df['kd_k'].iloc[-1] if not pd.isna(df['kd_k'].iloc[-1]) else 0,
                'latest_d': df['kd_d'].iloc[-1] if not pd.isna(df['kd_d'].iloc[-1]) else 0,
                'latest_j': df['kd_j'].iloc[-1] if not pd.isna(df['kd_j'].iloc[-1]) else 0,
            }
            
            # 缓存数据
            self.set_cached_data(cache_key, result)
            
            return result
        except Exception as e:
            print(f"计算技术指标时出错: {e}")
            return None
    
    def calculate_scores(self, stock_info, tech_data, symbol=None):
        """计算各项评分"""
        if not tech_data:
            return {'basic_score': 0, 'tech_score': 0, 'market_score': 0, 'financial_score': 0, 'overall_score': 0}
        
        # 基本面评分（简化版）
        basic_score = 0
        if stock_info and 'pe' in stock_info and not pd.isna(stock_info['pe']):
            # 市盈率评分：合理范围10-30
            pe = stock_info['pe']
            if 10 <= pe <= 30:
                basic_score = 8
            elif 5 <= pe < 10 or 30 < pe <= 50:
                basic_score = 6
            elif 0 < pe < 5 or 50 < pe <= 100:
                basic_score = 4
            else:
                basic_score = 2
        
        # 技术面评分
        tech_score = 0
        rsi = tech_data['latest_rsi']
        if 30 <= rsi <= 70:
            tech_score += 4  # RSI处于合理区间
        elif 20 <= rsi < 30 or 70 < rsi <= 80:
            tech_score += 3  # RSI接近超买超卖区
        else:
            tech_score += 2  # RSI超买超卖
        
        # 检查均线排列
        latest_data = tech_data['data'].iloc[-1]
        ma_values = [latest_data['ma5'], latest_data['ma10'], latest_data['ma20']]
        if all(not pd.isna(x) for x in ma_values) and ma_values[0] >= ma_values[1] >= ma_values[2]:
            tech_score += 3  # 多头排列
        elif all(not pd.isna(x) for x in ma_values) and ma_values[0] <= ma_values[1] <= ma_values[2]:
            tech_score += 1  # 空头排列
        else:
            tech_score += 2  # 其他情况
        
        # MACD状态
        macd_dif = tech_data['latest_macd']
        if macd_dif > 0:
            tech_score += 2  # 多头市场
        else:
            tech_score += 1  # 空头市场
        
        # 市场情绪评分（基于价格位置）
        market_score = 0
        current_price = latest_data['close']  # baostock使用'close'而不是'收盘'
        support = tech_data['support']
        resistance = tech_data['resistance']
        
        if support and resistance and resistance != support:
            position = (current_price - support) / (resistance - support)
            if 0.3 <= position <= 0.7:
                market_score = 5  # 在中间位置，中性
            elif position < 0.3:
                market_score = 4  # 接近支撑，偏乐观
            else:
                market_score = 3  # 接近压力，偏悲观
        else:
            market_score = 3  # 默认分数
        
        # 财务面评分
        financial_score = 0
        if symbol:
            financial_indicators = self.extract_financial_indicators(symbol)
            if financial_indicators:
                # 盈利能力评分
                roe_score = 0
                roe = financial_indicators.get('roe', 0)
                if roe > 15:
                    roe_score = 4
                elif roe > 10:
                    roe_score = 3
                elif roe > 5:
                    roe_score = 2
                elif roe > 0:
                    roe_score = 1
                
                # 偿债能力评分
                debt_score = 0
                debt_to_asset = financial_indicators.get('debt_to_asset_ratio', 100)
                if debt_to_asset < 30:
                    debt_score = 4
                elif debt_to_asset < 50:
                    debt_score = 3
                elif debt_to_asset < 70:
                    debt_score = 2
                else:
                    debt_score = 1
                
                # 营运能力评分
                operation_score = 0
                turnover = financial_indicators.get('total_assets_turnover', 0)
                if turnover > 1.5:
                    operation_score = 3
                elif turnover > 1.0:
                    operation_score = 2
                elif turnover > 0.5:
                    operation_score = 1
                
                # 成长能力评分
                growth_score = 0
                profit_growth = financial_indicators.get('net_profit_growth', 0)
                if profit_growth > 20:
                    growth_score = 4
                elif profit_growth > 10:
                    growth_score = 3
                elif profit_growth > 0:
                    growth_score = 2
                elif profit_growth > -10:
                    growth_score = 1
                
                financial_score = (roe_score + debt_score + operation_score + growth_score) / 4 * 2.5  # 调整到10分制
        
        # 综合评分（加权）
        overall_score = basic_score * 0.25 + tech_score * 0.25 + market_score * 0.25 + financial_score * 0.25
        
        return {
            'basic_score': round(basic_score, 1),
            'tech_score': round(tech_score, 1),
            'market_score': round(market_score, 1),
            'financial_score': round(financial_score, 1),
            'overall_score': round(overall_score, 1)
        }
    
    def get_recommendation(self, scores, stock_info, tech_data):
        """生成操作建议"""
        if not tech_data:
            return "数据不足，无法生成建议"
        
        overall_score = scores['overall_score']
        rsi = tech_data['latest_rsi']
        latest_data = tech_data['data'].iloc[-1]
        
        # 确定趋势
        trend = ""
        ma5 = latest_data['ma5'] if 'ma5' in latest_data else None
        ma20 = latest_data['ma20'] if 'ma20' in latest_data else None
        current_price = latest_data['close']  # baostock使用'close'而不是'收盘'
        
        if not pd.isna(ma5) and not pd.isna(ma20):
            if current_price > ma5 > ma20:
                trend = "上升趋势"
            elif current_price < ma5 < ma20:
                trend = "下降趋势"
            else:
                trend = "震荡趋势"
        else:
            trend = "趋势不明"
        
        # 生成建议
        if overall_score >= 7.5:
            recommendation = "买入"
            reason = f"综合评分较高({overall_score}/10)，{trend}，技术面和基本面均表现良好"
        elif 5.5 <= overall_score < 7.5:
            recommendation = "持有"
            reason = f"综合评分中等({overall_score}/10)，{trend}，建议观望"
        elif 3.5 <= overall_score < 5.5:
            recommendation = "谨慎"
            reason = f"综合评分较低({overall_score}/10)，{trend}，存在一定风险"
        else:
            recommendation = "卖出"
            reason = f"综合评分很低({overall_score}/10)，{trend}，建议规避风险"
        
        # RSI提醒
        if rsi > 70:
            reason += "，注意RSI超买风险"
        elif rsi < 30:
            reason += "，注意RSI超卖机会"
        
        return {
            'recommendation': recommendation,
            'reason': reason,
            'trend': trend
        }
    
    def analyze_stock(self, symbol):
        """完整分析一只股票"""
        print(f"正在分析股票: {symbol}")
        
        # 获取股票基本信息
        stock_info = self.get_stock_info(symbol)
        if not stock_info:
            print(f"无法获取股票 {symbol} 的信息")
            return None
        
        # 获取技术指标
        tech_data = self.get_technical_indicators(symbol)
        
        # 计算评分
        scores = self.calculate_scores(stock_info, tech_data, symbol)
        
        # 生成操作建议
        recommendation = self.get_recommendation(scores, stock_info, tech_data)
        
        # 组装结果
        result = {
            'stock_info': stock_info,
            'technical_data': tech_data,
            'financial_data': self.extract_financial_indicators(symbol),  # 添加财务数据
            'scores': scores,
            'recommendation': recommendation
        }
        
        return result
    
    def format_report(self, analysis_result):
        """格式化分析报告"""
        if not analysis_result:
            return "分析失败，未获得有效数据"
        
        stock_info = analysis_result['stock_info']
        tech_data = analysis_result['technical_data']
        financial_data = analysis_result.get('financial_data', {})
        scores = analysis_result['scores']
        recommendation = analysis_result['recommendation']
        
        report = []
        report.append("=" * 60)
        report.append("股票综合分析报告".center(60))
        report.append("=" * 60)
        
        # 基本信息
        report.append(f"【股票信息】")
        report.append(f"股票代码: {stock_info['code']:<15} 股票名称: {stock_info['name']}")
        report.append(f"当前价格: {stock_info['price']:<15} 涨跌幅: {stock_info['change']}%")
        report.append(f"涨跌金额：{stock_info['change_amount']:<15} 成交量：{stock_info['volume'] / 10000:,.2f}万股")
        report.append(f"成交金额: {stock_info['amount']:,.0f}   昨日收盘: {stock_info['close_yesterday']}")
        report.append("")
        
        # 技术分析
        if tech_data:
            latest_data = tech_data['data'].iloc[-1]
            prev_data = tech_data['data'].iloc[-2] if len(tech_data['data']) > 1 else latest_data
            report.append(f"【技术分析】")
            report.append(f"MA5: {latest_data['ma5']:.2f}({'↑' if latest_data['ma5'] > prev_data['ma5'] else '↓'}) | "
                         f"MA10: {latest_data['ma10']:.2f}({'↑' if latest_data['ma10'] > prev_data['ma10'] else '↓'}) | "
                         f"MA20: {latest_data['ma20']:.2f}({'↑' if latest_data['ma20'] > prev_data['ma20'] else '↓'})")
            report.append(f"RSI(14): {tech_data['latest_rsi']:.2f} ({'超买' if tech_data['latest_rsi'] > 70 else '超卖' if tech_data['latest_rsi'] < 30 else '正常'})")
            report.append(f"支撑位: {tech_data['support']:.2f} | 压力位: {tech_data['resistance']:.2f}")
            report.append("")
        
        # 财务分析
        if financial_data:
            report.append(f"【财务分析】")
            report.append(f"盈利能力 - ROE: {financial_data.get('roe', 0):.2f}% | ROA: {financial_data.get('roa', 0):.2f}% | 销售毛利率: {financial_data.get('gross_margin', 0):.2f}% | 销售净利率: {financial_data.get('net_margin', 0):.2f}%")
            report.append(f"偿债能力 - 资产负债率: {financial_data.get('debt_to_asset_ratio', 0):.2f}% | 流动比率: {financial_data.get('current_ratio', 0):.2f} | 速动比率: {financial_data.get('quick_ratio', 0):.2f}")
            report.append(f"营运能力 - 应收账款周转率: {financial_data.get('receivables_turnover', 0):.2f} | 存货周转率: {financial_data.get('inventory_turnover', 0):.2f} | 总资产周转率: {financial_data.get('total_assets_turnover', 0):.2f}")
            report.append(f"成长能力 - 净利润增长率: {financial_data.get('net_profit_growth', 0):.2f}% | 营业收入增长率: {financial_data.get('operating_income_growth', 0):.2f}% | 总资产增长率: {financial_data.get('total_assets_growth', 0):.2f}%")
            report.append("")
        
        # 评分详情
        report.append(f"【评分详情】")
        report.append(f"基本面评分: {scores['basic_score']}/10.0")
        report.append(f"技术面评分: {scores['tech_score']}/10.0")
        report.append(f"情绪面评分: {scores['market_score']}/10.0")
        report.append(f"财务面评分: {scores['financial_score']}/10.0")
        report.append(f"综合评分: {scores['overall_score']}/10.0")
        report.append("")
        
        # 操作建议
        report.append(f"【操作建议】")
        report.append(f"建议操作: {recommendation['recommendation']}")
        report.append(f"建议理由: {recommendation['reason']}")
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def get_sector_ranking(self):
        """获取板块涨跌幅排名"""
        try:
            # 检查缓存
            cache_key = f"sector_ranking_{datetime.now().date()}"
            cached_data = self.get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            print("数据获取失败：baostock不提供板块数据，无法获取板块涨跌幅排名")
            print("提示：您可以使用个股分析功能代替板块分析")
            return None
                
        except Exception as e:
            print(f"获取板块排名时出错: {e}")
            return None
    
    def format_sector_report(self, sector_df):
        """格式化板块分析报告"""
        if sector_df is None or sector_df.empty:
            return "数据获取失败：未能获取到有效的板块数据"
        
        report = []
        report.append("=" * 80)
        report.append("A股各大板块近一年涨跌幅排名".center(80))
        report.append("=" * 80)
        
        report.append("【涨幅前十名】")
        top_10 = sector_df.head(10)
        if top_10.empty:
            report.append("暂无涨幅数据")
        else:
            for idx, row in top_10.iterrows():
                rank = idx + 1
                report.append(f"{rank:2d}. {row['板块名称']:<12} 涨幅: {row['涨跌幅(%)']:>7.2f}% "
                             f"(起点:{row['起始价格']:>7.2f} -> 终点:{row['结束价格']:>7.2f})")
        
        report.append("\n【跌幅前十名】")
        # 只选择跌幅（负值）的板块
        negative_changes = sector_df[sector_df['涨跌幅(%)'] < 0].sort_values('涨跌幅(%)', ascending=True)
        if len(negative_changes) > 0:
            # 如果有负增长的板块，最多取10个跌幅最大的
            bottom_10 = negative_changes.head(10)
            for i, (idx, row) in enumerate(bottom_10.iterrows()):
                rank = i + 1  # 正确的排名
                report.append(f"{rank:2d}. {row['板块名称']:<12} 跌幅: {row['涨跌幅(%)']:>7.2f}% "
                             f"(起点:{row['起始价格']:>7.2f} -> 终点:{row['结束价格']:>7.2f})")
        else:
            # 如果没有负增长的板块，显示跌幅最小的10个（即涨幅最小的）
            smallest_positive = sector_df.sort_values('涨跌幅(%)', ascending=True).head(10)
            if smallest_positive.empty:
                report.append("暂无跌幅数据")
            else:
                for i, (idx, row) in enumerate(smallest_positive.iterrows()):
                    rank = i + 1  # 正确的排名
                    report.append(f"{rank:2d}. {row['板块名称']:<12} 降幅: {row['涨跌幅(%)']:>7.2f}% "
                                 f"(起点:{row['起始价格']:>7.2f} -> 终点:{row['结束价格']:>7.2f})")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    """主函数，用于测试"""
    analyzer = StockAnalyzer()
    
    # 测试分析单只股票
    print("测试分析平安银行(000001)")
    result = analyzer.analyze_stock("000001")
    if result:
        report = analyzer.format_report(result)
        print(report)
    
    print("\n" + "="*60 + "\n")
    
    # 测试板块排名
    print("测试板块涨跌幅排名")
    sector_result = analyzer.get_sector_ranking()
    if sector_result is not None:
        sector_report = analyzer.format_sector_report(sector_result)
        print(sector_report)


if __name__ == "__main__":
    main()