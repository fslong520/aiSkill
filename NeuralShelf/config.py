#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理器配置管理系统
负责加载、验证和管理所有配置选项
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认配置
        """
        self.config_file = config_file
        self.config = self._load_default_config()
        
        if config_file and os.path.exists(config_file):
            self._load_custom_config(config_file)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            # 基础配置
            'target_directory': '.',
            'backup_enabled': True,
            'dry_run': False,
            'verbose': False,
            
            # 排除配置
            'exclude_patterns': [
                '*.tmp',
                '*.log',
                '*.cache',
                '__pycache__',
                '.DS_Store',
                'Thumbs.db'
            ],
            
            'exclude_directories': [
                '.git',
                '.svn',
                'node_modules',
                '__pycache__'
            ],
            
            # 重复文件处理策略
            'duplicate_strategy': 'keep_newest',  # keep_newest, keep_largest, keep_first
            
            # 文件类型映射
            'file_types': {
                'documents': {
                    'extensions': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf'],
                    'target_folder': 'Documents'
                },
                'images': {
                    'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
                    'target_folder': 'Images'
                },
                'videos': {
                    'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
                    'target_folder': 'Videos'
                },
                'audio': {
                    'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
                    'target_folder': 'Audio'
                },
                'archives': {
                    'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                    'target_folder': 'Archives'
                },
                'code': {
                    'extensions': ['.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css', '.php'],
                    'target_folder': 'Code'
                },
                'executables': {
                    'extensions': ['.exe', '.msi', '.deb', '.rpm', '.dmg'],
                    'target_folder': 'Executables'
                }
            },
            
            # 命名规范
            'naming_conventions': {
                'default': '{category}/{filename}',
                'documents': '{year}/{month}/{filename}',
                'images': '{year}/{month}/{day}/{filename}',
                'videos': '{year}/{month}/{filename}',
                'code': '{project}/{filename}'
            },
            
            # 时间格式
            'date_format': {
                'year': '%Y',
                'month': '%m',
                'day': '%d'
            },
            
            # 报告配置
            'report': {
                'enabled': True,
                'format': 'markdown',
                'save_directory': './reports',
                'include_statistics': True,
                'include_file_list': True
            },
            
            # 日志配置
            'logging': {
                'level': 'INFO',
                'file': './logs/organizer.log',
                'max_size': '10MB',
                'backup_count': 5
            }
        }
    
    def _load_custom_config(self, config_file: str) -> None:
        """
        加载自定义配置文件
        
        Args:
            config_file: 配置文件路径
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = yaml.safe_load(f)
            
            # 合并配置（自定义配置覆盖默认配置）
            self._merge_configs(self.config, custom_config)
            
        except Exception as e:
            raise ValueError(f"配置文件加载失败 {config_file}: {str(e)}")
    
    def _merge_configs(self, base_config: Dict, custom_config: Dict) -> None:
        """
        递归合并配置字典
        
        Args:
            base_config: 基础配置
            custom_config: 自定义配置
        """
        for key, value in custom_config.items():
            if key in base_config and isinstance(base_config[key], dict) and isinstance(value, dict):
                self._merge_configs(base_config[key], value)
            else:
                base_config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键（支持点号分隔的嵌套键，如 'file_types.documents')
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        # 导航到倒数第二层
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置最后一层的值
        config[keys[-1]] = value
    
    def validate(self) -> List[str]:
        """
        验证配置的有效性
        
        Returns:
            错误消息列表
        """
        errors = []
        
        # 验证必要配置项
        required_keys = ['target_directory', 'file_types', 'duplicate_strategy']
        for key in required_keys:
            if self.get(key) is None:
                errors.append(f"缺少必要配置项: {key}")
        
        # 验证重复文件处理策略
        valid_strategies = ['keep_newest', 'keep_largest', 'keep_first', 'keep_all']
        strategy = self.get('duplicate_strategy')
        if strategy not in valid_strategies:
            errors.append(f"无效的重复文件处理策略: {strategy}")
        
        # 验证文件类型配置
        file_types = self.get('file_types', {})
        for category, config in file_types.items():
            if 'extensions' not in config or 'target_folder' not in config:
                errors.append(f"文件类型 {category} 配置不完整")
        
        return errors
    
    def save_config(self, filepath: str) -> None:
        """
        保存当前配置到文件
        
        Args:
            filepath: 保存路径
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def get_file_type_category(self, file_extension: str) -> Optional[str]:
        """
        根据文件扩展名获取文件类型分类
        
        Args:
            file_extension: 文件扩展名（包含点号）
            
        Returns:
            文件类型分类名称
        """
        file_types = self.get('file_types', {})
        
        for category, config in file_types.items():
            extensions = config.get('extensions', [])
            if file_extension.lower() in [ext.lower() for ext in extensions]:
                return category
        
        return 'others'  # 未分类文件
    
    def get_target_folder(self, file_extension: str) -> str:
        """
        根据文件扩展名获取目标文件夹
        
        Args:
            file_extension: 文件扩展名
            
        Returns:
            目标文件夹名称
        """
        category = self.get_file_type_category(file_extension)
        if category == 'others':
            return 'Others'
        
        file_types = self.get('file_types', {})
        return file_types.get(category, {}).get('target_folder', category.capitalize())
    
    def get_naming_pattern(self, file_extension: str) -> str:
        """
        获取文件命名模式
        
        Args:
            file_extension: 文件扩展名
            
        Returns:
            命名模式字符串
        """
        category = self.get_file_type_category(file_extension)
        conventions = self.get('naming_conventions', {})
        
        # 优先使用特定类型的命名规则
        if category in conventions:
            return conventions[category]
        
        # 使用默认命名规则
        return conventions.get('default', '{category}/{filename}')


def setup_logging(config_file: Optional[str] = None):
    """
    初始化日志系统
    
    Args:
        config_file: 配置文件路径
    """
    # 确保配置已加载
    if config_file:
        load_config(config_file)
    
    # 初始化日志系统已经在logger.py中处理
    from logger import get_logger
    get_logger()


# 全局配置实例
config_manager = None


def get_config(config_file: Optional[str] = None) -> ConfigManager:
    """
    获取配置管理器实例（单例模式）
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        ConfigManager实例
    """
    global config_manager
    if config_manager is None:
        config_manager = ConfigManager(config_file)
    return config_manager


def load_config(config_file: str) -> ConfigManager:
    """
    加载指定配置文件
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        ConfigManager实例
    """
    return ConfigManager(config_file)