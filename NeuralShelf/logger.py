#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理器日志系统
提供统一的日志记录和管理功能
"""

import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional
from config import get_config


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',      # 红色
        'CRITICAL': '\033[35m',   # 紫色
        'RESET': '\033[0m'        # 重置
    }
    
    def format(self, record):
        # 添加颜色
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class FileOrganizerLogger:
    """文件整理器专用日志管理器"""
    
    def __init__(self, name: str = 'file_organizer'):
        """
        初始化日志管理器
        
        Args:
            name: 日志器名称
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        config = get_config()
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_level = getattr(logging, config.get('logging.level', 'INFO'))
        console_handler.setLevel(console_level)
        
        # 彩色格式化器
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # 文件处理器
        log_file = config.get('logging.file', './logs/organizer.log')
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 使用RotatingFileHandler进行日志轮转
        max_bytes = self._parse_size(config.get('logging.max_size', '10MB'))
        backup_count = config.get('logging.backup_count', 5)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 文件格式化器
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def _parse_size(self, size_str: str) -> int:
        """
        解析大小字符串为字节数
        
        Args:
            size_str: 大小字符串（如 '10MB', '500KB'）
            
        Returns:
            字节数
        """
        size_str = size_str.upper().strip()
        
        if size_str.endswith('GB'):
            return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
        elif size_str.endswith('MB'):
            return int(float(size_str[:-2]) * 1024 * 1024)
        elif size_str.endswith('KB'):
            return int(float(size_str[:-2]) * 1024)
        else:
            return int(size_str)
    
    def debug(self, message: str):
        """调试级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """信息级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """错误级别日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """严重错误级别日志"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """异常日志（包含堆栈跟踪）"""
        self.logger.exception(message)
    
    def operation_start(self, operation: str, target: str = ""):
        """记录操作开始"""
        msg = f"🚀 开始执行: {operation}"
        if target:
            msg += f" - 目标: {target}"
        self.logger.info(msg)
    
    def operation_complete(self, operation: str, duration: float, stats: Optional[dict] = None):
        """记录操作完成"""
        msg = f"✅ 操作完成: {operation} (耗时 {duration:.2f}秒)"
        if stats:
            msg += f" - 统计: {stats}"
        self.logger.info(msg)
    
    def file_processed(self, action: str, source: str, target: str = "", size: int = 0):
        """记录文件处理事件"""
        size_mb = size / (1024 * 1024) if size > 0 else 0
        msg = f"📄 {action}: {source}"
        if target:
            msg += f" → {target}"
        if size_mb > 0:
            msg += f" ({size_mb:.2f} MB)"
        self.logger.info(msg)
    
    def duplicate_found(self, original: str, duplicate: str, strategy: str):
        """记录发现重复文件"""
        msg = f"🔍 发现重复文件: {duplicate}"
        msg += f" (原始文件: {original}, 处理策略: {strategy})"
        self.logger.info(msg)
    
    def error_occurred(self, error: str, context: str = ""):
        """记录错误发生"""
        msg = f"❌ 错误: {error}"
        if context:
            msg += f" - 上下文: {context}"
        self.logger.error(msg)


# 全局日志实例
_logger_instance = None


def get_logger() -> FileOrganizerLogger:
    """
    获取日志管理器实例（单例模式）
    
    Returns:
        FileOrganizerLogger实例
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = FileOrganizerLogger()
    return _logger_instance


def setup_logging(config_file: Optional[str] = None):
    """
    初始化日志系统
    
    Args:
        config_file: 配置文件路径
    """
    # 确保配置已加载
    if config_file:
        from config import load_config
        load_config(config_file)
    
    # 获取日志实例以触发初始化
    get_logger()


class OperationTimer:
    """操作计时器上下文管理器"""
    
    def __init__(self, operation_name: str, logger: Optional[FileOrganizerLogger] = None):
        """
        初始化计时器
        
        Args:
            operation_name: 操作名称
            logger: 日志记录器
        """
        self.operation_name = operation_name
        self.logger = logger or get_logger()
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """进入上下文"""
        self.start_time = datetime.now()
        self.logger.operation_start(self.operation_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.operation_complete(self.operation_name, duration)
        else:
            self.logger.error(f"操作失败: {self.operation_name} - {str(exc_val)}")
        
        return False  # 不抑制异常


# 便捷函数
def log_operation(operation_name: str):
    """装饰器：为函数添加操作日志"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            with OperationTimer(operation_name, logger):
                return func(*args, **kwargs)
        return wrapper
    return decorator