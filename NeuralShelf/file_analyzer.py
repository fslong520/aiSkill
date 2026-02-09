#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件分析器
负责分析文件内容、类型和关联关系，为智能整理提供决策依据
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
from utils import get_file_info, read_text_file, is_binary_file
from logger import get_logger
from config import get_config


class FileAnalyzer:
    """文件分析器主类"""
    
    def __init__(self):
        """初始化文件分析器"""
        self.logger = get_logger()
        self.config = get_config()
        self.content_keywords = self._load_content_keywords()
        # 项目工程标记
        self.project_markers = {
            '.git': 'git',
            '.idea': 'idea',
            '.vscode': 'vscode',
            'node_modules': 'nodejs',
            '.gradle': 'gradle',
            '.mvn': 'maven',
            'venv': 'python',
            '__pycache__': 'python',
            'package.json': 'nodejs',
            'pom.xml': 'maven',
            'build.gradle': 'gradle',
            'Makefile': 'make',
            'CMakeLists.txt': 'cmake'
        }
    
    def _load_content_keywords(self) -> Dict[str, List[str]]:
        """加载内容关键词库"""
        return {
            'document': [
                'document', 'report', 'manual', 'guide', 'specification',
                '合同', '协议', '说明书', '报告', '文档'
            ],
            'image': [
                'photo', 'picture', 'image', 'screenshot', 'graphic',
                '照片', '截图', '图片', '图像'
            ],
            'video': [
                'video', 'movie', 'film', 'clip', 'recording',
                '视频', '录像', '影片'
            ],
            'audio': [
                'music', 'song', 'audio', 'sound', 'track',
                '音乐', '音频', '声音'
            ],
            'archive': [
                'backup', 'archive', 'compressed', 'zip', 'rar',
                '备份', '压缩', '归档'
            ],
            'code': [
                'source', 'code', 'program', 'script', 'function',
                '源码', '代码', '程序', '脚本'
            ]
        }
    
    def analyze_file(self, file_path: Path) -> Dict[str, any]:
        """
        分析单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件分析结果字典
        """
        try:
            # 获取基本信息
            file_info = get_file_info(file_path)
            
            # 计算MD5哈希值
            file_hash = self._calculate_file_hash(file_path)
            
            # 分析文件类型
            file_type = self._analyze_file_type(file_path, file_info)
            
            # 分析内容特征
            content_features = self._analyze_content_features(file_path, file_info)
            
            # 分析时间特征
            time_features = self._analyze_time_features(file_info)
            
            # 分析命名特征
            naming_features = self._analyze_naming_features(file_path)
            
            # 检测项目工程文件
            project_info = self._detect_project_structure(file_path)
            
            # 分析内容关联性
            content_relevance = self._analyze_content_relevance(content_features, naming_features)
            
            # 综合分析结果
            analysis_result = {
                'file_info': file_info,
                'file_hash': file_hash,
                'file_type': file_type,
                'content_features': content_features,
                'time_features': time_features,
                'naming_features': naming_features,
                'project_info': project_info,
                'content_relevance': content_relevance,
                'confidence_score': self._calculate_confidence_score(
                    file_type, content_features, naming_features, project_info
                ),
                'suggested_category': self._suggest_category(
                    file_type, content_features, naming_features, project_info
                ),
                'semantic_theme': content_relevance.get('semantic_theme', 'uncategorized'),
                'tags': self._extract_tags(file_path, file_info, content_features)
            }
            
            self.logger.debug(f"文件分析完成: {file_path} -> {analysis_result['suggested_category']}")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"文件分析失败 {file_path}: {str(e)}")
            return self._create_error_result(file_path, str(e))
    
    def _analyze_file_type(self, file_path: Path, file_info: Dict) -> Dict[str, any]:
        """分析文件类型"""
        extension = file_info['suffix'].lower()
        mime_type = file_info['mime_type']
        
        # 从配置获取文件类型分类
        category = self.config.get_file_type_category(extension)
        target_folder = self.config.get_target_folder(extension)
        
        return {
            'extension': extension,
            'mime_type': mime_type,
            'category': category,
            'target_folder': target_folder,
            'is_binary': is_binary_file(file_path),
            'size_category': self._categorize_file_size(file_info['size'])
        }
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        计算文件的MD5哈希值用于去重
        
        Args:
            file_path: 文件路径
            
        Returns:
            MD5哈希字符串
        """
        try:
            md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            self.logger.debug(f"计算文件哈希失败 {file_path}: {str(e)}")
            return ""
    
    def _detect_project_structure(self, file_path: Path) -> Dict[str, any]:
        """
        检测文件是否属于项目工程结构
        
        Args:
            file_path: 文件路径
            
        Returns:
            项目信息字典
        """
        project_info = {
            'is_project_file': False,
            'project_type': None,
            'project_markers': [],
            'should_protect': False
        }
        
        try:
            # 检查文件名是否匹配项目标记
            if file_path.name in self.project_markers:
                project_info['is_project_file'] = True
                project_info['project_type'] = self.project_markers[file_path.name]
                project_info['project_markers'].append(file_path.name)
                project_info['should_protect'] = True
                return project_info
            
            # 检查文件所在目录是否有项目标记
            for part in file_path.parts:
                if part in self.project_markers:
                    project_info['is_project_file'] = True
                    project_info['project_type'] = self.project_markers[part]
                    project_info['project_markers'].append(part)
                    project_info['should_protect'] = True
            
            # 检查父目录中的项目标记
            current_dir = file_path.parent
            for _ in range(3):  # 向上查找3层
                if current_dir.exists():
                    for marker, marker_type in self.project_markers.items():
                        if (current_dir / marker).exists():
                            project_info['is_project_file'] = True
                            project_info['project_type'] = marker_type
                            project_info['project_markers'].append(marker)
                            project_info['should_protect'] = True
                    current_dir = current_dir.parent
                else:
                    break
                    
        except Exception as e:
            self.logger.debug(f"检测项目结构失败 {file_path}: {str(e)}")
        
        return project_info
    
    def _analyze_content_relevance(self, content_features: Dict, naming_features: Dict) -> Dict[str, any]:
        """
        分析文件的内容关联性和语义主题
        
        Args:
            content_features: 内容特征
            naming_features: 命名特征
            
        Returns:
            关联性分析字典
        """
        relevance = {
            'semantic_theme': 'uncategorized',
            'keywords': [],
            'related_categories': [],
            'relevance_score': 0.0
        }
        
        try:
            # 从检测到的关键词确定语义主题
            keywords = content_features.get('detected_keywords', [])
            if keywords:
                relevance['keywords'] = keywords
                
                # 根据关键词确定主题
                theme_mapping = {
                    'document': '文档',
                    'image': '图像',
                    'video': '视频',
                    'audio': '音频',
                    'archive': '归档',
                    'code': '代码'
                }
                
                for keyword in keywords:
                    for category_key, theme_name in theme_mapping.items():
                        if keyword.lower() in self.content_keywords.get(category_key, []):
                            relevance['semantic_theme'] = theme_name
                            relevance['related_categories'].append(category_key)
            
            # 从命名特征补充信息
            if naming_features.get('has_project'):
                relevance['related_categories'].append('project')
            if naming_features.get('has_date'):
                relevance['related_categories'].append('time_based')
            if naming_features.get('has_version'):
                relevance['related_categories'].append('versioned')
            
            # 计算关联性得分
            relevance['relevance_score'] = min(len(relevance['keywords']) * 0.3 + 
                                              len(relevance['related_categories']) * 0.2, 1.0)
            
        except Exception as e:
            self.logger.debug(f"分析内容关联性失败: {str(e)}")
        
        return relevance
    
    def _categorize_file_size(self, size: int) -> str:
        """根据文件大小分类"""
        if size < 1024:  # < 1KB
            return 'tiny'
        elif size < 1024 * 1024:  # < 1MB
            return 'small'
        elif size < 10 * 1024 * 1024:  # < 10MB
            return 'medium'
        elif size < 100 * 1024 * 1024:  # < 100MB
            return 'large'
        else:
            return 'huge'
    
    def _analyze_content_features(self, file_path: Path, file_info: Dict) -> Dict[str, any]:
        """分析文件内容特征"""
        features = {
            'has_text_content': False,
            'detected_keywords': [],
            'content_language': 'unknown',
            'is_temporary': False,
            'is_system_file': False
        }
        
        try:
            # 检查是否为文本文件
            if not file_info['is_binary']:
                features['has_text_content'] = True
                
                # 读取文件内容进行分析
                content = read_text_file(file_path)
                
                # 检测关键词
                detected_keywords = self._detect_content_keywords(content)
                features['detected_keywords'] = detected_keywords
                
                # 检测语言
                features['content_language'] = self._detect_language(content)
                
                # 检测是否为临时文件
                features['is_temporary'] = self._is_temporary_content(content)
                
        except Exception as e:
            self.logger.debug(f"内容分析失败 {file_path}: {str(e)}")
        
        # 检测是否为系统文件
        features['is_system_file'] = self._is_system_file(file_path.name)
        
        return features
    
    def _detect_content_keywords(self, content: str) -> List[str]:
        """检测内容中的关键词"""
        detected = []
        content_lower = content.lower()
        
        for category, keywords in self.content_keywords.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    detected.append(keyword)
                    break  # 每个类别最多记录一个关键词
        
        return detected
    
    def _detect_language(self, content: str) -> str:
        """简单语言检测"""
        # 统计中英文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_chars = len(re.findall(r'[a-zA-Z]', content))
        
        if chinese_chars > english_chars * 2:
            return 'chinese'
        elif english_chars > chinese_chars * 2:
            return 'english'
        else:
            return 'mixed'
    
    def _is_temporary_content(self, content: str) -> bool:
        """判断是否为临时内容"""
        temp_indicators = [
            'temp', 'temporary', 'draft', 'backup',
            '草稿', '临时', '备份', '暂存'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in temp_indicators)
    
    def _is_system_file(self, filename: str) -> bool:
        """判断是否为系统文件"""
        system_patterns = [
            r'^\.',  # 以点开头的隐藏文件
            r'^(Thumbs\.db|\.DS_Store)$',  # Windows/Mac系统文件
            r'\.(tmp|temp|log)$',  # 临时文件扩展名
        ]
        
        return any(re.match(pattern, filename, re.IGNORECASE) for pattern in system_patterns)
    
    def _analyze_time_features(self, file_info: Dict) -> Dict[str, any]:
        """分析时间特征"""
        now = datetime.now()
        modified_time = file_info['modified_time']
        created_time = file_info['created_time']
        
        # 计算相对时间
        days_since_modified = (now - modified_time).days
        days_since_created = (now - created_time).days
        
        return {
            'age_days': days_since_created,
            'days_since_modified': days_since_modified,
            'is_recent': days_since_modified <= 7,  # 一周内修改
            'is_old': days_since_modified >= 365,   # 一年未修改
            'time_category': self._categorize_file_age(days_since_modified)
        }
    
    def _categorize_file_age(self, days: int) -> str:
        """根据文件年龄分类"""
        if days <= 1:
            return 'today'
        elif days <= 7:
            return 'this_week'
        elif days <= 30:
            return 'this_month'
        elif days <= 90:
            return 'quarter'
        elif days <= 365:
            return 'year'
        else:
            return 'ancient'
    
    def _analyze_naming_features(self, file_path: Path) -> Dict[str, any]:
        """分析文件命名特征"""
        filename = file_path.name
        stem = file_path.stem
        
        # 提取日期信息
        date_info = self._extract_date_from_filename(filename)
        
        # 检测版本信息
        version_info = self._extract_version_info(filename)
        
        # 检测序号信息
        sequence_info = self._extract_sequence_info(filename)
        
        # 检测项目相关信息
        project_info = self._extract_project_info(filename)
        
        return {
            'has_date': date_info is not None,
            'date_info': date_info,
            'has_version': version_info is not None,
            'version_info': version_info,
            'has_sequence': sequence_info is not None,
            'sequence_info': sequence_info,
            'has_project': project_info is not None,
            'project_info': project_info,
            'naming_pattern': self._identify_naming_pattern(filename)
        }
    
    def _extract_date_from_filename(self, filename: str) -> Optional[Dict[str, any]]:
        """从文件名提取日期信息"""
        # 常见日期格式正则表达式
        date_patterns = [
            (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),  # 2024-01-15
            (r'(\d{4})(\d{2})(\d{2})', '%Y%m%d'),      # 20240115
            (r'(\d{2})-(\d{2})-(\d{4})', '%m-%d-%Y'),  # 01-15-2024
        ]
        
        for pattern, format_str in date_patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    date_str = match.group(0)
                    date_obj = datetime.strptime(date_str, format_str)
                    return {
                        'date_string': date_str,
                        'date_object': date_obj,
                        'year': date_obj.year,
                        'month': date_obj.month,
                        'day': date_obj.day
                    }
                except ValueError:
                    continue
        
        return None
    
    def _extract_version_info(self, filename: str) -> Optional[Dict[str, any]]:
        """提取版本信息"""
        version_patterns = [
            r'[vV](\d+\.\d+(?:\.\d+)?)',  # v1.2.3 或 V2.0
            r'_ver(?:sion)?[_\-]?(\d+\.\d+(?:\.\d+)?)',  # _ver1.0 或 _version_2.1
            r'\((\d+\.\d+(?:\.\d+)?)\)',   # (1.0) 或 (2.1.3)
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, filename)
            if match:
                return {
                    'version_string': match.group(0),
                    'version_number': match.group(1)
                }
        
        return None
    
    def _extract_sequence_info(self, filename: str) -> Optional[Dict[str, any]]:
        """提取序号信息"""
        # 查找数字序列
        numbers = re.findall(r'\d+', filename)
        
        if numbers:
            return {
                'sequence_numbers': [int(n) for n in numbers],
                'main_sequence': int(numbers[-1]) if numbers else None
            }
        
        return None
    
    def _extract_project_info(self, filename: str) -> Optional[Dict[str, any]]:
        """提取项目相关信息"""
        # 简单的项目名检测（假设项目名由字母组成）
        words = re.findall(r'[A-Za-z]+', filename)
        
        # 过滤掉常见的非项目词汇
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 
                       'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day',
                       'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new',
                       'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'man',
                       'men', 'put', 'too', 'use'}
        
        project_candidates = [word for word in words if word.lower() not in common_words]
        
        if project_candidates:
            return {
                'project_candidates': project_candidates,
                'likely_project': project_candidates[0] if project_candidates else None
            }
        
        return None
    
    def _identify_naming_pattern(self, filename: str) -> str:
        """识别命名模式"""
        patterns = {
            'date_based': r'\d{4}[-_]?\d{2}[-_]?\d{2}',      # 基于日期
            'version_based': r'[vV]\d+\.\d+',                # 基于版本
            'sequence_based': r'_\d+$',                      # 基于序号
            'project_based': r'^[A-Za-z]+_',                 # 基于项目
            'descriptive': r'^[A-Za-z\s]+$',                 # 描述性命名
        }
        
        for pattern_name, pattern in patterns.items():
            if re.search(pattern, filename):
                return pattern_name
        
        return 'unknown'
    
    def _calculate_confidence_score(self, file_type: Dict, content_features: Dict, 
                                  naming_features: Dict, project_info: Dict = None) -> float:
        """计算分类置信度得分"""
        score = 0.0
        
        # 文件类型置信度（最高权重）
        if file_type['category'] != 'others':
            score += 0.35
        
        # 内容特征置信度
        if content_features['detected_keywords']:
            score += 0.25
        
        # 命名特征置信度
        naming_indicators = [
            naming_features['has_date'],
            naming_features['has_version'],
            naming_features['has_project']
        ]
        score += 0.2 * sum(naming_indicators) / len(naming_indicators) if naming_indicators else 0
        
        # 项目保护提升得分
        if project_info and project_info.get('should_protect'):
            score += 0.15
        else:
            # 时间特征影响
            if naming_features['has_date']:
                score += 0.05
            
        return min(score, 1.0)  # 确保不超过1.0
    
    def _suggest_category(self, file_type: Dict, content_features: Dict, 
                         naming_features: Dict, project_info: Dict = None) -> str:
        """建议文件分类"""
        # 如果是项目文件，返回项目标记
        if project_info and project_info.get('is_project_file'):
            project_type = project_info.get('project_type', 'unknown')
            return f'ProjectFiles_{project_type}'
        
        # 优先使用配置定义的分类
        if file_type['category'] != 'others':
            return file_type['target_folder']
        
        # 基于内容关键词建议
        if content_features['detected_keywords']:
            keyword_mapping = {
                'document': 'Documents',
                'image': 'Images', 
                'video': 'Videos',
                'audio': 'Audio',
                'archive': 'Archives',
                'code': 'Code'
            }
            
            for keyword in content_features['detected_keywords']:
                for category_key, folder_name in keyword_mapping.items():
                    if keyword.lower() in self.content_keywords.get(category_key, []):
                        return folder_name
        
        # 基于命名特征分类
        if naming_features['has_date']:
            return 'Time_Organized'
        if naming_features['has_version']:
            return 'Versioned_Files'
        if naming_features['has_project']:
            return 'Project_Files'
        
        # 基于文件大小分类
        size_categories = {
            'tiny': 'Small_Files',
            'small': 'Regular_Files',
            'medium': 'Large_Files',
            'large': 'Big_Files',
            'huge': 'Huge_Files'
        }
        
        return size_categories.get(file_type['size_category'], 'Uncategorized')
    
    def _extract_tags(self, file_path: Path, file_info: Dict, 
                     content_features: Dict) -> List[str]:
        """提取文件标签"""
        tags = []
        
        # 基于文件类型添加标签
        if file_info['suffix']:
            tags.append(file_info['suffix'][1:].lower())  # 移除点号
        
        # 基于内容特征添加标签
        tags.extend([kw.lower() for kw in content_features['detected_keywords']])
        
        # 基于时间特征添加标签
        time_features = self._analyze_time_features(file_info)
        if time_features['is_recent']:
            tags.append('recent')
        if time_features['is_old']:
            tags.append('old')
        
        # 基于大小添加标签
        if file_info['size'] > 100 * 1024 * 1024:  # > 100MB
            tags.append('large_file')
        elif file_info['size'] < 1024:  # < 1KB
            tags.append('small_file')
        
        # 基于命名特征添加标签
        naming_features = self._analyze_naming_features(file_path)
        if naming_features['has_date']:
            tags.append('dated')
        if naming_features['has_version']:
            tags.append('versioned')
        
        return list(set(tags))  # 去重
    
    def _create_error_result(self, file_path: Path, error_message: str) -> Dict[str, any]:
        """创建错误分析结果"""
        return {
            'file_info': {
                'name': file_path.name,
                'path': str(file_path),
                'error': error_message
            },
            'file_hash': '',
            'file_type': {'category': 'error', 'target_folder': 'Errors'},
            'content_features': {},
            'time_features': {},
            'naming_features': {},
            'project_info': {'is_project_file': False, 'should_protect': False},
            'content_relevance': {'semantic_theme': 'error'},
            'confidence_score': 0.0,
            'suggested_category': 'Errors',
            'semantic_theme': 'error',
            'tags': ['error']
        }
    
    def batch_analyze(self, file_paths: List[Path]) -> List[Dict[str, any]]:
        """
        批量分析文件（增强版）
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            分析结果列表
        """
        results = []
        failed_files = []
        successful_analyses = 0
        
        self.logger.info(f"开始批量分析 {len(file_paths)} 个文件")
        
        # 按文件大小排序，优先处理小文件
        sorted_files = sorted(file_paths, key=lambda x: x.stat().st_size if x.exists() else 0)
        
        for i, file_path in enumerate(sorted_files, 1):
            try:
                # 显示进度
                if i % 100 == 1 or i == len(sorted_files):
                    progress = (i / len(sorted_files)) * 100
                    self.logger.info(f"分析进度: {i}/{len(sorted_files)} ({progress:.1f}%) - 当前文件: {file_path.name}")
                
                result = self.analyze_file(file_path)
                results.append(result)
                successful_analyses += 1
                
            except Exception as e:
                error_msg = f"分析文件失败 {file_path}: {str(e)}"
                failed_files.append((file_path, str(e)))
                self.logger.warning(error_msg)
                # 创建基本的分析记录，即使分析失败
                try:
                    basic_info = get_file_info(file_path)
                    results.append({
                        'file_info': basic_info,
                        'file_type': 'unknown',
                        'content_features': {},
                        'time_features': {},
                        'naming_features': {},
                        'confidence_score': 0.0,
                        'suggested_category': 'Uncategorized',
                        'tags': [],
                        'analysis_error': str(e)
                    })
                except Exception:
                    # 如果连基本信息都无法获取，则跳过
                    self.logger.error(f"无法获取文件基本信息: {file_path}")
                    continue
        
        # 记录分析统计
        self.logger.info(f"批量分析完成统计:")
        self.logger.info(f"  - 成功分析: {successful_analyses} 个文件")
        self.logger.info(f"  - 分析失败: {len(failed_files)} 个文件")
        
        if failed_files:
            self.logger.warning(f"分析失败的文件详情:")
            for file_path, error in failed_files[:10]:  # 显示前10个错误
                self.logger.warning(f"  {file_path.name}: {error}")
            if len(failed_files) > 10:
                self.logger.warning(f"  ... 还有 {len(failed_files) - 10} 个失败文件")
        
        return results


# 便捷函数
def analyze_single_file(file_path: str) -> Dict[str, any]:
    """分析单个文件的便捷函数"""
    analyzer = FileAnalyzer()
    return analyzer.analyze_file(Path(file_path))


def analyze_directory(directory: str, recursive: bool = True) -> List[Dict[str, any]]:
    """分析目录中所有文件"""
    directory_path = Path(directory)
    analyzer = FileAnalyzer()
    
    if recursive:
        file_paths = [f for f in directory_path.rglob('*') if f.is_file()]
    else:
        file_paths = [f for f in directory_path.iterdir() if f.is_file()]
    
    return analyzer.batch_analyze(file_paths)