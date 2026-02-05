"""
News Aggregator Logger
统一的日志系统
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from config import get_config

class NewsAggregatorLogger:
    """日志管理器"""

    _instance: Optional["NewsAggregatorLogger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self):
        """配置日志系统"""
        config = get_config()

        # 创建日志器
        self._logger = logging.getLogger("NewsAggregator")
        self._logger.setLevel(getattr(logging, config.log_level.upper()))

        # 清除现有处理器
        self._logger.handlers.clear()

        # 格式化器
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # 文件处理器
        log_file = Path(config.log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        # 防止日志传播
        self._logger.propagate = False

    @property
    def logger(self) -> logging.Logger:
        """获取底层logger实例"""
        return self._logger

    def debug(self, msg: str, *args, **kwargs):
        """DEBUG级别日志"""
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """INFO级别日志"""
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """WARNING级别日志"""
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, exc_info: bool = False, **kwargs):
        """ERROR级别日志"""
        self._logger.error(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg: str, *args, exc_info: bool = True, **kwargs):
        """CRITICAL级别日志"""
        self._logger.critical(msg, *args, exc_info=exc_info, **kwargs)

# 全局日志实例
def get_logger() -> NewsAggregatorLogger:
    """获取日志实例"""
    return NewsAggregatorLogger()
