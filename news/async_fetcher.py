"""
异步新闻获取器
使用 asyncio 和 aiohttp 实现高性能并发请求
"""
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from bs4 import BeautifulSoup
from logger import get_logger
from config import get_config
from retry import retry_on_failure, error_handler

class AsyncNewsFetcher:
    """异步新闻获取器"""

    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """上下文管理器入口"""
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=10)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers=headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.session:
            await self.session.close()

    @retry_on_failure(max_attempts=3, delay=1.0)
    async def fetch_url(self, url: str, source: str = "unknown") -> str:
        """获取URL内容"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"HTTP {response.status}"
                    )
        except Exception as e:
            error_handler.record_error(source, e)
            raise

    async def fetch_deep_content(self, url: str) -> str:
        """深度获取文章内容"""
        try:
            html = await self.fetch_url(url, "deep_content")
            soup = BeautifulSoup(html, 'html.parser')

            # 移除不需要的标签
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            # 提取文本
            text = soup.get_text(separator=' ', strip=True)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text[:self.config.deep_fetch_max_chars]
        except Exception as e:
            self.logger.warning(f"深度获取失败 {url}: {e}")
            return ""

    # ========== 数据源获取器 ==========

    async def fetch_hackernews(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 Hacker News"""
        items = []
        page = 1

        while len(items) < limit and page <= 3:
            url = f"https://news.ycombinator.com/news?p={page}"
            try:
                html = await self.fetch_url(url, "Hacker News")
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.select('.athing')

                for row in rows:
                    if len(items) >= limit:
                        break

                    try:
                        id_ = row.get('id')
                        title_line = row.select_one('.titleline a')
                        if not title_line:
                            continue

                        title = title_line.get_text()
                        link = title_line.get('href', '')

                        # 获取分数
                        score_span = soup.select_one(f'#score_{id_}')
                        score = score_span.get_text() if score_span else "0 points"

                        # 获取时间
                        age_span = soup.select_one(f'.age a[href="item?id={id_}"]')
                        time_str = age_span.get_text() if age_span else ""

                        if link.startswith('item?id='):
                            link = f"https://news.ycombinator.com/{link}"

                        items.append({
                            "source": "Hacker News",
                            "title": title,
                            "url": link,
                            "heat": score,
                            "time": time_str
                        })
                    except Exception:
                        continue

                page += 1
                await asyncio.sleep(0.5)

            except Exception as e:
                self.logger.error(f"HN 第 {page} 页获取失败: {e}")
                break

        return self._filter_items(items, keyword)

    async def fetch_github(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 GitHub Trending"""
        try:
            html = await self.fetch_url("https://github.com/trending", "GitHub Trending")
            soup = BeautifulSoup(html, 'html.parser')
            items = []

            for article in soup.select('article.Box-row'):
                try:
                    h2 = article.select_one('h2 a')
                    if not h2:
                        continue

                    title = h2.get_text(strip=True).replace('\n', '').replace(' ', '')
                    link = "https://github.com" + h2['href']

                    desc = article.select_one('p')
                    desc_text = desc.get_text(strip=True) if desc else ""

                    stars_tag = article.select_one('a[href$="/stargazers"]')
                    stars = stars_tag.get_text(strip=True) if stars_tag else ""

                    items.append({
                        "source": "GitHub Trending",
                        "title": f"{title} - {desc_text}",
                        "url": link,
                        "heat": f"{stars} stars",
                        "time": "Today"
                    })
                except Exception:
                    continue

            return self._filter_items(items[:limit], keyword)
        except Exception as e:
            self.logger.error(f"GitHub Trending 获取失败: {e}")
            return []

    async def fetch_weibo(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取微博热搜"""
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://weibo.com/"
        }

        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    self.logger.warning(f"微博 API 返回状态码: {response.status}")
                    return []

                data = await response.json()

                # 检查响应结构
                if not isinstance(data, dict):
                    self.logger.error(f"微博 API 返回格式错误: {type(data)}")
                    return []

                if data.get('ok') != 1:
                    self.logger.error(f"微博 API 返回错误: {data}")
                    return []

                items = data.get('data', {}).get('realtime', [])

                if not items:
                    self.logger.warning("微博热搜列表为空")
                    return []

                all_items = []
                for item in items[:limit]:
                    try:
                        # 优先使用 note，其次使用 word
                        title = item.get('note', '') or item.get('word', '')
                        if not title:
                            continue

                        heat = item.get('num', 0)
                        rank = item.get('rank', 0)

                        # 构建搜索 URL
                        from urllib.parse import quote
                        full_url = f"https://s.weibo.com/weibo?q={quote(title)}&Refer=top"

                        all_items.append({
                            "source": "Weibo Hot Search",
                            "title": title,
                            "url": full_url,
                            "heat": f"{heat:,}" if heat else "热度未知",
                            "time": "实时"
                        })
                    except Exception as e:
                        self.logger.debug(f"处理单条微博热搜失败: {e}")
                        continue

                self.logger.info(f"微博热搜获取成功: {len(all_items)} 条")
                return self._filter_items(all_items, keyword)

        except Exception as e:
            self.logger.error(f"微博热搜获取失败: {e}")
            return []

    async def fetch_36kr(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 36Kr 快讯"""
        try:
            html = await self.fetch_url("https://36kr.com/newsflashes", "36Kr")
            soup = BeautifulSoup(html, 'html.parser')
            items = []

            for item in soup.select('.newsflash-item')[:limit]:
                try:
                    title_elem = item.select_one('.item-title')
                    time_elem = item.select_one('.time')

                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    href = title_elem.get('href', '')
                    time_str = time_elem.get_text(strip=True) if time_elem else ""

                    items.append({
                        "source": "36Kr",
                        "title": title,
                        "url": f"https://36kr.com{href}" if not href.startswith('http') else href,
                        "time": time_str,
                        "heat": ""
                    })
                except Exception:
                    continue

            return self._filter_items(items, keyword)
        except Exception as e:
            self.logger.error(f"36Kr 获取失败: {e}")
            return []

    async def fetch_v2ex(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 V2EX 热门话题"""
        try:
            async with self.session.get("https://www.v2ex.com/api/topics/hot.json") as response:
                data = await response.json()
                items = []

                for t in data[:limit]:
                    items.append({
                        "source": "V2EX",
                        "title": t['title'],
                        "url": t['url'],
                        "heat": f"{t.get('replies', 0)} replies",
                        "time": "Hot"
                    })

                return self._filter_items(items, keyword)
        except Exception as e:
            self.logger.error(f"V2EX 获取失败: {e}")
            return []

    async def fetch_tencent(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取腾讯新闻"""
        url = "https://i.news.qq.com/web_backend/v2/getTagInfo?tagId=aEWqxLtdgmQ%3D"
        try:
            async with self.session.get(url, headers={"Referer": "https://news.qq.com/"}) as response:
                data = await response.json()
                items = []

                for news in data['data']['tabs'][0]['articleList'][:limit]:
                    items.append({
                        "source": "Tencent News",
                        "title": news['title'],
                        "url": news.get('url') or news.get('link_info', {}).get('url', ''),
                        "time": news.get('pub_time', '') or news.get('publish_time', '')
                    })

                return self._filter_items(items, keyword)
        except Exception as e:
            self.logger.error(f"腾讯新闻获取失败: {e}")
            return []

    async def fetch_wallstreetcn(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取华尔街见闻"""
        url = "https://api-one.wallstcn.com/apiv1/content/information-flow?channel=global-channel&accept=article&limit=30"
        try:
            async with self.session.get(url) as response:
                data = await response.json()
                items = []

                for item in data['data']['items'][:limit]:
                    res = item.get('resource')
                    if res and (res.get('title') or res.get('content_short')):
                        ts = res.get('display_time', 0)
                        time_str = datetime.fromtimestamp(ts).strftime('%H:%M') if ts else ""

                        items.append({
                            "source": "Wall Street CN",
                            "title": res.get('title') or res.get('content_short'),
                            "url": res.get('uri', ''),
                            "time": time_str
                        })

                return self._filter_items(items, keyword)
        except Exception as e:
            self.logger.error(f"华尔街见闻获取失败: {e}")
            return []

    async def fetch_producthunt(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 Product Hunt"""
        try:
            html = await self.fetch_url("https://www.producthunt.com/feed", "Product Hunt")
            soup = BeautifulSoup(html, 'xml')

            if not soup.find('item'):
                soup = BeautifulSoup(html, 'html.parser')

            items = []
            for entry in soup.find_all(['item', 'entry'])[:limit]:
                title = entry.find('title').get_text(strip=True)
                link_tag = entry.find('link')
                url = link_tag.get('href') or link_tag.get_text(strip=True) if link_tag else ""

                items.append({
                    "source": "Product Hunt",
                    "title": title,
                    "url": url,
                    "time": "",
                    "heat": "Top Product"
                })

            return self._filter_items(items, keyword)
        except Exception as e:
            self.logger.error(f"Product Hunt 获取失败: {e}")
            return []

    # ========== 新增数据源 ==========

    async def fetch_reddit(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 Reddit /r/technology 热门"""
        try:
            async with self.session.get("https://www.reddit.com/r/technology/hot.json?limit=50") as response:
                data = await response.json()
                items = []

                for post in data['data']['children'][:limit]:
                    post_data = post['data']
                    items.append({
                        "source": "Reddit /r/technology",
                        "title": post_data['title'],
                        "url": f"https://reddit.com{post_data['permalink']}",
                        "heat": f"{post_data.get('score', 0)} upvotes",
                        "time": f"{post_data.get('num_comments', 0)} comments"
                    })

                return self._filter_items(items, keyword)
        except Exception as e:
            self.logger.error(f"Reddit 获取失败: {e}")
            return []

    async def fetch_techcrunch(self, limit: int = 10, keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取 TechCrunch 最新文章"""
        try:
            html = await self.fetch_url("https://techcrunch.com", "TechCrunch")
            soup = BeautifulSoup(html, 'html.parser')
            items = []

            for post in soup.select('article.post-block')[:limit]:
                title_elem = post.select_one('.post-block__title__link')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                url = title_elem.get('href', '')

                items.append({
                    "source": "TechCrunch",
                    "title": title,
                    "url": url,
                    "time": "",
                    "heat": ""
                })

            return self._filter_items(items, keyword)
        except Exception as e:
            self.logger.error(f"TechCrunch 获取失败: {e}")
            return []

    # ========== 辅助方法 ==========

    def _filter_items(self, items: List[Dict[str, Any]], keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        """过滤项目"""
        if not keyword:
            return items

        import re
        keywords = [k.strip() for k in keyword.split(',') if k.strip()]
        pattern = '|'.join([r'\b' + re.escape(k) + r'\b' for k in keywords])
        regex = re.compile(pattern, re.IGNORECASE)

        return [item for item in items if regex.search(item.get('title', ''))]

    async def fetch_all_sources(
        self,
        sources: List[str],
        limit: int = 10,
        keyword: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """并发获取所有数据源"""
        source_map = {
            'hackernews': self.fetch_hackernews,
            'github': self.fetch_github,
            'weibo': self.fetch_weibo,
            '36kr': self.fetch_36kr,
            'v2ex': self.fetch_v2ex,
            'tencent': self.fetch_tencent,
            'wallstreetcn': self.fetch_wallstreetcn,
            'producthunt': self.fetch_producthunt,
            'reddit': self.fetch_reddit,
            'techcrunch': self.fetch_techcrunch,
        }

        tasks = []
        for source in sources:
            if source in source_map:
                tasks.append(source_map[source](limit, keyword))

        if not tasks:
            return []

        # 并发执行所有任务
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 合并结果
        all_items = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"任务失败: {result}")
                continue
            if isinstance(result, list):
                all_items.extend(result)

        return all_items

    async def enrich_with_content(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """深度获取文章内容"""
        self.logger.info(f"开始深度获取 {len(items)} 篇文章内容...")

        tasks = [self.fetch_deep_content(item['url']) for item in items]
        contents = await asyncio.gather(*tasks)

        for item, content in zip(items, contents):
            if content:
                item['content'] = content

        return items


async def fetch_news_async(
    sources: List[str],
    limit: int = 10,
    keyword: Optional[str] = None,
    deep: bool = False
) -> List[Dict[str, Any]]:
    """异步获取新闻的便捷函数"""
    async with AsyncNewsFetcher() as fetcher:
        items = await fetcher.fetch_all_sources(sources, limit, keyword)

        if deep and items:
            items = await fetcher.enrich_with_content(items)

        return items
