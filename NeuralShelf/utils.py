#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理器工具函数库
提供常用的辅助函数和实用工具
"""

import os
import hashlib
import mimetypes
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Union
from functools import lru_cache


def get_file_hash(file_path: Union[str, Path], algorithm: str = 'md5') -> str:
    """
    计算文件哈希值
    
    Args:
        file_path: 文件路径
        algorithm: 哈希算法 ('md5', 'sha1', 'sha256')
        
    Returns:
        文件哈希值（十六进制字符串）
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    hash_obj = hashlib.new(algorithm)
    
    try:
        with open(file_path, 'rb') as f:
            # 分块读取以处理大文件
            for chunk in iter(lambda: f.read(8192), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        raise IOError(f"计算文件哈希失败: {str(e)}")


def get_file_info(file_path: Union[str, Path]) -> Dict[str, any]:
    """
    获取文件详细信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        包含文件信息的字典
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    stat = file_path.stat()
    
    # 获取MIME类型
    mime_type, encoding = mimetypes.guess_type(str(file_path))
    
    return {
        'name': file_path.name,
        'stem': file_path.stem,  # 不包含扩展名的文件名
        'suffix': file_path.suffix,  # 扩展名
        'path': str(file_path),
        'parent': str(file_path.parent),
        'size': stat.st_size,
        'created_time': datetime.fromtimestamp(stat.st_ctime),
        'modified_time': datetime.fromtimestamp(stat.st_mtime),
        'accessed_time': datetime.fromtimestamp(stat.st_atime),
        'is_file': file_path.is_file(),
        'is_directory': file_path.is_dir(),
        'permissions': oct(stat.st_mode)[-3:],  # 权限（八进制）
        'mime_type': mime_type or 'unknown',
        'encoding': encoding
    }


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小显示
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def is_binary_file(file_path: Union[str, Path]) -> bool:
    """
    判断文件是否为二进制文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        是否为二进制文件
    """
    file_path = Path(file_path)
    
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            # 检查是否包含空字节或其他二进制字符
            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
            return bool(chunk.translate(None, text_chars))
    except Exception:
        return True  # 出错时假设为二进制文件


def read_text_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """
    读取文本文件内容
    
    Args:
        file_path: 文件路径
        encoding: 文件编码
        
    Returns:
        文件内容字符串
    """
    file_path = Path(file_path)
    
    encodings = [encoding, 'utf-8', 'gbk', 'gb2312', 'latin1']
    
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise IOError(f"读取文件失败: {str(e)}")
    
    raise ValueError(f"无法解码文件: {file_path}")


def get_similar_files(directory: Union[str, Path], similarity_threshold: float = 0.8) -> List[Tuple[str, str]]:
    """
    查找目录中相似的文件（基于文件名相似度）
    
    Args:
        directory: 目录路径
        similarity_threshold: 相似度阈值 (0-1)
        
    Returns:
        相似文件对列表 [(file1, file2), ...]
    """
    directory = Path(directory)
    files = [f for f in directory.iterdir() if f.is_file()]
    similar_pairs = []
    
    for i, file1 in enumerate(files):
        for file2 in files[i+1:]:
            similarity = calculate_filename_similarity(file1.name, file2.name)
            if similarity >= similarity_threshold:
                similar_pairs.append((str(file1), str(file2)))
    
    return similar_pairs


def calculate_filename_similarity(name1: str, name2: str) -> float:
    """
    计算两个文件名的相似度
    
    Args:
        name1: 第一个文件名
        name2: 第二个文件名
        
    Returns:
        相似度分数 (0-1)
    """
    # 移除扩展名进行比较
    stem1 = Path(name1).stem
    stem2 = Path(name2).stem
    
    # 使用简单的字符匹配算法
    if len(stem1) == 0 or len(stem2) == 0:
        return 0.0
    
    # 计算公共子序列长度
    common_length = longest_common_subsequence(stem1.lower(), stem2.lower())
    max_length = max(len(stem1), len(stem2))
    
    return common_length / max_length if max_length > 0 else 0.0


def longest_common_subsequence(s1: str, s2: str) -> int:
    """
    计算最长公共子序列长度
    
    Args:
        s1: 第一个字符串
        s2: 第二个字符串
        
    Returns:
        最长公共子序列长度
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]


@lru_cache(maxsize=1000)
def is_ignored_path(path: Union[str, Path], ignore_patterns: tuple) -> bool:
    """
    检查路径是否应该被忽略（使用缓存提高性能）
    
    Args:
        path: 路径
        ignore_patterns: 忽略模式列表
        
    Returns:
        是否应该忽略
    """
    path_str = str(path)
    
    for pattern in ignore_patterns:
        if re.match(pattern.replace('*', '.*'), path_str):
            return True
    
    return False


