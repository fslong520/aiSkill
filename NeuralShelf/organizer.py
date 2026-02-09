#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理引擎
核心整理逻辑，协调各组件完成文件整理任务
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict

from config import get_config
from logger import get_logger, OperationTimer
from file_analyzer import FileAnalyzer
from duplicate_detector import DuplicateDetector
from backup_manager import get_backup_manager, BackupRecord
from directory_analyzer import DirectoryAnalyzer
from utils import (
    get_file_info, safe_move_file, validate_directory_permissions,
    get_available_disk_space, format_file_size
)


@dataclass
class OrganizeOperation:
    """整理操作记录"""
    source_path: str
    target_path: str
    action: str  # move, copy, skip, duplicate
    file_size: int
    timestamp: datetime
    success: bool
    session_id: Optional[str] = None
    backup_path: Optional[str] = None
    file_hash: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class OrganizeStatistics:
    """整理统计信息"""
    total_files: int = 0
    processed_files: int = 0
    moved_files: int = 0
    skipped_files: int = 0
    duplicate_files: int = 0
    error_files: int = 0
    total_size: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def duration(self) -> float:
        """总耗时（秒）"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    @property
    def success_rate(self) -> float:
        """成功率"""
        if self.processed_files == 0:
            return 0.0
        return (self.moved_files + self.skipped_files) / self.processed_files


class FileOrganizer:
    """文件整理引擎主类"""
    
    def __init__(self, target_directory: str, config_file: Optional[str] = None):
        """
        初始化文件整理器
        
        Args:
            target_directory: 目标整理目录
            config_file: 配置文件路径
        """
        self.target_directory = Path(target_directory).resolve()
        self.config = get_config(config_file)
        self.logger = get_logger()
        
        # 更新配置中的目标目录
        self.config.set('target_directory', str(self.target_directory))
        
        # 初始化组件
        self.analyzer = FileAnalyzer()
        self.duplicate_detector = DuplicateDetector()
        self.backup_manager = get_backup_manager()
        self.directory_analyzer = DirectoryAnalyzer()
        
        # 操作记录
        self.operations: List[OrganizeOperation] = []
        self.statistics = OrganizeStatistics()
        self.session_id: Optional[str] = None
        
        # 验证目标目录
        self._validate_target_directory()
    
    def _validate_target_directory(self):
        """验证目标目录"""
        has_permission, errors = validate_directory_permissions(self.target_directory)
        
        if not has_permission:
            error_msg = f"目标目录权限不足: {'; '.join(errors)}"
            self.logger.error(error_msg)
            raise PermissionError(error_msg)
        
        self.logger.info(f"目标目录验证通过: {self.target_directory}")
    
    def _deduplicate_files(self, file_paths: List[Path]) -> Tuple[List[Path], Dict[str, str]]:
        """
        去重文件速平
        
        Args:
            file_paths: 原始文件路径列表
            
        Returns:
            (不重文件路径列表, MD5哈希到路径的映射)
        """
        self.logger.info(f"开始去重: 扫描 {len(file_paths)} 个文件")
        
        hash_map: Dict[str, str] = {}  # MD5哈希 -> 文件路径
        duplicate_map: Dict[str, str] = {}  # 重复文件 -> 原例
        unique_files: List[Path] = []
        
        for file_path in file_paths:
            try:
                # 计算MD5哈希
                file_hash = self._calculate_file_hash(file_path)
                if not file_hash:
                    unique_files.append(file_path)
                    continue
                
                # 检查是否已存在
                if file_hash in hash_map:
                    # 这是一个重复文件
                    duplicate_map[str(file_path)] = hash_map[file_hash]
                    self.logger.debug(f"检测到重复: {file_path.name} ← {Path(hash_map[file_hash]).name}")
                else:
                    # 新的不重文件
                    hash_map[file_hash] = str(file_path)
                    unique_files.append(file_path)
                    
            except Exception as e:
                self.logger.warning(f"去重检查失败 {file_path}: {str(e)}")
                unique_files.append(file_path)  # 失败会保留文件
        
        self.logger.info(f"去重结果: 原始 {len(file_paths)} -> 不重 {len(unique_files)} 个文件、检测到 {len(duplicate_map)} 个重复")
        return unique_files, duplicate_map
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        计算文件MD5哈希
        
        Args:
            file_path: 文件路径
            
        Returns:
            MD5哈希字符串
        """
        import hashlib
        try:
            md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            self.logger.warning(f"计算哈希失败 {file_path}: {str(e)}")
            return ""
    
    def _group_by_content_relevance(self, analyzed_files: List[Dict]) -> Dict[str, List[Dict]]:
        """
        根据内容相关性分组文件
        
        Args:
            analyzed_files: 分析完的文件列表
            
        Returns:
            主题 -> 文件列表的字典
        """
        self.logger.info(f"开始按内容相关性分组: {len(analyzed_files)} 个文件")
        
        groups: Dict[str, List[Dict]] = {}
        project_files: List[Dict] = []  # 项目文件专项
        
        for file_analysis in analyzed_files:
            # 优先保护项目文件
            if file_analysis.get('project_info', {}).get('should_protect'):
                project_files.append(file_analysis)
                continue
            
            # 根据语义主题分组
            semantic_theme = file_analysis.get('semantic_theme', 'uncategorized')
            if semantic_theme not in groups:
                groups[semantic_theme] = []
            groups[semantic_theme].append(file_analysis)
        
        # 项目文件单独分组
        if project_files:
            groups['ProjectFiles'] = project_files
        
        self.logger.info(f"分组完成: {len(groups)} 个主题组")
        for theme, files in groups.items():
            self.logger.info(f"  {theme}: {len(files)} 个文件")
        
        return groups
    
    def _calculate_success_metrics(self, original_count: int, unique_count: int, organized_count: int, 
                                 backup_count: int, protected_count: int = 0) -> Dict[str, any]:
        """
        计算成功判定指标
        
        Args:
            original_count: 原始文件数
            unique_count: 去重后文件数
            organized_count: 整理后文件数
            backup_count: 备份文件数
            protected_count: 受保护的项目文件数
            
        Returns:
            成功指标字典
        """
        # 判断成功条件
        success = (organized_count == unique_count) and (backup_count >= 0)
        
        metrics = {
            'original_count': original_count,
            'unique_count': unique_count,
            'organized_count': organized_count,
            'backup_count': backup_count,
            'protected_count': protected_count,
            'duplicates_removed': original_count - unique_count,
            'success': success,
            'message': f"整理{'' if success else '不'}'成功: 原始{original_count} → 不重{unique_count} → 整理{organized_count}"
        }
        
        return metrics
    
    def enhanced_analyze_directory(self) -> Dict[str, any]:
        """
        增强目录分析：集成tree命令输出分析和多方案生成
        
        Returns:
            增强分析结果
        """
        self.logger.operation_start("增强目录分析", str(self.target_directory))
        
        try:
            # 执行增强目录分析
            analysis_result = self.directory_analyzer.analyze_with_tree(str(self.target_directory))
            
            # 保存分析报告
            report_path = self.directory_analyzer.save_analysis_report(analysis_result, 'markdown')
            
            # 生成方案预览
            scheme_previews = []
            for scheme in analysis_result['schemes']:
                preview = self._generate_scheme_preview(scheme, analysis_result['statistics'])
                scheme_previews.append(preview)
            
            result = {
                'success': True,
                'message': '增强目录分析完成',
                'directory': str(self.target_directory),
                'analysis_result': analysis_result,
                'scheme_previews': scheme_previews,
                'recommended_scheme': analysis_result['recommendation'],
                'report_path': report_path
            }
            
            self.logger.operation_complete(
                "增强目录分析",
                0,
                {
                    '总文件数': analysis_result['statistics']['total_files'],
                    '方案数量': len(analysis_result['schemes']),
                    '推荐方案': analysis_result['recommendation']['name']
                }
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"增强目录分析失败: {str(e)}")
            return {
                'success': False,
                'message': f"分析失败: {str(e)}"
            }
    
    def _generate_scheme_preview(self, scheme: 'AnalysisScheme', statistics: Dict) -> Dict[str, any]:
        """生成方案预览"""
        return {
            'scheme_id': scheme.scheme_id,
            'name': scheme.name,
            'description': scheme.description,
            'confidence': scheme.confidence,
            'risk_level': scheme.risk_level,
            'estimated_moves': scheme.estimated_moves,
            'estimated_time': scheme.estimated_time,
            'details': scheme.details,
            'preview_stats': {
                'files_to_move': min(scheme.estimated_moves, statistics['total_files']),
                'directories_to_create': len(scheme.details.get('categories', [])),
                'space_efficiency': '高' if scheme.confidence > 0.8 else '中' if scheme.confidence > 0.6 else '低'
            }
        }
    
    def smart_organize(self, analyze_only: bool = False, plan_only: bool = False, 
                      execute_plan: Optional[str] = None, dry_run: bool = False) -> Dict[str, any]:
        """
        四阶段智能整理
        
        Args:
            analyze_only: 仅执行分析阶段
            plan_only: 仅生成整理方案
            execute_plan: 执行指定的整理方案文件
            dry_run: 是否为试运行模式
            
        Returns:
            整理结果字典
        """
        self.logger.operation_start("四阶段智能整理", str(self.target_directory))
        
        try:
            # 阶段一：启动备份会话
            self.session_id = self.backup_manager.start_session(str(self.target_directory))
            self.logger.info(f"📋 阶段一：启动备份会话 {self.session_id}")
            
            # 阶段二：文件分析
            with OperationTimer("文件分析", self.logger):
                file_paths = self._scan_files()
                self.statistics.total_files = len(file_paths)
                self.logger.info(f"📊 扫描到 {len(file_paths)} 个文件")
                
                if not file_paths:
                    self.logger.warning("目标目录中没有找到文件")
                    self.backup_manager.cancel_session()
                    return self._create_result_dict(success=True, message="目录为空")
                
                analyzed_files = self._analyze_files(file_paths)
                self.logger.info(f"🔍 文件分析完成，识别出 {len(analyzed_files)} 个文件的特征")
            
            if analyze_only:
                self.backup_manager.cancel_session()
                return self._create_analysis_result(analyzed_files)
            
            # 阶段三：生成整理方案
            with OperationTimer("AI决策", self.logger):
                plan = self._generate_smart_plan(analyzed_files, file_paths)
                self.logger.info(f"🧠 AI决策完成，生成整理方案")
                
                if plan_only:
                    plan_file = self._save_plan(plan)
                    self.backup_manager.cancel_session()
                    return self._create_plan_result(plan, plan_file)
                
                if execute_plan:
                    plan = self._load_plan(execute_plan)
            
            # 阶段四：安全执行
            with OperationTimer("安全执行", self.logger):
                self._execute_smart_plan(plan, dry_run)
            
            # 完成会话
            self.backup_manager.complete_session({
                'moved_files': self.statistics.moved_files,
                'skipped_files': self.statistics.skipped_files,
                'duplicate_files': self.statistics.duplicate_files,
                'error_files': self.statistics.error_files
            })
            
            # 完成统计
            self.statistics.end_time = datetime.now()
            
            # 生成结果
            result = self._create_smart_result(
                success=True,
                message=f"智能整理完成，处理 {self.statistics.processed_files} 个文件",
                plan=plan,
                dry_run=dry_run
            )
            
            self.logger.operation_complete(
                "四阶段智能整理", 
                self.statistics.duration,
                {
                    '处理文件': self.statistics.processed_files,
                    '移动文件': self.statistics.moved_files,
                    '跳过文件': self.statistics.skipped_files,
                    '重复文件': self.statistics.duplicate_files,
                    '错误文件': self.statistics.error_files
                }
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"智能整理过程出错: {str(e)}")
            if self.session_id:
                self.backup_manager.cancel_session()
            return self._create_result_dict(
                success=False,
                message=f"整理失败: {str(e)}"
            )
    
    def _scan_files(self) -> List[Path]:
        """扫描目标目录中的文件（增强版）"""
        exclude_patterns = self.config.get('exclude_patterns', [])
        exclude_dirs = self.config.get('exclude_directories', [])
        
        file_paths = []
        skipped_items = []
        error_items = []
        
        self.logger.info(f"开始深度扫描目录: {self.target_directory}")
        
        try:
            # 使用os.walk进行更可靠的扫描
            for root, dirs, files in os.walk(self.target_directory, followlinks=True):
                root_path = Path(root)
                
                # 检查目录是否应该被排除
                should_skip_dir = False
                for exclude_dir in exclude_dirs:
                    if exclude_dir in root_path.parts:
                        should_skip_dir = True
                        skipped_items.append((root_path, "excluded_directory"))
                        break
                
                if should_skip_dir:
                    dirs.clear()  # 不进入子目录
                    continue
                
                # 处理文件
                for file_name in files:
                    file_path = root_path / file_name
                    
                    try:
                        # 检查基本排除模式
                        should_exclude = False
                        for pattern in exclude_patterns:
                            if file_path.match(pattern):
                                should_exclude = True
                                skipped_items.append((file_path, f"pattern_match:{pattern}"))
                                break
                        
                        # 检查文件属性
                        if not should_exclude:
                            try:
                                stat_info = file_path.stat()
                                # 跳过非常小的文件（可能是系统文件）
                                if stat_info.st_size < 1:  # 小于1字节
                                    should_exclude = True
                                    skipped_items.append((file_path, "zero_size"))
                                # 跳过隐藏文件（可选）
                                elif file_name.startswith('.') and not self.config.get('include_hidden', False):
                                    should_exclude = True
                                    skipped_items.append((file_path, "hidden_file"))
                            except (OSError, PermissionError) as e:
                                error_items.append((file_path, f"stat_error:{str(e)}"))
                                should_exclude = True
                        
                        if not should_exclude:
                            file_paths.append(file_path)
                            
                    except Exception as e:
                        error_items.append((file_path, f"processing_error:{str(e)}"))
                        self.logger.debug(f"处理文件时出错 {file_path}: {str(e)}")
                        continue
                
                # 限制递归深度（可配置）
                max_depth = self.config.get('max_scan_depth', 10)
                current_depth = len(root_path.relative_to(self.target_directory).parts)
                if current_depth >= max_depth:
                    dirs.clear()
            
            # 记录扫描统计
            self.logger.info(f"扫描完成统计:")
            self.logger.info(f"  - 发现文件: {len(file_paths)} 个")
            self.logger.info(f"  - 跳过项目: {len(skipped_items)} 个")
            self.logger.info(f"  - 错误项目: {len(error_items)} 个")
            
            # 如果启用了详细日志，记录跳过的文件
            if self.config.get('verbose_scan_log', False) and skipped_items:
                self.logger.debug("跳过的文件详情:")
                for item, reason in skipped_items[:10]:  # 只显示前10个
                    self.logger.debug(f"  {item} - {reason}")
                if len(skipped_items) > 10:
                    self.logger.debug(f"  ... 还有 {len(skipped_items) - 10} 个跳过项")
            
            # 记录错误文件
            if error_items:
                self.logger.warning(f"扫描过程中遇到 {len(error_items)} 个错误文件")
                for item, error in error_items[:5]:  # 只显示前5个错误
                    self.logger.debug(f"  {item} - {error}")
            
        except Exception as e:
            self.logger.error(f"文件扫描失败: {str(e)}")
            raise
        
        return file_paths
    
    def _analyze_files(self, file_paths: List[Path]) -> List[Dict[str, any]]:
        """分析文件"""
        return self.analyzer.batch_analyze(file_paths)
    
    def _detect_duplicates(self, file_paths: List[Path]) -> List[List[Path]]:
        """检测重复文件"""
        method = self.config.get('duplicate_detection_method', 'smart')
        return self.duplicate_detector.detect_duplicates(file_paths, method)
    
    def _process_files(self, analyzed_files: List[Dict], 
                      duplicates: List[List[Path]], dry_run: bool):
        """处理文件"""
        # 创建重复文件映射
        duplicate_map = {}
        for group in duplicates:
            keeper, candidates = self.duplicate_detector.resolve_duplicates(group)
            for candidate in candidates:
                duplicate_map[str(candidate)] = str(keeper)
        
        # 处理每个文件
        for file_analysis in analyzed_files:
            try:
                self._process_single_file(file_analysis, duplicate_map, dry_run)
            except Exception as e:
                self.logger.error(f"处理文件失败 {file_analysis['file_info']['path']}: {str(e)}")
                self._record_operation(
                    source_path=file_analysis['file_info']['path'],
                    target_path="",
                    action="error",
                    file_size=file_analysis['file_info']['size'],
                    success=False,
                    error_message=str(e)
                )
                self.statistics.error_files += 1
    
    def _process_single_file(self, file_analysis: Dict, 
                           duplicate_map: Dict[str, str], dry_run: bool):
        """处理单个文件"""
        file_info = file_analysis['file_info']
        file_path = Path(file_info['path'])
        
        self.statistics.processed_files += 1
        self.statistics.total_size += file_info['size']
        
        # 检查是否为重复文件
        if str(file_path) in duplicate_map:
            self._handle_duplicate_file(file_path, duplicate_map[str(file_path)], dry_run)
            return
        
        # 确定目标路径
        target_path = self._determine_target_path(file_analysis)
        
        # 检查是否需要移动
        if file_path == target_path:
            self._record_operation(
                source_path=str(file_path),
                target_path=str(target_path),
                action="skip",
                file_size=file_info['size'],
                success=True
            )
            self.statistics.skipped_files += 1
            return
        
        # 执行移动
        self._move_file(file_path, target_path, dry_run)
    
    def _handle_duplicate_file(self, file_path: Path, keeper_path: str, dry_run: bool):
        """处理重复文件"""
        strategy = self.config.get('duplicate_strategy', 'keep_newest')
        
        if strategy == 'keep_all':
            # 保留所有文件，正常处理
            return
        
        # 移动重复文件到隔离目录
        isolation_dir = self.target_directory / 'Duplicates_Isolated'
        target_path = isolation_dir / file_path.name
        
        self._move_file(file_path, target_path, dry_run, action="duplicate")
        self.statistics.duplicate_files += 1
    
    def _determine_target_path(self, file_analysis: Dict) -> Path:
        """确定文件的目标路径"""
        file_info = file_analysis['file_info']
        file_path = Path(file_info['path'])
        
        # 获取建议的分类目录
        category = file_analysis['suggested_category']
        target_dir = self.target_directory / category
        
        # 应用命名规范
        naming_pattern = self.config.get_naming_pattern(file_info['suffix'])
        new_filename = self._apply_naming_pattern(file_path.name, file_analysis, naming_pattern)
        
        return target_dir / new_filename
    
    def _apply_naming_pattern(self, filename: str, file_analysis: Dict, pattern: str) -> str:
        """应用命名规范"""
        file_info = file_analysis['file_info']
        naming_features = file_analysis['naming_features']
        
        # 替换占位符
        result = pattern
        
        # 基本替换
        result = result.replace('{filename}', filename)
        result = result.replace('{category}', file_analysis['suggested_category'])
        
        # 时间相关替换
        now = datetime.now()
        result = result.replace('{year}', now.strftime('%Y'))
        result = result.replace('{month}', now.strftime('%m'))
        result = result.replace('{day}', now.strftime('%d'))
        
        # 文件名相关替换
        result = result.replace('{name}', file_info['stem'])
        result = result.replace('{ext}', file_info['suffix'][1:] if file_info['suffix'] else '')
        
        # 命名特征替换
        if naming_features['has_date'] and naming_features['date_info']:
            date_info = naming_features['date_info']
            result = result.replace('{file_year}', str(date_info['year']))
            result = result.replace('{file_month}', f"{date_info['month']:02d}")
            result = result.replace('{file_day}', f"{date_info['day']:02d}")
        
        if naming_features['has_version'] and naming_features['version_info']:
            result = result.replace(
                '{version}', 
                naming_features['version_info']['version_number']
            )
        
        if naming_features['has_project'] and naming_features['project_info']:
            result = result.replace(
                '{project}', 
                naming_features['project_info']['likely_project'] or 'unknown'
            )
        
        return result
    
    def _move_file(self, source_path: Path, target_path: Path, 
                   dry_run: bool, action: str = "move"):
        """移动文件（适应新的移动-复制备份策略）"""
        try:
            # 确保目标目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            backup_path = None
            file_hash = None
            
            if dry_run:
                # 试运行模式：只记录操作，不实际移动
                self.logger.info(f"[试运行] {action}: {source_path} → {target_path}")
                success = True
                error_msg = None
            else:
                # 实际操作：从备份位置复制文件到目标位置
                if self.session_id and action == "move":
                    # 查找该文件的备份记录
                    backup_record = self._find_backup_record(str(source_path))
                    if backup_record:
                        backup_path = backup_record.backup_path
                        file_hash = backup_record.file_hash
                        
                        # 从备份位置复制文件到新位置
                        if Path(backup_path).exists():
                            shutil.copy2(str(backup_path), str(target_path))
                            success = True
                            self.logger.debug(f"从备份复制文件: {backup_path} → {target_path}")
                        else:
                            success = False
                            error_msg = f"备份文件不存在: {backup_path}"
                            self.logger.error(error_msg)
                    else:
                        # 如果找不到备份记录，尝试直接复制原始文件
                        if source_path.exists():
                            shutil.copy2(str(source_path), str(target_path))
                            success = True
                            self.logger.debug(f"直接复制文件: {source_path} → {target_path}")
                        else:
                            success = False
                            error_msg = f"原始文件和备份都不存在: {source_path}"
                            self.logger.error(error_msg)
                else:
                    # 非整理操作或其他情况
                    backup_enabled = self.config.get('backup_enabled', True)
                    success = safe_move_file(source_path, target_path, backup_enabled)
                    error_msg = None
                    
                if success:
                    self.logger.file_processed(action, str(source_path), str(target_path), 
                                             Path(backup_path or source_path).stat().st_size)
            
            self._record_operation(
                source_path=str(source_path),
                target_path=str(target_path),
                action=action,
                file_size=Path(backup_path or source_path).stat().st_size,
                success=success,
                session_id=self.session_id,
                backup_path=backup_path,
                file_hash=file_hash,
                error_message=error_msg
            )
            
            if success and action == "move":
                self.statistics.moved_files += 1
                
        except Exception as e:
            self.logger.error(f"文件移动失败 {source_path}: {str(e)}")
            self._record_operation(
                source_path=str(source_path),
                target_path=str(target_path),
                action=action,
                file_size=0,
                success=False,
                session_id=self.session_id,
                error_message=str(e)
            )
            self.statistics.error_files += 1
            raise
    
    def _record_operation(self, source_path: str, target_path: str, action: str,
                         file_size: int, success: bool, error_message: Optional[str] = None):
        """记录操作"""
        operation = OrganizeOperation(
            source_path=source_path,
            target_path=target_path,
            action=action,
            file_size=file_size,
            timestamp=datetime.now(),
            success=success,
            error_message=error_message
        )
        self.operations.append(operation)
    
    def _generate_smart_plan(self, analyzed_files: List[Dict], file_paths: List[Path]) -> Dict[str, any]:
        """生成智能整理方案"""
        plan = {
            'target_directory': str(self.target_directory),
            'total_files': len(file_paths),
            'move_operations': [],
            'skip_operations': [],
            'duplicate_handling': [],
            'backup_required': 0,
            'estimated_time': '0',
            'risk_level': 'low',
            'classification_strategy': {}
        }
        
        # 检测重复文件
        duplicates = self._detect_duplicates(file_paths)
        duplicate_map = {}
        for group in duplicates:
            keeper, candidates = self.duplicate_detector.resolve_duplicates(group)
            for candidate in candidates:
                duplicate_map[str(candidate)] = str(keeper)
                plan['duplicate_handling'].append({
                    'duplicate': str(candidate),
                    'keeper': str(keeper),
                    'strategy': self.config.get('duplicate_strategy', 'keep_newest')
                })
        
        # 生成移动操作
        for file_analysis in analyzed_files:
            file_info = file_analysis['file_info']
            file_path = Path(file_info['path'])
            
            # 检查是否为重复文件
            if str(file_path) in duplicate_map:
                continue
            
            # 确定目标路径
            target_path = self._determine_target_path(file_analysis)
            
            # 检查是否需要移动
            if file_path == target_path:
                plan['skip_operations'].append({
                    'source': str(file_path),
                    'reason': 'already_in_correct_location'
                })
            else:
                plan['move_operations'].append({
                    'source': str(file_path),
                    'target': str(target_path),
                    'size': file_info['size'],
                    'category': file_analysis['suggested_category'],
                    'confidence': file_analysis['confidence_score']
                })
                plan['backup_required'] += 1
        
        plan['estimated_time'] = f"{len(plan['move_operations']) * 0.1:.1f} seconds"
        plan['risk_level'] = 'high' if len(plan['move_operations']) > 100 else 'medium' if len(plan['move_operations']) > 50 else 'low'
        
        return plan
    
    def _save_plan(self, plan: Dict[str, any]) -> str:
        """保存整理方案到文件"""
        from datetime import datetime
        import json
        
        plans_dir = Path('./plans')
        plans_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_file = plans_dir / f"smart_plan_{timestamp}.json"
        
        plan['generated_at'] = datetime.now().isoformat()
        plan['session_id'] = self.session_id
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"方案已保存至: {plan_file}")
        return str(plan_file)
    
    def _load_plan(self, plan_file: str) -> Dict[str, any]:
        """加载整理方案"""
        import json
        
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        
        return plan
    
    def _execute_smart_plan(self, plan: Dict[str, any], dry_run: bool):
        """执行智能整理方案（适应移动-复制备份策略）"""
        self.logger.info(f"🛡️ 开始执行整理方案，共 {len(plan['move_operations'])} 个移动操作")
        
        # 阶段1：为所有需要移动的文件创建备份（移动原始文件到备份位置）
        if not dry_run:
            self.logger.info(f"🔒 阶段1：移动原始文件到备份位置，共 {len(plan['move_operations'])} 个文件")
            backup_count = 0
            for operation in plan['move_operations']:
                source_path = Path(operation['source'])
                if source_path.exists():
                    backup_record = self.backup_manager.create_backup(
                        source_path, 
                        {
                            'operation': operation, 
                            'category': operation['category'],
                            'session_id': self.session_id,
                            'target_path': operation['target']
                        }
                    )
                    if backup_record:
                        backup_count += 1
                        if backup_count <= 10:  # 只显示前10个备份信息
                            self.logger.debug(f"移动到备份: {source_path.name} → {Path(backup_record.backup_path).name}")
            self.logger.info(f"✅ 阶段1完成：已移动 {backup_count} 个文件到备份位置")
        
        self.logger.info(f"🔒 阶段1完成：已为 {plan['backup_required']} 个文件创建移动备份")
        
        # 阶段2：从备份位置复制文件到新的目标位置
        self.logger.info(f"🔄 阶段2：从备份复制文件到目标位置")
        copied_count = 0
        for operation in plan['move_operations']:
            source_path = Path(operation['source'])
            target_path = Path(operation['target'])
            
            if dry_run:
                self.logger.info(f"[试运行] 🔄 复制: {source_path} → {target_path}")
                self.statistics.moved_files += 1
            else:
                self._move_file(source_path, target_path, dry_run=False, action="move")
                copied_count += 1
        
        self.logger.info(f"✅ 阶段2完成：已复制 {copied_count} 个文件到目标位置")
        
        # 处理重复文件
        for dup_info in plan['duplicate_handling']:
            if not dry_run:
                duplicate_path = Path(dup_info['duplicate'])
                keeper_path = Path(dup_info['keeper'])
                self._handle_duplicate_file(duplicate_path, str(keeper_path), dry_run=False)
    
    def _create_analysis_result(self, analyzed_files: List[Dict]) -> Dict[str, any]:
        """创建分析结果"""
        # 统计文件类型分布
        type_stats = {}
        for file_analysis in analyzed_files:
            category = file_analysis['suggested_category']
            type_stats[category] = type_stats.get(category, 0) + 1
        
        return {
            'success': True,
            'message': '文件分析完成',
            'analysis_results': {
                'total_files': len(analyzed_files),
                'type_distribution': type_stats,
                'detailed_analysis': analyzed_files
            }
        }
    
    def _create_plan_result(self, plan: Dict[str, any], plan_file: str) -> Dict[str, any]:
        """创建方案结果"""
        return {
            'success': True,
            'message': '整理方案生成完成',
            'plan': plan,
            'plan_file': plan_file
        }
    
    def _create_smart_result(self, success: bool, message: str, plan: Dict[str, any],
                           dry_run: bool = False) -> Dict[str, any]:
        """创建智能整理结果字典"""
        return {
            'success': success,
            'message': message,
            'dry_run': dry_run,
            'session_id': self.session_id,
            'statistics': asdict(self.statistics),
            'operations': [asdict(op) for op in self.operations],
            'plan': plan,
            'target_directory': str(self.target_directory)
        }
    
    def _create_result_dict(self, success: bool, message: str, 
                           dry_run: bool = False) -> Dict[str, any]:
        """创建结果字典（兼容旧版本）"""
        return {
            'success': success,
            'message': message,
            'dry_run': dry_run,
            'statistics': asdict(self.statistics),
            'operations': [asdict(op) for op in self.operations],
            'target_directory': str(self.target_directory)
        }
    
    def get_operations_summary(self) -> Dict[str, int]:
        """获取操作摘要统计"""
        summary = {
            'move': 0,
            'copy': 0,
            'skip': 0,
            'duplicate': 0,
            'error': 0
        }
        
        for operation in self.operations:
            if operation.success:
                summary[operation.action] += 1
            else:
                summary['error'] += 1
        
        return summary
    
    def rollback_last_operation(self) -> bool:
        """回滚最后一次操作（兼容旧版本）"""
        if not self.operations:
            return False
        
        last_op = self.operations[-1]
        if not last_op.success or not last_op.target_path:
            return False
        
        try:
            # 将文件移回原位置
            source = Path(last_op.target_path)
            target = Path(last_op.source_path)
            
            if source.exists() and not target.exists():
                source.rename(target)
                self.logger.info(f"回滚操作: {source} → {target}")
                self.operations.pop()  # 移除操作记录
                return True
                
        except Exception as e:
            self.logger.error(f"回滚失败: {str(e)}")
        
        return False
    
    def undo_session(self, session_id: str) -> Tuple[bool, List[str]]:
        """撤销整个会话的操作"""
        return self.backup_manager.restore_session(session_id)
    
    def undo_file(self, session_id: str, source_path: str) -> bool:
        """撤销单个文件的操作"""
        return self.backup_manager.restore_file(session_id, source_path)
    
    def list_sessions(self, status_filter: Optional[str] = None) -> List[Dict[str, any]]:
        """列出所有会话"""
        sessions = self.backup_manager.list_sessions(status_filter)
        return [
            {
                'session_id': s.session_id,
                'target_directory': s.target_directory,
                'start_time': s.start_time.isoformat(),
                'end_time': s.end_time.isoformat() if s.end_time else None,
                'status': s.status,
                'backup_count': len(s.backup_records),
                'operation_summary': s.operation_summary
            }
            for s in sessions
        ]
    
    def _find_backup_record(self, source_path: str) -> Optional[BackupRecord]:
        """查找指定源文件的备份记录"""
        if not self.session_id:
            return None
            
        session = self.backup_manager.get_session(self.session_id)
        if not session:
            return None
            
        for record in session.backup_records:
            if record.source_path == source_path:
                return record
        return None
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, any]]:
        """获取会话详细信息"""
        session = self.backup_manager.get_session(session_id)
        if not session:
            return None
        
        return {
            'session_id': session.session_id,
            'target_directory': session.target_directory,
            'start_time': session.start_time.isoformat(),
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'status': session.status,
            'backup_records': [
                {
                    'source_path': r.source_path,
                    'backup_path': r.backup_path,
                    'file_size': r.file_size,
                    'backup_time': r.backup_time.isoformat(),
                    'metadata': r.metadata
                }
                for r in session.backup_records
            ],
            'operation_summary': session.operation_summary
        }


# 便捷函数
def organize_directory(directory: str, config_file: Optional[str] = None, 
                      dry_run: bool = False) -> Dict[str, any]:
    """
    整理目录的便捷函数
    
    Args:
        directory: 目标目录
        config_file: 配置文件路径
        dry_run: 是否试运行
        
    Returns:
        整理结果
    """
    organizer = FileOrganizer(directory, config_file)
    return organizer.organize(dry_run=dry_run)


def scan_for_duplicates(directory: str, config_file: Optional[str] = None) -> Dict[str, any]:
    """
    扫描目录中的重复文件
    
    Args:
        directory: 目标目录
        config_file: 配置文件路径
        
    Returns:
        重复文件扫描结果
    """
    organizer = FileOrganizer(directory, config_file)
    
    try:
        # 只执行扫描和检测步骤
        file_paths = organizer._scan_files()
        duplicates = organizer._detect_duplicates(file_paths)
        
        stats = organizer.duplicate_detector.get_duplicate_statistics()
        
        return {
            'success': True,
            'duplicate_groups': len(duplicates),
            'total_duplicate_files': stats['total_duplicate_files'],
            'statistics': stats,
            'duplicate_details': [[str(f) for f in group] for group in duplicates]
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"扫描失败: {str(e)}"
        }