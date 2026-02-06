#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录分析器
集成tree命令输出分析和多方案生成
"""

import subprocess
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from logger import get_logger
from config import get_config


@dataclass
class DirectoryStructure:
    """目录结构信息"""
    path: str
    name: str
    type: str  # directory, file
    size: int = 0
    children: List['DirectoryStructure'] = None
    file_count: int = 0
    dir_count: int = 0
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


@dataclass
class AnalysisScheme:
    """分析方案"""
    scheme_id: str
    name: str
    description: str
    strategy: str  # content_based, name_based, type_based, hybrid
    confidence: float
    estimated_moves: int
    estimated_time: str
    risk_level: str  # low, medium, high
    details: Dict


class DirectoryAnalyzer:
    """目录分析器主类"""
    
    def __init__(self):
        """初始化目录分析器"""
        self.logger = get_logger()
        self.config = get_config()
    
    def analyze_with_tree(self, directory: str) -> Dict[str, any]:
        """
        使用tree命令分析目录结构
        
        Args:
            directory: 目标目录
            
        Returns:
            分析结果字典
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        try:
            # 生成tree命令输出到临时文件
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # 执行tree命令
            cmd = ['tree', '-a', '-s', '-D', '--dirsfirst', '-o', temp_filename, str(directory_path)]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    self.logger.warning(f"tree命令执行警告: {result.stderr}")
            except subprocess.TimeoutExpired:
                self.logger.warning("tree命令执行超时，使用备用方法")
                self._generate_tree_fallback(directory_path, temp_filename)
            except FileNotFoundError:
                self.logger.info("未找到tree命令，使用备用方法生成目录结构")
                self._generate_tree_fallback(directory_path, temp_filename)
            
            # 读取tree输出
            with open(temp_filename, 'r', encoding='utf-8', errors='ignore') as f:
                tree_output = f.read()
            
            # 清理临时文件
            Path(temp_filename).unlink()
            
            # 分析tree输出
            structure = self._parse_tree_output(tree_output, directory_path)
            statistics = self._calculate_directory_statistics(structure)
            
            # 生成多种整理方案
            schemes = self._generate_organization_schemes(structure, statistics)
            
            return {
                'directory': str(directory_path),
                'analysis_time': datetime.now().isoformat(),
                'tree_output': tree_output,
                'structure': structure,
                'statistics': statistics,
                'schemes': schemes,
                'recommendation': self._get_best_scheme(schemes)
            }
            
        except Exception as e:
            self.logger.error(f"目录分析失败: {str(e)}")
            raise
    
    def _generate_tree_fallback(self, directory_path: Path, output_file: str):
        """备用方法生成类似tree的输出"""
        def walk_directory(path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
            lines = []
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                
                for i, item in enumerate(items):
                    is_last_item = (i == len(items) - 1)
                    connector = "└── " if is_last_item else "├── "
                    
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            lines.append(f"{prefix}{connector}{item.name} [{size} bytes]")
                        else:
                            lines.append(f"{prefix}{connector}{item.name}/")
                            if not is_last_item:
                                lines.extend(walk_directory(item, prefix + "│   ", is_last_item))
                            else:
                                lines.extend(walk_directory(item, prefix + "    ", is_last_item))
                    except (PermissionError, OSError) as e:
                        lines.append(f"{prefix}{connector}{item.name} [无法访问: {str(e)}]")
                        
            except PermissionError:
                lines.append(f"{prefix}└── [权限不足]")
            
            return lines
        
        # 生成目录树文本
        tree_lines = [f"{directory_path.name}/"]
        tree_lines.extend(walk_directory(directory_path))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(tree_lines))
    
    def _parse_tree_output(self, tree_output: str, root_path: Path) -> DirectoryStructure:
        """解析tree命令输出"""
        lines = tree_output.strip().split('\n')
        if not lines:
            return DirectoryStructure(str(root_path), root_path.name, 'directory')
        
        # 创建根节点
        root = DirectoryStructure(str(root_path), root_path.name, 'directory')
        node_stack = [(0, root)]  # (indent_level, node)
        
        for line in lines[1:]:  # 跳过第一行（根目录名）
            if not line.strip():
                continue
                
            # 计算缩进级别
            indent = len(line) - len(line.lstrip())
            level = indent // 4  # 假设每个缩进级别是4个空格
            
            # 提取文件/目录信息
            content = line.strip()
            if not content:
                continue
            
            # 解析文件名和大小
            name_part = content
            size = 0
            
            # 检查是否包含大小信息
            if '[' in content and ']' in content:
                bracket_start = content.rfind('[')
                bracket_end = content.rfind(']')
                if bracket_start != -1 and bracket_end != -1:
                    size_info = content[bracket_start+1:bracket_end]
                    name_part = content[:bracket_start].strip()
                    # 提取数字大小
                    if 'bytes' in size_info:
                        try:
                            size_str = size_info.replace('bytes', '').strip()
                            size = int(size_str)
                        except ValueError:
                            pass
            
            # 确定类型
            is_directory = name_part.endswith('/')
            if is_directory:
                name_part = name_part[:-1]  # 移除末尾的 '/'
            
            # 创建节点
            node = DirectoryStructure(
                path="",  # 路径稍后填充
                name=name_part,
                type='directory' if is_directory else 'file',
                size=size
            )
            
            # 找到父节点
            while node_stack and node_stack[-1][0] >= level:
                node_stack.pop()
            
            if node_stack:
                parent_node = node_stack[-1][1]
                parent_node.children.append(node)
                parent_node.file_count += 1 if node.type == 'file' else 0
                parent_node.dir_count += 1 if node.type == 'directory' else 0
            
            # 更新栈
            if is_directory:
                node_stack.append((level, node))
        
        return root
    
    def _calculate_directory_statistics(self, structure: DirectoryStructure) -> Dict:
        """计算目录统计信息"""
        def traverse(node: DirectoryStructure) -> Tuple[int, int, int, int]:
            total_files = 0
            total_dirs = 0
            total_size = 0
            max_depth = 0
            
            if node.type == 'file':
                total_files = 1
                total_size = node.size
            else:
                total_dirs = 1
                for child in node.children:
                    files, dirs, size, depth = traverse(child)
                    total_files += files
                    total_dirs += dirs
                    total_size += size
                    max_depth = max(max_depth, depth + 1)
            
            return total_files, total_dirs, total_size, max_depth
        
        files, dirs, size, depth = traverse(structure)
        
        return {
            'total_files': files,
            'total_directories': dirs,
            'total_size_bytes': size,
            'max_depth': depth,
            'average_files_per_directory': files / max(dirs, 1),
            'size_distribution': self._analyze_size_distribution(structure)
        }
    
    def _analyze_size_distribution(self, structure: DirectoryStructure) -> Dict:
        """分析文件大小分布"""
        sizes = []
        
        def collect_sizes(node: DirectoryStructure):
            if node.type == 'file' and node.size > 0:
                sizes.append(node.size)
            elif node.type == 'directory':
                for child in node.children:
                    collect_sizes(child)
        
        collect_sizes(structure)
        
        if not sizes:
            return {}
        
        # 分类统计
        categories = {
            'tiny': 0,      # < 1KB
            'small': 0,     # 1KB - 1MB
            'medium': 0,    # 1MB - 10MB
            'large': 0,     # 10MB - 100MB
            'huge': 0       # > 100MB
        }
        
        for size in sizes:
            if size < 1024:
                categories['tiny'] += 1
            elif size < 1024 * 1024:
                categories['small'] += 1
            elif size < 10 * 1024 * 1024:
                categories['medium'] += 1
            elif size < 100 * 1024 * 1024:
                categories['large'] += 1
            else:
                categories['huge'] += 1
        
        return categories
    
    def _generate_organization_schemes(self, structure: DirectoryStructure, 
                                     statistics: Dict) -> List[AnalysisScheme]:
        """生成多种整理方案"""
        schemes = []
        
        # 方案1: 按文件类型分类
        type_scheme = self._generate_type_based_scheme(structure, statistics)
        schemes.append(type_scheme)
        
        # 方案2: 按文件大小分类
        size_scheme = self._generate_size_based_scheme(structure, statistics)
        schemes.append(size_scheme)
        
        # 方案3: 按修改时间分类
        time_scheme = self._generate_time_based_scheme(structure, statistics)
        schemes.append(time_scheme)
        
        # 方案4: 混合智能分类
        hybrid_scheme = self._generate_hybrid_scheme(structure, statistics)
        schemes.append(hybrid_scheme)
        
        return schemes
    
    def _generate_type_based_scheme(self, structure: DirectoryStructure, 
                                  statistics: Dict) -> AnalysisScheme:
        """生成基于文件类型的方案"""
        return AnalysisScheme(
            scheme_id="type_based",
            name="按文件类型分类",
            description="根据文件扩展名和类型将文件分类到不同的目录",
            strategy="type_based",
            confidence=0.85,
            estimated_moves=statistics['total_files'] // 2,
            estimated_time=f"{statistics['total_files'] * 0.1:.1f} 秒",
            risk_level="low",
            details={
                'categories': ['Documents', 'Images', 'Videos', 'Audio', 'Archives', 'Code', 'Others'],
                'logic': '基于文件扩展名识别文件类型'
            }
        )
    
    def _generate_size_based_scheme(self, structure: DirectoryStructure, 
                                  statistics: Dict) -> AnalysisScheme:
        """生成基于文件大小的方案"""
        return AnalysisScheme(
            scheme_id="size_based",
            name="按文件大小分类",
            description="根据文件大小将文件分类到不同大小级别的目录",
            strategy="size_based",
            confidence=0.75,
            estimated_moves=statistics['total_files'] // 3,
            estimated_time=f"{statistics['total_files'] * 0.15:.1f} 秒",
            risk_level="medium",
            details={
                'categories': ['Tiny_Files', 'Small_Files', 'Medium_Files', 'Large_Files', 'Huge_Files'],
                'logic': '基于文件大小进行分级存储'
            }
        )
    
    def _generate_time_based_scheme(self, structure: DirectoryStructure, 
                                  statistics: Dict) -> AnalysisScheme:
        """生成基于时间的方案"""
        return AnalysisScheme(
            scheme_id="time_based",
            name="按时间分类",
            description="根据文件创建或修改时间按年月日进行分类",
            strategy="time_based",
            confidence=0.80,
            estimated_moves=statistics['total_files'] // 1.5,
            estimated_time=f"{statistics['total_files'] * 0.12:.1f} 秒",
            risk_level="medium",
            details={
                'categories': ['By_Year', 'By_Month', 'By_Day'],
                'logic': '基于文件时间戳进行时间序列分类'
            }
        )
    
    def _generate_hybrid_scheme(self, structure: DirectoryStructure, 
                              statistics: Dict) -> AnalysisScheme:
        """生成混合智能方案"""
        return AnalysisScheme(
            scheme_id="hybrid",
            name="智能混合分类",
            description="结合文件类型、大小、时间和内容特征的综合分类方案",
            strategy="hybrid",
            confidence=0.90,
            estimated_moves=statistics['total_files'] // 1.2,
            estimated_time=f"{statistics['total_files'] * 0.18:.1f} 秒",
            risk_level="low",
            details={
                'categories': ['Work_Documents', 'Media_Files', 'Development', 'Archives', 'Personal'],
                'logic': '多维度AI智能分析和分类'
            }
        )
    
    def _get_best_scheme(self, schemes: List[AnalysisScheme]) -> AnalysisScheme:
        """获取最佳方案"""
        # 按置信度和风险级别排序
        try:
            sorted_schemes = sorted(schemes, 
                                  key=lambda x: (x.confidence, 
                                               {'low': 3, 'medium': 2, 'high': 1}[x.risk_level]),
                                  reverse=True)
            return sorted_schemes[0] if sorted_schemes else schemes[0]
        except Exception as e:
            self.logger.error(f"排序方案时出错: {str(e)}")
            # 返回第一个方案作为备选
            return schemes[0] if schemes else None
    
    def save_analysis_report(self, analysis_result: Dict, format_type: str = 'markdown') -> str:
        """保存分析报告"""
        from reporter import ReportGenerator
        
        generator = ReportGenerator()
        
        if format_type == 'markdown':
            content = self._generate_markdown_report(analysis_result)
        elif format_type == 'json':
            content = json.dumps(analysis_result, indent=2, ensure_ascii=False)
        else:
            content = str(analysis_result)
        
        report_path = generator.save_report(content, 'directory_analysis', format_type)
        return report_path
    
    def _generate_markdown_report(self, analysis_result: Dict) -> str:
        """生成Markdown格式的分析报告"""
        stats = analysis_result['statistics']
        schemes = analysis_result['schemes']
        recommendation = analysis_result['recommendation']
        
        report = f"""# 目录结构分析报告

## 基本信息
- **分析目录**: `{analysis_result['directory']}`
- **分析时间**: {analysis_result['analysis_time']}
- **总文件数**: {stats['total_files']}
- **总目录数**: {stats['total_directories']}
- **总大小**: {stats['total_size_bytes']:,} 字节
- **最大深度**: {stats['max_depth']} 层

## 文件大小分布
"""
        
        size_dist = stats['size_distribution']
        for category, count in size_dist.items():
            if count > 0:
                report += f"- **{category.capitalize()}**: {count} 个文件\n"
        
        report += "\n## 整理方案对比\n\n"
        report += "| 方案名称 | 置信度 | 预估移动 | 预估时间 | 风险级别 |\n"
        report += "|---------|--------|----------|----------|----------|\n"
        
        for scheme in schemes:
            risk_icon = {'low': '✅', 'medium': '⚠️', 'high': '❌'}[scheme.risk_level]
            report += f"| {scheme.name} | {scheme.confidence:.2f} | {scheme.estimated_moves} | {scheme.estimated_time} | {risk_icon} {scheme.risk_level} |\n"
        
        report += f"\n## 推荐方案\n\n"
        report += f"**{recommendation.name}**\n\n"
        report += f"- **描述**: {recommendation.description}\n"
        report += f"- **策略**: {recommendation.strategy}\n"
        report += f"- **置信度**: {recommendation.confidence:.2f}\n"
        report += f"- **风险级别**: {recommendation.risk_level}\n\n"
        
        report += "## 方案详情\n\n"
        for scheme in schemes:
            report += f"### {scheme.name}\n"
            report += f"- **逻辑**: {scheme.details.get('logic', 'N/A')}\n"
            report += f"- **分类**: {', '.join(scheme.details.get('categories', []))}\n\n"
        
        return report


# 便捷函数
def analyze_directory_structure(directory: str) -> Dict[str, any]:
    """
    分析目录结构的便捷函数
    
    Args:
        directory: 目录路径
        
    Returns:
        分析结果
    """
    analyzer = DirectoryAnalyzer()
    return analyzer.analyze_with_tree(directory)


def generate_organization_schemes(directory: str) -> List[AnalysisScheme]:
    """
    生成整理方案
    
    Args:
        directory: 目录路径
        
    Returns:
        方案列表
    """
    analyzer = DirectoryAnalyzer()
    result = analyzer.analyze_with_tree(directory)
    return result['schemes']