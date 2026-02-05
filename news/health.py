"""
数据源健康监控系统
"""
import time
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from logger import get_logger
from config import get_config

@dataclass
class SourceHealth:
    """单个数据源的健康状态"""
    name: str
    enabled: bool = True
    success_count: int = 0
    failure_count: int = 0
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    last_error: Optional[str] = None
    avg_response_time: float = 0.0
    total_response_time: float = 0.0
    sample_count: int = 0

    @property
    def success_rate(self) -> float:
        """计算成功率"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 1.0
        return self.success_count / total

    @property
    def is_healthy(self) -> bool:
        """判断是否健康（成功率 > 50% 且最近失败不超过 5 次）"""
        return self.success_rate > 0.5 and self.failure_count < 5

    @property
    def status(self) -> str:
        """获取状态描述"""
        if not self.enabled:
            return "🔴 已禁用"
        if self.is_healthy:
            return "🟢 健康"
        if self.success_rate > 0.2:
            return "🟡 不稳定"
        return "🔴 故障"

    def record_success(self, response_time: float):
        """记录成功请求"""
        self.success_count += 1
        self.last_success = datetime.now()
        self.total_response_time += response_time
        self.sample_count += 1
        self.avg_response_time = self.total_response_time / self.sample_count

    def record_failure(self, error: str):
        """记录失败请求"""
        self.failure_count += 1
        self.last_failure = datetime.now()
        self.last_error = error[:100]  # 限制错误信息长度

    def reset(self):
        """重置统计"""
        self.success_count = 0
        self.failure_count = 0
        self.last_success = None
        self.last_failure = None
        self.last_error = None
        self.avg_response_time = 0.0
        self.total_response_time = 0.0
        self.sample_count = 0


class HealthMonitor:
    """健康监控器"""

    def __init__(self):
        self.logger = get_logger()
        self.config = get_config()
        self.sources: Dict[str, SourceHealth] = {}
        self._initialize_sources()

    def _initialize_sources(self):
        """初始化所有数据源的健康状态"""
        for source_key, source_config in self.config.sources.items():
            self.sources[source_key] = SourceHealth(
                name=source_config.name,
                enabled=source_config.enabled
            )

    def record_success(self, source: str, response_time: float = 0.0):
        """记录成功请求"""
        source_key = source.lower().replace(" ", "_").replace("/", "_")
        if source_key not in self.sources:
            self.sources[source_key] = SourceHealth(name=source)

        self.sources[source_key].record_success(response_time)
        self.logger.debug(f"{source} 请求成功 (响应时间: {response_time:.2f}s)")

    def record_failure(self, source: str, error: str):
        """记录失败请求"""
        source_key = source.lower().replace(" ", "_").replace("/", "_")
        if source_key not in self.sources:
            self.sources[source_key] = SourceHealth(name=source)

        self.sources[source_key].record_failure(error)
        self.logger.warning(f"{source} 请求失败: {error}")

        # 自动禁用连续失败的数据源
        health = self.sources[source_key]
        if health.failure_count >= 5 and health.success_rate < 0.2:
            health.enabled = False
            self.logger.error(f"{source} 连续失败，已自动禁用")

    def get_health(self, source: str) -> SourceHealth:
        """获取特定数据源的健康状态"""
        source_key = source.lower().replace(" ", "_").replace("/", "_")
        return self.sources.get(source_key, SourceHealth(name=source))

    def get_all_health(self) -> Dict[str, SourceHealth]:
        """获取所有数据源的健康状态"""
        return self.sources.copy()

    def get_enabled_sources(self) -> List[str]:
        """获取所有启用的数据源"""
        return [
            key for key, health in self.sources.items()
            if health.enabled
        ]

    def get_health_report(self) -> str:
        """生成健康报告"""
        lines = [
            "\n" + "=" * 60,
            "📊 数据源健康监控报告",
            "=" * 60,
            f"{'数据源':<25} {'状态':<10} {'成功率':<10} {'平均响应时间':<15}",
            "-" * 60
        ]

        for key, health in self.sources.items():
            lines.append(
                f"{health.name:<25} {health.status:<10} "
                f"{health.success_rate*100:>6.1f}%    "
                f"{health.avg_response_time:>6.2f}s"
            )

        lines.append("=" * 60 + "\n")
        return "\n".join(lines)

    def disable_source(self, source: str):
        """手动禁用数据源"""
        source_key = source.lower().replace(" ", "_").replace("/", "_")
        if source_key in self.sources:
            self.sources[source_key].enabled = False
            self.logger.info(f"已禁用数据源: {source}")

    def enable_source(self, source: str):
        """手动启用数据源"""
        source_key = source.lower().replace(" ", "_").replace("/", "_")
        if source_key in self.sources:
            self.sources[source_key].enabled = True
            self.sources[source_key].failure_count = 0
            self.logger.info(f"已启用数据源: {source}")

    def reset_source(self, source: str):
        """重置数据源统计"""
        source_key = source.lower().replace(" ", "_").replace("/", "_")
        if source_key in self.sources:
            self.sources[source_key].reset()
            self.logger.info(f"已重置数据源统计: {source}")

    async def health_check(self, sources: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        执行健康检查

        Args:
            sources: 要检查的数据源列表，None 表示检查所有

        Returns:
            数据源名称到健康状态的映射
        """
        # TODO: 实现实际的健康检查请求
        # 这里仅返回当前状态
        results = {}
        for key, health in self.sources.items():
            if sources is None or key in sources:
                results[key] = health.is_healthy

        return results


# 全局健康监控实例
_monitor = None

def get_health_monitor() -> HealthMonitor:
    """获取健康监控器实例"""
    global _monitor
    if _monitor is None:
        _monitor = HealthMonitor()
    return _monitor
