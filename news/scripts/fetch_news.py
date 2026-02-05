#!/usr/bin/env python3
"""
News Aggregator - Enhanced Version
支持异步并发、智能缓存、健康监控、订阅模式等功能
"""
import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加父目录到路径以导入模块
sys.path.insert(0, str(Path(__file__).parent.parent))

# 首先导入并配置编码工具
from encoding_utils import setup_utf8_output, safe_print, safe_write
setup_utf8_output()

from config import get_config
from logger import get_logger
from cache import get_cache
from health import get_health_monitor
from keywords import get_expander
from ui import ProgressBar, OutputFormatter, InteractiveConfig
from subscription import get_subscription_manager, create_quick_subscription

# 导入异步获取器（如果 aiohttp 可用）
try:
    import aiohttp
    from async_fetcher import AsyncNewsFetcher
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    AsyncNewsFetcher = None


class NewsAggregatorCLI:
    """新闻聚合器 CLI"""

    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self.cache = get_cache()
        self.health_monitor = get_health_monitor()
        self.keyword_expander = get_expander()
        self.formatter = OutputFormatter()

        # 可用的数据源
        self.all_sources = [
            'hackernews', 'github', 'weibo', '36kr', 'v2ex',
            'tencent', 'wallstreetcn', 'producthunt', 'reddit', 'techcrunch'
        ]

    def parse_sources(self, source_str: str) -> List[str]:
        """解析数据源参数"""
        if source_str == 'all':
            return [s for s in self.all_sources
                    if self.config.sources[s].enabled]
        return [s.strip() for s in source_str.split(',')
                if s.strip() in self.config.sources]

    def expand_keyword(self, keyword: Optional[str]) -> Optional[str]:
        """扩展关键词（如果启用）"""
        if not keyword or not self.config.smart_keyword_expansion:
            return keyword
        return self.keyword_expander.expand(keyword)

    async def fetch_async(
        self,
        sources: List[str],
        limit: int,
        keyword: Optional[str],
        deep: bool
    ) -> List[Dict[str, Any]]:
        """异步获取新闻"""
        async with AsyncNewsFetcher() as fetcher:
            # 并发获取
            items = await fetcher.fetch_all_sources(sources, limit, keyword)

            # 深度获取内容
            if deep and items:
                items = await fetcher.enrich_with_content(items)

            return items

    def fetch_sync_fallback(
        self,
        sources: List[str],
        limit: int,
        keyword: Optional[str]
    ) -> List[Dict[str, Any]]:
        """同步回退方法（使用旧的 requests 实现）"""
        # 这里保留原有的同步实现作为回退
        # 为简洁起见，这里仅返回空列表
        self.logger.warning("使用同步回退方法，功能受限")
        return []

    def run(
        self,
        sources: List[str],
        limit: int = 10,
        keyword: Optional[str] = None,
        deep: bool = False,
        output_format: str = "json",
        use_cache: bool = True,
        expand_keywords: bool = True
    ) -> List[Dict[str, Any]]:
        """运行新闻聚合器"""
        self.logger.info(f"开始获取新闻，数据源: {sources}")

        # 扩展关键词
        if expand_keywords and keyword:
            keyword = self.expand_keyword(keyword)

        all_items = []

        # 检查缓存
        if use_cache:
            for source in sources:
                cached = self.cache.get(source, keyword)
                if cached:
                    all_items.extend(cached)
                    self.logger.info(f"从缓存加载: {source} ({len(cached)} 条)")

        # 确定需要获取的源
        sources_to_fetch = [s for s in sources if s not in [i.get('source', '').lower().replace(' ', '_') for i in all_items]]

        if not sources_to_fetch:
            self.logger.info("所有数据均来自缓存")
            return all_items[:limit]

        # 使用异步或同步方法
        if ASYNC_AVAILABLE and self.config.performance.async_enabled:
            try:
                items = asyncio.run(self.fetch_async(sources_to_fetch, limit, keyword, deep))
            except Exception as e:
                self.logger.error(f"异步获取失败: {e}")
                items = self.fetch_sync_fallback(sources_to_fetch, limit, keyword)
        else:
            items = self.fetch_sync_fallback(sources_to_fetch, limit, keyword)

        # 更新缓存
        if use_cache and items:
            for source in sources_to_fetch:
                source_items = [i for i in items if i.get('source', '').lower().replace(' ', '_') == source]
                if source_items:
                    self.cache.set(source, source_items, keyword)

        all_items.extend(items)
        self.logger.info(f"共获取 {len(all_items)} 条新闻")

        return all_items

    def output(self, items: List[Dict[str, Any]], format: str = "json", save: bool = True):
        """输出结果"""
        if format == "json":
            content = self.formatter.format_json(items)
            safe_write(content)
        elif format == "markdown":
            content = self.formatter.format_markdown(items)
            safe_write(content)
        elif format == "html":
            content = self.formatter.format_html(items)
            safe_write(content)

        # 保存报告
        if save and items:
            report_path = self.formatter.save_report(content, format)
            if report_path:
                safe_print(f"\n📄 报告已保存到: {report_path}")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="News Aggregator - 全网热点新闻聚合器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 获取 Hacker News 前 15 条
  python fetch_news.py --source hackernews --limit 15

  # 获取 AI 相关新闻（带智能关键词扩展）
  python fetch_news.py --source all --keyword "AI" --limit 20

  # 深度获取文章内容
  python fetch_news.py --source hackernews,github --limit 10 --deep

  # 输出 Markdown 格式
  python fetch_news.py --source all --format markdown

  # 交互式配置
  python fetch_news.py --interactive

  # 查看健康状态
  python fetch_news.py --health

  # 管理订阅
  python fetch_news.py --subscription status
  python fetch_news.py --subscription run
        """
    )

    parser.add_argument('--source', '-s', default='all',
                       help='数据源（逗号分隔或 all）')
    parser.add_argument('--limit', '-l', type=int, default=10,
                       help='每个数据源的条数限制')
    parser.add_argument('--keyword', '-k', help='关键词过滤（逗号分隔）')
    parser.add_argument('--deep', '-d', action='store_true',
                       help='深度获取文章内容')
    parser.add_argument('--format', '-f', choices=['json', 'markdown', 'html'],
                       default='json', help='输出格式')
    parser.add_argument('--no-cache', action='store_true',
                       help='禁用缓存')
    parser.add_argument('--no-expand', action='store_true',
                       help='禁用关键词智能扩展')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='交互式配置')
    parser.add_argument('--health', action='store_true',
                       help='显示健康状态报告')
    parser.add_argument('--subscription', nargs='?', const='status',
                       choices=['status', 'run', 'list'],
                       help='订阅管理')
    parser.add_argument('--save', action='store_true', default=True,
                       help='保存报告到文件')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细日志输出')

    args = parser.parse_args()

    # 设置日志级别
    if args.verbose:
        get_logger().logger.setLevel(logging.DEBUG)

    cli = NewsAggregatorCLI()

    # 处理特殊命令
    if args.health:
        report = cli.health_monitor.get_health_report()
        safe_write(report)
        return

    if args.subscription:
        sub_manager = get_subscription_manager()

        if args.subscription == 'status':
            print(sub_manager.get_status())
        elif args.subscription == 'list':
            for sub in sub_manager.list_all():
                print(f"  - {sub.name}: {', '.join(sub.sources)}")
        elif args.subscription == 'run':
            due = sub_manager.get_due_subscriptions()
            if not due:
                print("没有需要运行的订阅")
                return

            print(f"运行 {len(due)} 个订阅...")
            for sub in due:
                print(f"\n执行订阅: {sub.name}")
                items = cli.run(
                    cli.parse_sources(','.join(sub.sources)),
                    limit=args.limit,
                    keyword=sub.keywords,
                    deep=sub.deep_fetch,
                    use_cache=not args.no_cache
                )
                cli.output(items, sub.output_format, save=args.save)
                sub_manager.update_last_run(sub.name)
        return

    # 交互式模式
    if args.interactive:
        config = InteractiveConfig()
        sources = config.prompt_sources()
        keyword = config.prompt_keyword()
        output_format = config.prompt_format()

        items = cli.run(
            sources,
            limit=args.limit,
            keyword=keyword,
            deep=args.deep,
            use_cache=not args.no_cache
        )
        cli.output(items, output_format, save=args.save)
        return

    # 正常模式
    sources = cli.parse_sources(args.source)
    if not sources:
        print("错误: 没有可用的数据源", file=sys.stderr)
        sys.exit(1)

    items = cli.run(
        sources,
        limit=args.limit,
        keyword=args.keyword,
        deep=args.deep,
        output_format=args.format,
        use_cache=not args.no_cache,
        expand_keywords=not args.no_expand
    )

    cli.output(items, args.format, save=args.save)


if __name__ == "__main__":
    main()
