"""
网络爬虫模块
用于获取财经新闻和市场分析数据
"""
import requests
from bs4 import BeautifulSoup
import datetime
import re
from typing import List, Dict, Optional
import time
import random


class MarketNewsCrawler:
    """市场新闻爬虫"""
    
    def __init__(self):
        """初始化爬虫"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # 主要财经网站URL
        self.news_sources = {
            'sina': 'https://finance.sina.com.cn/stock/',
            'eastmoney': 'https://stock.eastmoney.com/',
            'hexun': 'https://stock.hexun.com/',
            '10jqka': 'https://www.10jqka.com.cn/'
        }
    
    def get_market_news(self, source: str = 'sina', limit: int = 10) -> List[Dict]:
        """获取市场新闻"""
        if source not in self.news_sources:
            raise ValueError(f"不支持的数据源: {source}")
        
        url = self.news_sources[source]
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []
            
            if source == 'sina':
                # 新浪财经新闻抓取
                news_elements = soup.select('div.main-content ul li a')[:limit]
                for elem in news_elements:
                    title = elem.get_text(strip=True)
                    link = elem.get('href')
                    if title and link:
                        news_items.append({
                            'title': title,
                            'link': link,
                            'source': 'sina',
                            'timestamp': datetime.datetime.now().isoformat()
                        })
            elif source == 'eastmoney':
                # 东方财富新闻抓取
                news_elements = soup.select('a[title]')[:limit]
                for elem in news_elements:
                    title = elem.get('title', '').strip()
                    link = elem.get('href')
                    if title and link and len(title) > 10:  # 过滤太短的标题
                        if not link.startswith('http'):
                            link = 'https://stock.eastmoney.com' + link
                        news_items.append({
                            'title': title,
                            'link': link,
                            'source': 'eastmoney',
                            'timestamp': datetime.datetime.now().isoformat()
                        })
            
            # 随机延时，避免被封IP
            time.sleep(random.uniform(0.5, 1.5))
            
            return news_items
            
        except Exception as e:
            print(f"获取{source}新闻时出错: {e}")
            return []
    
    def get_latest_market_analysis(self) -> List[Dict]:
        """获取最新的市场分析文章"""
        analysis_articles = []
        
        # 从多个源获取分析文章
        for source in ['sina', 'eastmoney']:
            try:
                articles = self.get_market_news(source=source, limit=5)
                # 过滤包含"分析"、"收评"、"展望"等关键词的文章
                filtered_articles = [
                    article for article in articles 
                    if any(keyword in article['title'] for keyword in ['分析', '收评', '展望', '策略', '观点', '研判'])
                ]
                analysis_articles.extend(filtered_articles)
            except:
                continue
        
        return analysis_articles[:10]  # 返回最多10篇分析文章
    
    def get_policy_news(self) -> List[Dict]:
        """获取政策相关新闻"""
        policy_news = []
        
        # 从多个源获取政策新闻
        for source in ['sina', 'eastmoney']:
            try:
                articles = self.get_market_news(source=source, limit=10)
                # 过滤包含政策相关关键词的文章
                filtered_articles = [
                    article for article in articles 
                    if any(keyword in article['title'] for keyword in ['政策', '监管', '央行', '财政', '国常会', '发改委', '证监会', '银保监会'])
                ]
                policy_news.extend(filtered_articles)
            except:
                continue
        
        return policy_news[:5]  # 返回最多5篇政策新闻
    
    def get_global_market_impact_news(self) -> List[Dict]:
        """获取海外市场影响相关新闻"""
        global_news = []
        
        # 从多个源获取相关新闻
        for source in ['sina', 'eastmoney']:
            try:
                articles = self.get_market_news(source=source, limit=10)
                # 过滤包含海外市场影响关键词的文章
                filtered_articles = [
                    article for article in articles 
                    if any(keyword in article['title'] for keyword in ['美股', '美联储', '加息', '欧股', '港股', '外资', '北向资金', '海外市场'])
                ]
                global_news.extend(filtered_articles)
            except:
                continue
        
        return global_news[:5]  # 返回最多5篇全球市场影响新闻


class MarketDataCrawler:
    """市场数据爬虫"""
    
    def __init__(self):
        """初始化数据爬虫"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_northbound_funds(self) -> Dict:
        """获取北向资金数据（模拟实现，实际需要从专业财经网站获取）"""
        # 这里是模拟数据，实际实现需要从东方财富、同花顺等网站获取
        return {
            'north_money': round(random.uniform(-50, 50), 2),  # 亿元
            'hgt_money': round(random.uniform(-30, 30), 2),    # 沪股通
            'sgt_money': round(random.uniform(-20, 20), 2),    # 深股通
            'update_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_market_sentiment_index(self) -> Dict:
        """获取市场情绪指标（模拟实现）"""
        # 这里是模拟数据，实际需要从专业网站获取恐慌贪婪指数等
        return {
            'fear_greed_index': random.randint(30, 70),  # 恐慌贪婪指数
            'sentiment_level': random.choice(['恐惧', '中性', '贪婪']),
            'volatility': round(random.uniform(15, 35), 2),  # 波动率
            'update_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


def get_default_market_crawler():
    """获取默认的市场爬虫实例"""
    return {
        'news_crawler': MarketNewsCrawler(),
        'data_crawler': MarketDataCrawler()
    }


if __name__ == "__main__":
    # 测试爬虫功能
    crawlers = get_default_market_crawler()
    
    print("测试市场新闻爬虫...")
    news = crawlers['news_crawler'].get_market_news(limit=5)
    for item in news:
        print(f"- {item['title']}")
    
    print("\n测试市场分析文章爬虫...")
    analysis = crawlers['news_crawler'].get_latest_market_analysis()
    for item in analysis[:3]:
        print(f"- {item['title']}")
    
    print("\n测试北向资金数据...")
    funds = crawlers['data_crawler'].get_northbound_funds()
    print(f"北向资金: {funds}")
    
    print("\n测试市场情绪指标...")
    sentiment = crawlers['data_crawler'].get_market_sentiment_index()
    print(f"市场情绪: {sentiment}")