def create_backup_path(original_path: Union[str, Path]) -> Path:
    """
    为文件创建备份路径
    
    Args:
        original_path: 原始文件路径
        
    Returns:
        备份文件路径
    """
    original_path = Path(original_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{original_path.stem}_backup_{timestamp}{original_path.suffix}"
    return original_path.parent / backup_name


def safe_move_file(source: Union[str, Path], target: Union[str, Path], 
                   create_backup: bool = True) -> bool:
    """
    安全地移动文件（包含备份和错误处理）
    
    Args:
        source: 源文件路径
        target: 目标文件路径
        create_backup: 是否创建备份
        
    Returns:
        移动是否成功
    """
    source = Path(source)
    target = Path(target)
    
    if not source.exists():
        raise FileNotFoundError(f"源文件不存在: {source}")
    
    # 确保目标目录存在
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # 如果目标文件已存在，创建备份
    if target.exists() and create_backup:
        backup_path = create_backup_path(target)
        target.rename(backup_path)
    
    try:
        source.rename(target)
        return True
    except Exception as e:
        raise IOError(f"移动文件失败: {str(e)}")


def get_directory_tree(directory: Union[str, Path], max_depth: int = 3) -> Dict:
    """
    获取目录树结构
    
    Args:
        directory: 目录路径
        max_depth: 最大递归深度
        
    Returns:
        目录树字典
    """
    directory = Path(directory)
    
    def _build_tree(path: Path, current_depth: int) -> Dict:
        if current_depth > max_depth:
            return {'name': path.name, 'type': 'directory', 'children': []}
        
        tree = {
            'name': path.name,
            'type': 'directory' if path.is_dir() else 'file',
            'path': str(path)
        }
        
        if path.is_dir():
            try:
                children = []
                for item in path.iterdir():
                    if item.is_dir():
                        children.append(_build_tree(item, current_depth + 1))
                    else:
                        children.append({
                            'name': item.name,
                            'type': 'file',
                            'path': str(item),
                            'size': item.stat().st_size
                        })
                tree['children'] = children
            except PermissionError:
                tree['children'] = []
                tree['error'] = 'Permission denied'
        
        return tree
    
    return _build_tree(directory, 0)


def human_readable_time(seconds: float) -> str:
    """
    将秒数转换为人类可读的时间格式
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串
    """
    if seconds < 1:
        return f"{seconds*1000:.1f} 毫秒"
    elif seconds < 60:
        return f"{seconds:.1f} 秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} 分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} 小时"


def validate_directory_permissions(directory: Union[str, Path]) -> Tuple[bool, List[str]]:
    """
    验证目录权限
    
    Args:
        directory: 目录路径
        
    Returns:
        (是否有足够权限, 错误信息列表)
    """
    directory = Path(directory)
    errors = []
    
    try:
        # 检查是否存在
        if not directory.exists():
            errors.append("目录不存在")
            return False, errors
        
        # 检查是否为目录
        if not directory.is_dir():
            errors.append("路径不是目录")
            return False, errors
        
        # 检查读权限
        if not os.access(directory, os.R_OK):
            errors.append("缺少读取权限")
        
        # 检查写权限
        if not os.access(directory, os.W_OK):
            errors.append("缺少写入权限")
        
        # 检查执行权限（用于遍历目录）
        if not os.access(directory, os.X_OK):
            errors.append("缺少执行权限")
            
    except Exception as e:
        errors.append(f"权限检查失败: {str(e)}")
    
    return len(errors) == 0, errors


def get_available_disk_space(path: Union[str, Path]) -> int:
    """
    获取指定路径所在磁盘的可用空间
    
    Args:
        path: 路径
        
    Returns:
        可用空间字节数
    """
    import shutil
    
    try:
        total, used, free = shutil.disk_usage(str(path))
        return free
    except Exception:
        return 0  # 返回0表示无法获取


def format_datetime(dt: datetime, format_type: str = 'standard') -> str:
    """
    格式化日期时间
    
    Args:
        dt: datetime对象
        format_type: 格式类型 ('standard', 'filename', 'compact')
        
    Returns:
        格式化后的字符串
    """
    formats = {
        'standard': '%Y-%m-%d %H:%M:%S',
        'filename': '%Y%m%d_%H%M%S',
        'compact': '%Y%m%d%H%M%S'
    }
    
    fmt = formats.get(format_type, formats['standard'])
    return dt.strftime(fmt)