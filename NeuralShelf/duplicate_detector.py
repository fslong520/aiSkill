#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重复文件检测器
基于内容哈希和相似度算法检测重复文件
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
from utils import get_file_hash, get_file_info
from logger import get_logger
from config import get_config


class DuplicateDetector:
    """重复文件检测器"""
    
    def __init__(self):
        """初始化重复文件检测器"""
        self.logger = get_logger()
        self.config = get_config()
        self.strategy = self.config.get('duplicate_strategy', 'keep_newest')
        
        # 缓存已计算的哈希值
        self.hash_cache = {}
        
        # 存储检测结果
        self.duplicate_groups = []
        self.processed_files = set()
    
    def detect_duplicates(self, file_paths: List[Path], 
                         method: str = 'content') -> List[List[Path]]:
        """
        检测重复文件组
        
        Args:
            file_paths: 文件路径列表
            method: 检测方法 ('content', 'name', 'size', 'smart')
            
        Returns:
            重复文件组列表，每组包含重复的文件路径
        """
        self.logger.info(f"开始检测重复文件，共 {len(file_paths)} 个文件")
        
        if method == 'content':
            duplicates = self._detect_by_content_hash(file_paths)
        elif method == 'name':
            duplicates = self._detect_by_name(file_paths)
        elif method == 'size':
            duplicates = self._detect_by_size(file_paths)
        elif method == 'smart':
            duplicates = self._detect_smart(file_paths)
        else:
            raise ValueError(f"不支持的检测方法: {method}")
        
        self.duplicate_groups = duplicates
        self.logger.info(f"检测到 {len(duplicates)} 组重复文件")
        
        return duplicates
    
    def _detect_by_content_hash(self, file_paths: List[Path]) -> List[List[Path]]:
        """基于内容哈希检测重复文件"""
        # 按文件大小分组，相同大小的文件才可能是重复的
        size_groups = defaultdict(list)
        for file_path in file_paths:
            try:
                file_info = get_file_info(file_path)
                size_groups[file_info['size']].append(file_path)
            except Exception as e:
                self.logger.debug(f"获取文件信息失败 {file_path}: {str(e)}")
                continue
        
        # 对每个大小组计算哈希值
        hash_groups = defaultdict(list)
        
        for size, files in size_groups.items():
            # 只对有多个文件的组进行哈希计算
            if len(files) > 1:
                for file_path in files:
                    try:
                        file_hash = self._get_file_hash_cached(file_path)
                        hash_groups[file_hash].append(file_path)
                    except Exception as e:
                        self.logger.debug(f"计算文件哈希失败 {file_path}: {str(e)}")
                        continue
        
        # 收集重复组（哈希值相同的文件）
        duplicates = []
        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                duplicates.append(files)
                self.logger.debug(f"发现内容重复组: {len(files)} 个文件，哈希: {file_hash[:16]}...")
        
        return duplicates
    
    def _detect_by_name(self, file_paths: List[Path]) -> List[List[Path]]:
        """基于文件名检测重复文件"""
        name_groups = defaultdict(list)
        
        for file_path in file_paths:
            # 使用文件名（不含扩展名）作为键
            name_key = file_path.stem.lower()
            name_groups[name_key].append(file_path)
        
        # 收集重复组
        duplicates = []
        for name_key, files in name_groups.items():
            if len(files) > 1:
                duplicates.append(files)
                self.logger.debug(f"发现名称重复组: {name_key} -> {len(files)} 个文件")
        
        return duplicates
    
    def _detect_by_size(self, file_paths: List[Path]) -> List[List[Path]]:
        """基于文件大小检测重复文件"""
        size_groups = defaultdict(list)
        
        for file_path in file_paths:
            try:
                file_info = get_file_info(file_path)
                size_groups[file_info['size']].append(file_path)
            except Exception as e:
                self.logger.debug(f"获取文件大小失败 {file_path}: {str(e)}")
                continue
        
        # 收集可能的重复组（相同大小且大于最小阈值）
        duplicates = []
        min_duplicate_size = 1024  # 1KB，避免将小文件误判为重复
        
        for size, files in size_groups.items():
            if len(files) > 1 and size > min_duplicate_size:
                duplicates.append(files)
                self.logger.debug(f"发现大小重复组: {size} bytes -> {len(files)} 个文件")
        
        return duplicates
    
    def _detect_smart(self, file_paths: List[Path]) -> List[List[Path]]:
        """智能检测：结合多种方法"""
        # 第一步：快速筛选（按大小）
        size_groups = defaultdict(list)
        for file_path in file_paths:
            try:
                file_info = get_file_info(file_path)
                size_groups[file_info['size']].append(file_path)
            except Exception:
                continue
        
        # 第二步：对候选文件进行内容哈希
        candidates = []
        for size, files in size_groups.items():
            if len(files) > 1:
                candidates.extend(files)
        
        if not candidates:
            return []
        
        # 第三步：内容哈希检测
        return self._detect_by_content_hash(candidates)
    
    def _get_file_hash_cached(self, file_path: Path, algorithm: str = 'md5') -> str:
        """获取文件哈希值（带缓存）"""
        file_key = str(file_path)
        
        if file_key not in self.hash_cache:
            self.hash_cache[file_key] = get_file_hash(file_path, algorithm)
        
        return self.hash_cache[file_key]
    
    def resolve_duplicates(self, duplicate_group: List[Path]) -> Tuple[Path, List[Path]]:
        """
        解决重复文件组，确定保留文件和待处理文件
        
        Args:
            duplicate_group: 重复文件组
            
        Returns:
            (保留的文件, 待处理的文件列表)
        """
        if len(duplicate_group) <= 1:
            return duplicate_group[0] if duplicate_group else None, []
        
        # 根据策略选择保留的文件
        if self.strategy == 'keep_newest':
            keeper, candidates = self._keep_newest(duplicate_group)
        elif self.strategy == 'keep_largest':
            keeper, candidates = self._keep_largest(duplicate_group)
        elif self.strategy == 'keep_first':
            keeper, candidates = self._keep_first(duplicate_group)
        elif self.strategy == 'keep_all':
            # 保留所有文件
            return duplicate_group[0], duplicate_group[1:]
        else:
            # 默认策略：保留最新的
            keeper, candidates = self._keep_newest(duplicate_group)
        
        self.logger.debug(f"重复文件处理决策: 保留 {keeper.name}, 处理 {len(candidates)} 个文件")
        return keeper, candidates
    
    def _keep_newest(self, files: List[Path]) -> Tuple[Path, List[Path]]:
        """保留最新的文件"""
        file_times = []
        for file_path in files:
            try:
                file_info = get_file_info(file_path)
                file_times.append((file_path, file_info['modified_time']))
            except Exception:
                file_times.append((file_path, None))
        
        # 按修改时间排序（最新的在前）
        file_times.sort(key=lambda x: x[1] if x[1] else 0, reverse=True)
        
        keeper = file_times[0][0]
        candidates = [f[0] for f in file_times[1:]]
        
        return keeper, candidates
    
    def _keep_largest(self, files: List[Path]) -> Tuple[Path, List[Path]]:
        """保留最大的文件"""
        file_sizes = []
        for file_path in files:
            try:
                file_info = get_file_info(file_path)
                file_sizes.append((file_path, file_info['size']))
            except Exception:
                file_sizes.append((file_path, 0))
        
        # 按文件大小排序（最大的在前）
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        
        keeper = file_sizes[0][0]
        candidates = [f[0] for f in file_sizes[1:]]
        
        return keeper, candidates
    
    def _keep_first(self, files: List[Path]) -> Tuple[Path, List[Path]]:
        """保留第一个文件"""
        return files[0], files[1:]
    
    def get_duplicate_statistics(self) -> Dict[str, any]:
        """获取重复文件统计信息"""
        total_duplicates = sum(len(group) for group in self.duplicate_groups)
        unique_files = len(set(file for group in self.duplicate_groups for file in group))
        
        # 按重复次数分组统计
        group_size_stats = defaultdict(int)
        for group in self.duplicate_groups:
            group_size_stats[len(group)] += 1
        
        return {
            'total_duplicate_groups': len(self.duplicate_groups),
            'total_duplicate_files': total_duplicates,
            'unique_files_involved': unique_files,
            'average_group_size': total_duplicates / len(self.duplicate_groups) if self.duplicate_groups else 0,
            'group_size_distribution': dict(group_size_stats),
            'strategy_used': self.strategy
        }
    
    def generate_duplicate_report(self) -> str:
        """生成重复文件检测报告"""
        if not self.duplicate_groups:
            return "未发现重复文件"
        
        stats = self.get_duplicate_statistics()
        report_lines = [
            "# 重复文件检测报告",
            "",
            f"## 检测统计",
            f"- 重复文件组数: {stats['total_duplicate_groups']}",
            f"- 重复文件总数: {stats['total_duplicate_files']}",
            f"- 涉及唯一文件数: {stats['unique_files_involved']}",
            f"- 平均组大小: {stats['average_group_size']:.1f}",
            f"- 处理策略: {stats['strategy_used']}",
            ""
        ]
        
        # 详细重复组信息
        report_lines.append("## 重复文件组详情")
        report_lines.append("")
        
        for i, group in enumerate(self.duplicate_groups, 1):
            report_lines.append(f"### 组 {i} ({len(group)} 个文件)")
            report_lines.append("")
            
            # 确定保留文件
            keeper, candidates = self.resolve_duplicates(group)
            
            report_lines.append("**保留文件:**")
            report_lines.append(f"- `{keeper}`")
            report_lines.append("")
            
            if candidates:
                report_lines.append("**待处理文件:**")
                for candidate in candidates:
                    report_lines.append(f"- `{candidate}`")
                report_lines.append("")
        
        return "\n".join(report_lines)
    
    def find_similar_files(self, file_paths: List[Path], 
                          similarity_threshold: float = 0.9) -> List[Tuple[Path, Path, float]]:
        """
        查找相似文件（基于内容相似度）
        
        Args:
            file_paths: 文件路径列表
            similarity_threshold: 相似度阈值
            
        Returns:
            相似文件对列表 [(file1, file2, similarity), ...]
        """
        from difflib import SequenceMatcher
        
        similar_pairs = []
        processed_pairs = set()
        
        # 只对大小相近的文件进行比较
        size_groups = defaultdict(list)
        for file_path in file_paths:
            try:
                file_info = get_file_info(file_path)
                size_group = file_info['size'] // 10240  # 按10KB分组
                size_groups[size_group].append(file_path)
            except Exception:
                continue
        
        for size_group, files in size_groups.items():
            if len(files) <= 1:
                continue
                
            # 比较同一大小组内的文件
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    pair_key = tuple(sorted([str(file1), str(file2)]))
                    if pair_key in processed_pairs:
                        continue
                    
                    processed_pairs.add(pair_key)
                    
                    try:
                        similarity = self._calculate_file_similarity(file1, file2)
                        if similarity >= similarity_threshold:
                            similar_pairs.append((file1, file2, similarity))
                    except Exception as e:
                        self.logger.debug(f"相似度计算失败 {file1} vs {file2}: {str(e)}")
                        continue
        
        # 按相似度排序
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        return similar_pairs
    
    def _calculate_file_similarity(self, file1: Path, file2: Path) -> float:
        """计算两个文件的相似度"""
        from difflib import SequenceMatcher
        
        # 对于小文件，直接比较内容
        try:
            info1 = get_file_info(file1)
            info2 = get_file_info(file2)
            
            # 如果文件很大，只比较部分内容
            max_compare_size = 102400  # 100KB
            
            if info1['size'] > max_compare_size or info2['size'] > max_compare_size:
                # 比较文件头部和尾部
                content1 = self._get_file_sample(file1, max_compare_size)
                content2 = self._get_file_sample(file2, max_compare_size)
            else:
                # 比较完整内容
                content1 = self._read_file_content_safe(file1)
                content2 = self._read_file_content_safe(file2)
            
            if content1 and content2:
                return SequenceMatcher(None, content1, content2).ratio()
            
        except Exception:
            pass
        
        return 0.0
    
    def _get_file_sample(self, file_path: Path, sample_size: int) -> str:
        """获取文件样本内容"""
        try:
            with open(file_path, 'rb') as f:
                # 读取头部
                head_content = f.read(sample_size // 2)
                # 跳到尾部附近
                f.seek(-min(sample_size // 2, file_path.stat().st_size), 2)
                tail_content = f.read()
                
                # 合并内容
                combined = head_content + tail_content
                
                # 尝试解码为文本
                try:
                    return combined.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        return combined.decode('gbk')
                    except UnicodeDecodeError:
                        return str(combined)  # 返回字节串的字符串表示
                        
        except Exception:
            return ""
    
    def _read_file_content_safe(self, file_path: Path) -> str:
        """安全地读取文件内容"""
        try:
            encodings = ['utf-8', 'gbk', 'latin1']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read(102400)  # 限制读取大小
                except UnicodeDecodeError:
                    continue
        except Exception:
            pass
        
        return ""


# 便捷函数
def detect_directory_duplicates(directory: str, method: str = 'smart') -> List[List[Path]]:
    """检测目录中的重复文件"""
    directory_path = Path(directory)
    detector = DuplicateDetector()
    
    # 获取所有文件
    file_paths = [f for f in directory_path.rglob('*') if f.is_file()]
    
    return detector.detect_duplicates(file_paths, method)


def get_duplicate_statistics(directory: str) -> Dict[str, any]:
    """获取目录重复文件统计"""
    duplicates = detect_directory_duplicates(directory)
    detector = DuplicateDetector()
    detector.duplicate_groups = duplicates
    return detector.get_duplicate_statistics()