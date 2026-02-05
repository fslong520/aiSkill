"""
用户体验增强组件
进度条、交互式配置、自定义模板
"""
import sys
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from logger import get_logger

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class ProgressBar:
    """进度条（带降级支持）"""

    def __init__(self, total: int, desc: str = "Processing"):
        self.total = total
        self.desc = desc
        self.current = 0
        self.start_time = time.time()
        self.logger = get_logger()

        if TQDM_AVAILABLE:
            self.tqdm_bar = tqdm(total=total, desc=desc, file=sys.stdout)
        else:
            self.tqdm_bar = None
            self._print_header()

    def _print_header(self):
        """打印简单进度头"""
        sys.stdout.write(f"\n{self.desc}...\n")
        sys.stdout.flush()

    def update(self, n: int = 1):
        """更新进度"""
        self.current += n

        if self.tqdm_bar:
            self.tqdm_bar.update(n)
        else:
            # 简单文本进度条
            percent = min(100, int(self.current / self.total * 100))
            filled = int(percent / 2)
            bar = "█" * filled + "░" * (50 - filled)
            elapsed = time.time() - self.start_time
            sys.stdout.write(f"\r[{bar}] {percent}% ({self.current}/{self.total}) {elapsed:.1f}s")
            sys.stdout.flush()

    def close(self):
        """关闭进度条"""
        if self.tqdm_bar:
            self.tqdm_bar.close()
        else:
            sys.stdout.write("\n✓ 完成\n\n")
            sys.stdout.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class OutputFormatter:
    """输出格式化器"""

    def __init__(self):
        self.logger = get_logger()

    def format_json(self, items: List[Dict[str, Any]], pretty: bool = True) -> str:
        """格式化为 JSON"""
        import json
        return json.dumps(items, indent=2 if pretty else None, ensure_ascii=False)

    def format_markdown(self, items: List[Dict[str, Any]], title: str = "新闻汇总") -> str:
        """格式化为 Markdown"""
        lines = [
            f"# {title}\n",
            f"*生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*  \n",
            f"*总计 {len(items)} 条新闻*\n",
            "---\n"
        ]

        # 按来源分组
        by_source: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            source = item.get('source', 'Unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(item)

        # 生成各来源的条目
        for source, source_items in by_source.items():
            lines.append(f"\n## {source}\n")

            for i, item in enumerate(source_items, 1):
                title = item.get('title', '无标题')
                url = item.get('url', '')
                time_str = item.get('time', '')
                heat = item.get('heat', '')

                # 标题链接
                if url:
                    lines.append(f"### {i}. [{title}]({url})\n")
                else:
                    lines.append(f"### {i}. {title}\n")

                # 元数据行
                meta_parts = []
                if time_str:
                    meta_parts.append(f"🕒 {time_str}")
                if heat:
                    meta_parts.append(f"🔥 {heat}")

                if meta_parts:
                    lines.append(f"*{' | '.join(meta_parts)}*\n")

                # 深度内容（如果有）
                if 'content' in item and item['content']:
                    content = item['content'][:300]
                    lines.append(f"\n> {content}...\n")

                lines.append("\n")

        return "\n".join(lines)

    def format_html(self, items: List[Dict[str, Any]], title: str = "新闻汇总") -> str:
        """格式化为 HTML"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007AFF; padding-bottom: 10px; }}
        .meta {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
        .source {{ margin-top: 30px; }}
        .source-header {{ color: #007AFF; font-size: 18px; font-weight: bold; margin-bottom: 15px; }}
        .item {{ margin-bottom: 20px; padding: 15px; background: #f9f9f9; border-radius: 6px; }}
        .item-title {{ font-size: 16px; font-weight: 600; margin-bottom: 8px; }}
        .item-title a {{ color: #333; text-decoration: none; }}
        .item-title a:hover {{ color: #007AFF; }}
        .item-meta {{ font-size: 12px; color: #888; }}
        .item-content {{ margin-top: 10px; font-size: 14px; color: #555; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p class="meta">生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')} | 总计 {len(items)} 条新闻</p>
"""

        # 按来源分组
        by_source: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            source = item.get('source', 'Unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(item)

        for source, source_items in by_source.items():
            html += f'        <div class="source">\n'
            html += f'            <div class="source-header">{source}</div>\n'

            for item in source_items:
                title = item.get('title', '无标题')
                url = item.get('url', '')
                time_str = item.get('time', '')
                heat = item.get('heat', '')
                content = item.get('content', '')

                html += f'            <div class="item">\n'
                html += f'                <div class="item-title">'
                if url:
                    html += f'<a href="{url}" target="_blank">{title}</a>'
                else:
                    html += title
                html += f'</div>\n'

                if time_str or heat:
                    html += f'                <div class="item-meta">'
                    if time_str:
                        html += f'🕒 {time_str} '
                    if heat:
                        html += f'🔥 {heat}'
                    html += f'</div>\n'

                if content:
                    html += f'                <div class="item-content">{content[:300]}...</div>\n'

                html += f'            </div>\n'

            html += f'        </div>\n'

        html += """    </div>
</body>
</html>"""
        return html

    def save_report(self, content: str, format: str = "markdown", prefix: str = "news_report") -> Optional[str]:
        """保存报告到文件"""
        config = get_logger().logger.manager.loggerDict.get('NewsAggregator')
        try:
            from config import get_config
            config_obj = get_config()

            if not config_obj.save_reports:
                return None

            reports_dir = Path(config_obj.reports_dir)
            reports_dir.mkdir(parents=True, exist_ok=True)

            timestamp = time.strftime('%Y%m%d_%H%M%S')
            extension = "md" if format == "markdown" else ("json" if format == "json" else "html")
            filename = f"{prefix}_{timestamp}.{extension}"
            filepath = reports_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            self.logger.info(f"报告已保存: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"保存报告失败: {e}")
            return None


class TemplateManager:
    """模板管理器"""

    def __init__(self):
        self.logger = get_logger()
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)

        # 创建默认模板
        self._create_default_templates()

    def _create_default_templates(self):
        """创建默认输出模板"""
        default_template = """# {{title}}

📅 {{date}} | 🕒 {{time}} | 📊 {{count}} 条新闻

{% for source in sources %}
## {{source.name}}

{% for item in source.items %}
### {{loop.index}}. [{{item.title}}]({{item.url}})

{{item.time}} | {{item.heat}}

{% if item.content %}
> {{item.content[:200]}}...
{% endif %}

{% endfor %}
{% endfor %}

---
*由 News Aggregator 自动生成*
"""
        template_file = self.templates_dir / "default.md"
        if not template_file.exists():
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(default_template)

    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        templates = []
        for file in self.templates_dir.glob("*.md"):
            templates.append(file.stem)
        return templates

    def get_template(self, name: str = "default") -> Optional[str]:
        """获取模板内容"""
        template_file = self.templates_dir / f"{name}.md"
        if template_file.exists():
            return template_file.read_text(encoding='utf-8')
        return None

    def save_template(self, name: str, content: str):
        """保存自定义模板"""
        template_file = self.templates_dir / f"{name}.md"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(content)
        self.logger.info(f"模板已保存: {name}")


class InteractiveConfig:
    """交互式配置助手"""

    def __init__(self):
        self.logger = get_logger()

    def prompt_sources(self) -> List[str]:
        """提示用户选择数据源"""
        available = [
            ("hackernews", "Hacker News - 硅谷技术热点"),
            ("github", "GitHub Trending - 开源项目趋势"),
            ("producthunt", "Product Hunt - 新产品发现"),
            ("36kr", "36Kr - 中文科技快讯"),
            ("tencent", "腾讯新闻 - 科技资讯"),
            ("wallstreetcn", "华尔街见闻 - 金融动态"),
            ("v2ex", "V2EX - 开发者社区"),
            ("weibo", "微博热搜 - 社交热点"),
            ("reddit", "Reddit /r/technology - 科技讨论"),
            ("techcrunch", "TechCrunch - 科技新闻"),
        ]

        print("\n📡 可用数据源：")
        for i, (key, desc) in enumerate(available, 1):
            print(f"  {i:2d}. {desc}")

        print("\n请输入序号（多个用空格分隔，直接回车选择全部）: ", end="")
        choice = input().strip()

        if not choice:
            return [key for key, _ in available]

        selected = []
        for num in choice.split():
            idx = int(num) - 1
            if 0 <= idx < len(available):
                selected.append(available[idx][0])

        return selected

    def prompt_keyword(self) -> Optional[str]:
        """提示用户输入关键词"""
        print("\n🔍 输入关键词过滤（可选，直接回车跳过）: ", end="")
        keyword = input().strip()
        return keyword if keyword else None

    def prompt_format(self) -> str:
        """提示用户选择输出格式"""
        print("\n📄 输出格式：")
        print("  1. JSON")
        print("  2. Markdown")
        print("  3. HTML")
        print("请选择（直接回车默认 Markdown）: ", end="")
        choice = input().strip()

        format_map = {"1": "json", "2": "markdown", "3": "html"}
        return format_map.get(choice, "markdown")
