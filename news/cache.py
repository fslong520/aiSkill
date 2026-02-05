"""
智能缓存系统
支持内存缓存和文件缓存
"""
import hashlib
import json
import pickle
import time
from pathlib import Path
from typing import Any, Optional, Dict
from collections import OrderedDict
from logger import get_logger
from config import get_config

class CacheBackend:
    """缓存后端基类"""

    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    def set(self, key: str, value: Any, ttl: int) -> bool:
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class MemoryCache(CacheBackend):
    """内存缓存（LRU）"""

    def __init__(self, max_size: int = 1000):
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.max_size = max_size
        self.logger = get_logger()

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None

        value, expire_time = self.cache[key]
        if time.time() > expire_time:
            # 已过期
            del self.cache[key]
            return None

        # LRU: 移到末尾
        self.cache.move_to_end(key)
        return value

    def set(self, key: str, value: Any, ttl: int) -> bool:
        try:
            expire_time = time.time() + ttl
            self.cache[key] = (value, expire_time)
            self.cache.move_to_end(key)

            # 超出大小限制，删除最旧的
            while len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

            return True
        except Exception as e:
            self.logger.error(f"内存缓存设置失败: {e}")
            return False

    def delete(self, key: str) -> bool:
        return self.cache.pop(key, None) is not None

    def clear(self):
        self.cache.clear()


class FileCache(CacheBackend):
    """文件缓存"""

    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger()

    def _get_cache_path(self, key: str) -> Path:
        """生成缓存文件路径"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"

    def get(self, key: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "rb") as f:
                data = pickle.load(f)
                value, expire_time = data

                if time.time() > expire_time:
                    # 已过期
                    cache_path.unlink(missing_ok=True)
                    return None

                return value
        except Exception as e:
            self.logger.error(f"文件缓存读取失败: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int) -> bool:
        cache_path = self._get_cache_path(key)
        try:
            expire_time = time.time() + ttl
            with open(cache_path, "wb") as f:
                pickle.dump((value, expire_time), f)
            return True
        except Exception as e:
            self.logger.error(f"文件缓存写入失败: {e}")
            return False

    def delete(self, key: str) -> bool:
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False

    def clear(self):
        """清空所有缓存文件"""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink(missing_ok=True)


class NewsCache:
    """新闻缓存管理器"""

    def __init__(self):
        config = get_config()
        self.config = config.cache
        self.logger = get_logger()

        # 初始化缓存后端
        if self.config.backend == "file":
            self.backend = FileCache()
        else:
            self.backend = MemoryCache()

        self.enabled = self.config.enabled
        self.default_ttl = self.config.ttl

    def _generate_key(self, source: str, keyword: Optional[str] = None, **kwargs) -> str:
        """生成缓存键"""
        key_parts = [source]
        if keyword:
            key_parts.append(keyword)
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, source: str, keyword: Optional[str] = None, **kwargs) -> Optional[list]:
        """获取缓存数据"""
        if not self.enabled:
            return None

        key = self._generate_key(source, keyword, **kwargs)
        data = self.backend.get(key)

        if data is not None:
            self.logger.info(f"缓存命中: {source} (keyword: {keyword})")
        else:
            self.logger.debug(f"缓存未命中: {source}")

        return data

    def set(self, source: str, data: list, keyword: Optional[str] = None, ttl: Optional[int] = None, **kwargs) -> bool:
        """设置缓存数据"""
        if not self.enabled:
            return False

        key = self._generate_key(source, keyword, **kwargs)
        ttl = ttl or self.default_ttl
        success = self.backend.set(key, data, ttl)

        if success:
            self.logger.info(f"缓存已设置: {source} (TTL: {ttl}s)")

        return success

    def invalidate(self, source: Optional[str] = None):
        """使缓存失效"""
        if source:
            # TODO: 实现按源失效
            self.logger.info(f"清除缓存: {source}")
        else:
            self.backend.clear()
            self.logger.info("所有缓存已清除")

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return {
            "enabled": self.enabled,
            "backend": self.config.backend,
            "default_ttl": self.default_ttl
        }


# 全局缓存实例
_cache = None

def get_cache() -> NewsCache:
    """获取缓存实例"""
    global _cache
    if _cache is None:
        _cache = NewsCache()
    return _cache
