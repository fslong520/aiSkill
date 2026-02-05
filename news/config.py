"""
News Aggregator Configuration
集中管理所有配置参数
"""
import os
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class SourceConfig:
    """单个数据源配置"""
    name: str
    enabled: bool = True
    timeout: int = 10
    retry_times: int = 3
    retry_delay: float = 1.0
    max_items: int = 10

@dataclass
class CacheConfig:
    """缓存配置"""
    enabled: bool = True
    ttl: int = 300  # 缓存5分钟
    backend: str = "memory"  # memory, file, redis

@dataclass
class PerformanceConfig:
    """性能配置"""
    max_workers: int = 10
    async_enabled: bool = True
    batch_size: int = 5

@dataclass
class NewsAggregatorConfig:
    """主配置类"""
    # 数据源配置
    sources: Dict[str, SourceConfig] = field(default_factory=dict)

    # 缓存配置
    cache: CacheConfig = field(default_factory=CacheConfig)

    # 性能配置
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)

    # 深度抓取配置
    deep_fetch_max_chars: int = 3000
    deep_fetch_timeout: int = 5

    # 关键词扩展配置
    smart_keyword_expansion: bool = True

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "news_aggregator.log"

    # 输出配置
    output_format: str = "json"  # json, markdown, html
    save_reports: bool = True
    reports_dir: str = "reports"

    def __post_init__(self):
        """初始化默认数据源配置"""
        if not self.sources:
            self.sources = {
                "hackernews": SourceConfig("Hacker News", timeout=10, max_items=15),
                "github": SourceConfig("GitHub Trending", timeout=10, max_items=15),
                "producthunt": SourceConfig("Product Hunt", timeout=10, max_items=10),
                "36kr": SourceConfig("36Kr", timeout=10, max_items=10),
                "tencent": SourceConfig("Tencent News", timeout=8, max_items=10),
                "wallstreetcn": SourceConfig("Wall Street CN", timeout=8, max_items=10),
                "v2ex": SourceConfig("V2EX", timeout=10, max_items=10),
                "weibo": SourceConfig("Weibo Hot Search", timeout=8, max_items=10),
                "reddit": SourceConfig("Reddit Technology", timeout=10, max_items=15),
                "techcrunch": SourceConfig("TechCrunch", timeout=10, max_items=10),
            }

    @classmethod
    def from_env(cls) -> "NewsAggregatorConfig":
        """从环境变量加载配置"""
        config = cls()

        # 从环境变量覆盖配置
        if os.getenv("NEWS_CACHE_DISABLED"):
            config.cache.enabled = False
        if os.getenv("NEWS_LOG_LEVEL"):
            config.log_level = os.getenv("NEWS_LOG_LEVEL")
        if os.getenv("NEWS_ASYNC_DISABLED"):
            config.performance.async_enabled = False

        return config

# 全局配置实例
_config = None

def get_config() -> NewsAggregatorConfig:
    """获取全局配置实例（单例模式）"""
    global _config
    if _config is None:
        _config = NewsAggregatorConfig.from_env()
    return _config

def reset_config():
    """重置配置（主要用于测试）"""
    global _config
    _config = None
