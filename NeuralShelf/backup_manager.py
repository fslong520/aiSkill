#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份管理器
负责文件备份、恢复和撤销操作的管理
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

from logger import get_logger
from utils import format_datetime


@dataclass
class BackupRecord:
    """备份记录"""
    session_id: str
    source_path: str
    backup_path: str
    file_size: int
    backup_time: datetime
    file_hash: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class SessionInfo:
    """会话信息"""
    session_id: str
    target_directory: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "running"  # running, completed, failed, cancelled
    backup_records: List[BackupRecord] = None
    operation_summary: Optional[Dict] = None
    
    def __post_init__(self):
        if self.backup_records is None:
            self.backup_records = []


class BackupManager:
    """备份管理器主类"""
    
    def __init__(self, base_backup_dir: Optional[str] = None):
        """
        初始化备份管理器
        
        Args:
            base_backup_dir: 备份根目录，默认为 ~/.file-organizer/backups
        """
        self.logger = get_logger()
        
        if base_backup_dir is None:
            self.base_backup_dir = Path.home() / '.file-organizer' / 'backups'
        else:
            self.base_backup_dir = Path(base_backup_dir)
        
        self.base_backup_dir.mkdir(parents=True, exist_ok=True)
        self.current_session: Optional[SessionInfo] = None
        self.sessions_file = self.base_backup_dir / 'sessions.json'
        self.sessions: Dict[str, SessionInfo] = self._load_sessions()
    
    def _load_sessions(self) -> Dict[str, SessionInfo]:
        """加载会话信息"""
        if not self.sessions_file.exists():
            return {}
        
        try:
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            sessions = {}
            for session_id, session_data in data.items():
                # 转换时间字符串为datetime对象
                session_data['start_time'] = datetime.fromisoformat(session_data['start_time'])
                if session_data.get('end_time'):
                    session_data['end_time'] = datetime.fromisoformat(session_data['end_time'])
                
                # 转换备份记录
                backup_records = []
                for record_data in session_data.get('backup_records', []):
                    record_data['backup_time'] = datetime.fromisoformat(record_data['backup_time'])
                    backup_records.append(BackupRecord(**record_data))
                
                session_data['backup_records'] = backup_records
                sessions[session_id] = SessionInfo(**session_data)
            
            return sessions
        except Exception as e:
            self.logger.error(f"加载会话信息失败: {str(e)}")
            return {}
    
    def _save_sessions(self):
        """保存会话信息"""
        try:
            # 转换为可序列化的格式
            serializable_data = {}
            for session_id, session in self.sessions.items():
                session_dict = asdict(session)
                # 转换datetime为字符串
                session_dict['start_time'] = session.start_time.isoformat()
                if session.end_time:
                    session_dict['end_time'] = session.end_time.isoformat()
                
                # 转换备份记录
                backup_records = []
                for record in session.backup_records:
                    record_dict = asdict(record)
                    record_dict['backup_time'] = record.backup_time.isoformat()
                    backup_records.append(record_dict)
                
                session_dict['backup_records'] = backup_records
                serializable_data[session_id] = session_dict
            
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"保存会话信息失败: {str(e)}")
    
    def start_session(self, target_directory: str) -> str:
        """
        开始新的备份会话
        
        Args:
            target_directory: 目标目录
            
        Returns:
            会话ID
        """
        session_id = f"SESSION_{format_datetime(datetime.now(), 'filename')}"
        
        self.current_session = SessionInfo(
            session_id=session_id,
            target_directory=target_directory,
            start_time=datetime.now()
        )
        
        # 创建会话备份目录
        session_backup_dir = self.base_backup_dir / session_id
        session_backup_dir.mkdir(exist_ok=True)
        
        self.sessions[session_id] = self.current_session
        self._save_sessions()
        
        self.logger.info(f"开始备份会话: {session_id}")
        return session_id
    
    def create_backup(self, source_path: Path, metadata: Optional[Dict] = None) -> Optional[BackupRecord]:
        """
        为文件创建备份
        
        Args:
            source_path: 源文件路径
            metadata: 额外的元数据
            
        Returns:
            备份记录，如果失败返回None
        """
        if not self.current_session:
            self.logger.error("没有活跃的会话")
            return None
        
        try:
            if not source_path.exists():
                self.logger.warning(f"源文件不存在: {source_path}")
                return None
            
            # 生成备份文件名
            timestamp = format_datetime(datetime.now(), 'filename')
            backup_filename = f"{timestamp}_{source_path.name}"
            backup_path = self.base_backup_dir / self.current_session.session_id / backup_filename
            
            # 移动文件（真正的移动而非复制以节省空间）
            shutil.move(str(source_path), str(backup_path))
            
            # 创建备份记录
            stat = source_path.stat()
            backup_record = BackupRecord(
                session_id=self.current_session.session_id,
                source_path=str(source_path),
                backup_path=str(backup_path),
                file_size=stat.st_size,
                backup_time=datetime.now(),
                metadata=metadata
            )
            
            self.current_session.backup_records.append(backup_record)
            self._save_sessions()
            
            self.logger.debug(f"创建备份: {source_path} → {backup_path}")
            return backup_record
            
        except Exception as e:
            self.logger.error(f"创建备份失败 {source_path}: {str(e)}")
            return None
    
    def complete_session(self, operation_summary: Optional[Dict] = None):
        """
        完成当前会话
        
        Args:
            operation_summary: 操作摘要信息
        """
        if not self.current_session:
            return
        
        self.current_session.end_time = datetime.now()
        self.current_session.status = "completed"
        self.current_session.operation_summary = operation_summary
        
        self._save_sessions()
        self.logger.info(f"会话完成: {self.current_session.session_id}")
        self.current_session = None
    
    def cancel_session(self):
        """取消当前会话"""
        if not self.current_session:
            return
        
        self.current_session.end_time = datetime.now()
        self.current_session.status = "cancelled"
        
        # 清理会话备份目录
        session_backup_dir = self.base_backup_dir / self.current_session.session_id
        if session_backup_dir.exists():
            shutil.rmtree(session_backup_dir)
            self.logger.info(f"清理取消的会话备份: {session_backup_dir}")
        
        self._save_sessions()
        self.current_session = None
    
    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """
        获取会话信息
        
        Args:
            session_id: 会话ID
            
        Returns:
            会话信息，如果不存在返回None
        """
        return self.sessions.get(session_id)
    
    def list_sessions(self, status_filter: Optional[str] = None) -> List[SessionInfo]:
        """
        列出会话
        
        Args:
            status_filter: 状态过滤器 (running, completed, failed, cancelled)
            
        Returns:
            会话列表
        """
        sessions = list(self.sessions.values())
        
        if status_filter:
            sessions = [s for s in sessions if s.status == status_filter]
        
        # 按开始时间排序
        sessions.sort(key=lambda x: x.start_time, reverse=True)
        return sessions
    
    def restore_session(self, session_id: str) -> Tuple[bool, List[str]]:
        """
        恢复指定会话的所有文件
        
        Args:
            session_id: 会话ID
            
        Returns:
            (是否成功, 错误信息列表)
        """
        session = self.get_session(session_id)
        if not session:
            return False, [f"会话不存在: {session_id}"]
        
        if session.status != "completed":
            return False, [f"会话状态不正确: {session.status}"]
        
        errors = []
        success_count = 0
        
        self.logger.info(f"开始恢复会话: {session_id}")
        
        for backup_record in session.backup_records:
            try:
                source_path = Path(backup_record.source_path)
                backup_path = Path(backup_record.backup_path)
                
                # 确保目标目录存在
                source_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 恢复文件（移动回去）
                if backup_path.exists():
                    # 确保目标文件不存在，避免冲突
                    if source_path.exists():
                        source_path.unlink()
                    shutil.move(str(backup_path), str(source_path))
                    self.logger.info(f"恢复文件: {backup_path.name} → {source_path}")
                    success_count += 1
                else:
                    errors.append(f"备份文件不存在: {backup_path}")
                    
            except Exception as e:
                error_msg = f"恢复文件失败 {backup_record.source_path}: {str(e)}"
                errors.append(error_msg)
                self.logger.error(error_msg)
        
        self.logger.info(f"会话恢复完成: {success_count} 成功, {len(errors)} 失败")
        return len(errors) == 0, errors
    
    def restore_file(self, session_id: str, source_path: str) -> bool:
        """
        恢复单个文件
        
        Args:
            session_id: 会话ID
            source_path: 原始文件路径
            
        Returns:
            是否成功
        """
        session = self.get_session(session_id)
        if not session:
            self.logger.error(f"会话不存在: {session_id}")
            return False
        
        # 查找对应的备份记录
        backup_record = None
        for record in session.backup_records:
            if record.source_path == source_path:
                backup_record = record
                break
        
        if not backup_record:
            self.logger.error(f"未找到文件的备份记录: {source_path}")
            return False
        
        try:
            backup_path = Path(backup_record.backup_path)
            target_path = Path(source_path)
            
            if not backup_path.exists():
                self.logger.error(f"备份文件不存在: {backup_path}")
                return False
            
            # 确保目标目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 恢复文件（移动回去）
            # 确保目标文件不存在，避免冲突
            if target_path.exists():
                target_path.unlink()
            shutil.move(str(backup_path), str(target_path))
            self.logger.info(f"文件恢复成功: {source_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"文件恢复失败 {source_path}: {str(e)}")
            return False
    
    def cleanup_old_backups(self, days_to_keep: int = 7) -> int:
        """
        清理旧备份
        
        Args:
            days_to_keep: 保留天数
            
        Returns:
            清理的会话数量
        """
        cutoff_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_time = cutoff_time.replace(day=cutoff_time.day - days_to_keep)
        
        cleaned_count = 0
        
        for session_id, session in list(self.sessions.items()):
            if session.end_time and session.end_time < cutoff_time:
                # 删除备份文件
                session_backup_dir = self.base_backup_dir / session_id
                if session_backup_dir.exists():
                    shutil.rmtree(session_backup_dir)
                    self.logger.info(f"清理旧备份: {session_id}")
                
                # 从会话记录中移除
                del self.sessions[session_id]
                cleaned_count += 1
        
        self._save_sessions()
        return cleaned_count
    
    def get_backup_stats(self) -> Dict[str, any]:
        """
        获取备份统计信息
        
        Returns:
            统计信息字典
        """
        total_sessions = len(self.sessions)
        completed_sessions = len([s for s in self.sessions.values() if s.status == "completed"])
        total_backups = sum(len(s.backup_records) for s in self.sessions.values())
        
        # 计算总备份大小
        total_size = 0
        for session in self.sessions.values():
            for record in session.backup_records:
                total_size += record.file_size
        
        return {
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'active_sessions': len([s for s in self.sessions.values() if s.status == "running"]),
            'total_backups': total_backups,
            'total_backup_size': total_size,
            'backup_directory': str(self.base_backup_dir)
        }


# 便捷函数
def get_backup_manager() -> BackupManager:
    """获取备份管理器实例"""
    return BackupManager()


def create_session_backup(target_directory: str) -> str:
    """
    为目录创建备份会话
    
    Args:
        target_directory: 目标目录
        
    Returns:
        会话ID
    """
    manager = get_backup_manager()
    return manager.start_session(target_directory)


def restore_from_session(session_id: str) -> Tuple[bool, List[str]]:
    """
    从会话恢复文件
    
    Args:
        session_id: 会话ID
        
    Returns:
        (是否成功, 错误信息列表)
    """
    manager = get_backup_manager()
    return manager.restore_session(session_id)