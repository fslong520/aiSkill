#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票研究技能配置模块
提供统一的配置管理功能
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class CacheConfig:
    """缓存配置"""
    enabled: bool = True
    ttl_hours: int = 24
    max_size: int = 1000  # 最大缓存项目数
    cache_dir: str = "~/.stock_analyzer_cache"


@dataclass
class AnalysisConfig:
    """分析配置"""
    default_period: int = 120  # 默认分析周期（天）
    ma_periods: list = None    # 移动平均线周期
    rsi_period: int = 14       # RSI计算周期
    macd_fast: int = 12        # MACD快线周期
    macd_slow: int = 26        # MACD慢线周期
    macd_signal: int = 9       # MACD信号线周期
    
    def __post_init__(self):
        if self.ma_periods is None:
            self.ma_periods = [5, 10, 20, 30, 60]


@dataclass
class ScoringConfig:
    """评分配置"""
    fundamental_weight: float = 0.4   # 基本面权重
    technical_weight: float = 0.35    # 技术面权重
    sentiment_weight: float = 0.25    # 情绪面权重
    risk_threshold_low: float = 7.0   # 低风险阈值
    risk_threshold_high: float = 4.0  # 高风险阈值


@dataclass
class OutputConfig:
    """输出配置"""
    default_format: str = "text"  # 默认输出格式: text/json/csv
    show_details: bool = True     # 是否显示详细信息
    precision: int = 2            # 数值精度


@dataclass
class StockConfig:
    """股票研究主配置"""
    cache: CacheConfig = None
    analysis: AnalysisConfig = None
    scoring: ScoringConfig = None
    output: OutputConfig = None
    
    def __post_init__(self):
        if self.cache is None:
            self.cache = CacheConfig()
        if self.analysis is None:
            self.analysis = AnalysisConfig()
        if self.scoring is None:
            self.scoring = ScoringConfig()
        if self.output is None:
            self.output = OutputConfig()


def get_config_from_env() -> StockConfig:
    """从环境变量获取配置"""
    cache_enabled = os.getenv("STOCK_CACHE_ENABLED", "true").lower() == "true"
    cache_ttl = int(os.getenv("STOCK_CACHE_TTL_HOURS", "24"))
    default_format = os.getenv("STOCK_OUTPUT_FORMAT", "text")
    
    return StockConfig(
        cache=CacheConfig(
            enabled=cache_enabled,
            ttl_hours=cache_ttl
        ),
        output=OutputConfig(
            default_format=default_format
        )
    )


def get_default_config() -> StockConfig:
    """获取默认配置"""
    env_config = get_config_from_env()
    
    # 如果环境变量没有覆盖，则使用默认值
    if env_config.cache.enabled:
        cache_config = CacheConfig(
            enabled=env_config.cache.enabled,
            ttl_hours=env_config.cache.ttl_hours
        )
    else:
        cache_config = CacheConfig(enabled=False)
    
    return StockConfig(
        cache=cache_config,
        output=OutputConfig(default_format=env_config.output.default_format)
    )


# 全局配置实例
CONFIG = get_default_config()


def print_config_summary(config: Optional[StockConfig] = None):
    """打印配置摘要"""
    if config is None:
        config = CONFIG
    
    print("=== 股票研究技能配置 ===")
    print(f"- 缓存启用: {config.cache.enabled}")
    print(f"- 缓存TTL: {config.cache.ttl_hours}小时")
    print(f"- 默认分析周期: {config.analysis.default_period}天")
    print(f"- 默认输出格式: {config.output.default_format}")
    print(f"- 基本面权重: {config.scoring.fundamental_weight}")
    print(f"- 技术面权重: {config.scoring.technical_weight}")
    print(f"- 情绪面权重: {config.scoring.sentiment_weight}")


if __name__ == "__main__":
    print_config_summary()