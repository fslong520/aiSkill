#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存管理模块
负责处理股票数据的缓存逻辑
"""

import pickle
from pathlib import Path
from datetime import datetime
import time


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_enabled=True, cache_ttl_hours=24):
        """
        初始化缓存管理器
        :param cache_enabled: 是否启用缓存
        :param cache_ttl_hours: 缓存生存时间（小时）
        """
        self.cache_enabled = cache_enabled
        self.cache_ttl_hours = cache_ttl_hours
        self.cache_dir = Path.home() / ".stock_analyzer_cache"
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cached_data(self, cache_key):
        """获取缓存数据"""
        if not self.cache_enabled:
            return None
            
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        if cache_file.exists():
            # 检查缓存是否过期（根据配置的TTL）
            cache_time = cache_file.stat().st_mtime
            cache_age_hours = (datetime.now().timestamp() - cache_time) / 3600
            if cache_age_hours <= self.cache_ttl_hours:
                try:
                    with open(cache_file, 'rb') as f:
                        return pickle.load(f)
                except:
                    pass
        return None
    
    def set_cached_data(self, cache_key, data):
        """设置缓存数据"""
        if not self.cache_enabled:
            return
            
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except:
            pass
    
    def clear_cache(self):
        """清空缓存"""
        import os
        for file in self.cache_dir.glob("*.pkl"):
            try:
                os.remove(file)
            except:
                pass


def get_default_cache_manager():
    """获取默认缓存管理器"""
    return CacheManager()