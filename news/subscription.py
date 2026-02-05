"""
订阅模式管理
支持定时推送、个性化配置
"""
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from logger import get_logger
from config import get_config

@dataclass
class Subscription:
    """订阅配置"""
    name: str
    sources: List[str] = field(default_factory=list)
    keywords: Optional[str] = None
    schedule: str = "daily"  # daily, hourly, weekly
    output_format: str = "markdown"
    enabled: bool = True
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    deep_fetch: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Subscription":
        return cls(**data)


class SubscriptionManager:
    """订阅管理器"""

    def __init__(self):
        self.logger = get_logger()
        self.config_file = Path.home() / ".news-aggregator" / "subscriptions.json"
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.subscriptions: Dict[str, Subscription] = {}
        self._load()

    def _load(self):
        """加载订阅配置"""
        if not self.config_file.exists():
            # 创建默认订阅
            self._create_default_subscriptions()
            return

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for name, sub_data in data.items():
                    self.subscriptions[name] = Subscription.from_dict(sub_data)
            self.logger.info(f"加载了 {len(self.subscriptions)} 个订阅")
        except Exception as e:
            self.logger.error(f"加载订阅配置失败: {e}")
            self._create_default_subscriptions()

    def _save(self):
        """保存订阅配置"""
        try:
            data = {name: sub.to_dict() for name, sub in self.subscriptions.items()}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info("订阅配置已保存")
        except Exception as e:
            self.logger.error(f"保存订阅配置失败: {e}")

    def _create_default_subscriptions(self):
        """创建默认订阅"""
        defaults = {
            "daily_tech": Subscription(
                name="daily_tech",
                sources=["hackernews", "github", "36kr", "producthunt"],
                keywords="AI,LLM,GPT",
                schedule="daily",
                output_format="markdown",
                deep_fetch=False
            ),
            "finance_daily": Subscription(
                name="finance_daily",
                sources=["wallstreetcn", "tencent"],
                schedule="daily",
                output_format="markdown"
            ),
            "global_scan": Subscription(
                name="global_scan",
                sources=["all"],
                schedule="daily",
                output_format="markdown"
            ),
            "ai_focus": Subscription(
                name="ai_focus",
                sources=["hackernews", "github", "producthunt"],
                keywords="AI,LLM,DeepSeek",
                schedule="hourly",
                output_format="markdown",
                deep_fetch=True
            )
        }
        self.subscriptions = defaults
        self._save()

    def add(self, subscription: Subscription):
        """添加订阅"""
        self.subscriptions[subscription.name] = subscription
        self._save()
        self.logger.info(f"已添加订阅: {subscription.name}")

    def remove(self, name: str):
        """删除订阅"""
        if name in self.subscriptions:
            del self.subscriptions[name]
            self._save()
            self.logger.info(f"已删除订阅: {name}")

    def get(self, name: str) -> Optional[Subscription]:
        """获取订阅"""
        return self.subscriptions.get(name)

    def list_all(self) -> List[Subscription]:
        """列出所有订阅"""
        return list(self.subscriptions.values())

    def enable(self, name: str):
        """启用订阅"""
        if name in self.subscriptions:
            self.subscriptions[name].enabled = True
            self._save()

    def disable(self, name: str):
        """禁用订阅"""
        if name in self.subscriptions:
            self.subscriptions[name].enabled = False
            self._save()

    def update_last_run(self, name: str):
        """更新最后运行时间"""
        if name in self.subscriptions:
            self.subscriptions[name].last_run = datetime.now().isoformat()
            self._calculate_next_run(name)
            self._save()

    def _calculate_next_run(self, name: str):
        """计算下次运行时间"""
        if name not in self.subscriptions:
            return

        sub = self.subscriptions[name]
        now = datetime.now()

        if sub.schedule == "hourly":
            next_run = now + timedelta(hours=1)
        elif sub.schedule == "daily":
            # 设置为明天早上 8 点
            next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        elif sub.schedule == "weekly":
            # 设置为下周一早上 8 点
            days_ahead = 0 - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
            next_run += timedelta(days=days_ahead)
        else:
            next_run = now + timedelta(hours=1)

        sub.next_run = next_run.isoformat()

    def get_due_subscriptions(self) -> List[Subscription]:
        """获取到期应该运行的订阅"""
        now = datetime.now()
        due = []

        for sub in self.subscriptions.values():
            if not sub.enabled:
                continue

            if not sub.next_run:
                self._calculate_next_run(sub.name)

            try:
                next_run = datetime.fromisoformat(sub.next_run)
                if now >= next_run:
                    due.append(sub)
            except Exception as e:
                self.logger.error(f"解析下次运行时间失败: {e}")

        return due

    def get_status(self) -> str:
        """获取订阅状态报告"""
        lines = [
            "\n" + "=" * 60,
            "📋 订阅状态",
            "=" * 60,
        ]

        for sub in self.subscriptions.values():
            status = "✅ 启用" if sub.enabled else "❌ 禁用"
            lines.append(f"\n📰 {sub.name} [{status}]")
            lines.append(f"   数据源: {', '.join(sub.sources)}")
            lines.append(f"   频率: {sub.schedule}")

            if sub.keywords:
                lines.append(f"   关键词: {sub.keywords}")

            if sub.last_run:
                lines.append(f"   上次运行: {sub.last_run}")

            if sub.next_run:
                lines.append(f"   下次运行: {sub.next_run}")

        lines.append("\n" + "=" * 60 + "\n")
        return "\n".join(lines)


# 全局订阅管理器实例
_manager = None

def get_subscription_manager() -> SubscriptionManager:
    """获取订阅管理器实例"""
    global _manager
    if _manager is None:
        _manager = SubscriptionManager()
    return _manager


def create_quick_subscription(name: str, sources: List[str], **kwargs) -> Subscription:
    """快速创建订阅的便捷函数"""
    return Subscription(
        name=name,
        sources=sources,
        **kwargs
    )
