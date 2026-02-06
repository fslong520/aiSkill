#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器
生成详细的文件整理报告和统计信息
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json

from config import get_config
from logger import get_logger
from utils import format_file_size, human_readable_time, format_datetime


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.config = get_config()
        self.logger = get_logger()
        self.report_formats = ['markdown', 'json', 'html']
    
    def generate_organize_report(self, result: Dict, output_format: str = 'markdown') -> str:
        """
        生成整理报告
        
        Args:
            result: 整理结果数据
            output_format: 输出格式 ('markdown', 'json', 'html')
            
        Returns:
            生成的报告内容
        """
        if output_format == 'markdown':
            return self._generate_markdown_report(result)
        elif output_format == 'json':
            return self._generate_json_report(result)
        elif output_format == 'html':
            return self._generate_html_report(result)
        else:
            raise ValueError(f"不支持的报告格式: {output_format}")
    
    def _generate_markdown_report(self, result: Dict) -> str:
        """生成Markdown格式报告"""
        timestamp = datetime.now()
        
        lines = [
            f"# 文件整理报告",
            f"",
            f"## 基本信息",
            f"- **报告生成时间**: {format_datetime(timestamp, 'standard')}",
            f"- **目标目录**: `{result.get('target_directory', 'Unknown')}`",
            f"- **执行模式**: {'试运行' if result.get('dry_run', False) else '实际执行'}",
            f"- **执行状态**: {'✅ 成功' if result.get('success', False) else '❌ 失败'}",
            f"",
        ]
        
        # 添加执行消息
        if result.get('message'):
            lines.append(f"## 执行摘要")
            lines.append(f"> {result['message']}")
            lines.append(f"")
        
        # 添加统计信息
        stats = result.get('statistics', {})
        if stats:
            lines.extend(self._generate_statistics_section(stats))
        
        # 添加操作详情
        operations = result.get('operations', [])
        if operations:
            lines.extend(self._generate_operations_section(operations))
        
        # 添加错误信息（如果有）
        error_ops = [op for op in operations if not op.get('success', True)]
        if error_ops:
            lines.extend(self._generate_errors_section(error_ops))
        
        return "\n".join(lines)
    
    def _generate_statistics_section(self, stats: Dict) -> List[str]:
        """生成统计信息部分"""
        lines = [
            "## 统计信息",
            "",
            "| 指标 | 数值 |",
            "|------|------|",
            f"| 总文件数 | {stats.get('total_files', 0)} |",
            f"| 已处理文件 | {stats.get('processed_files', 0)} |",
            f"| 成功移动 | {stats.get('moved_files', 0)} |",
            f"| 跳过文件 | {stats.get('skipped_files', 0)} |",
            f"| 重复文件 | {stats.get('duplicate_files', 0)} |",
            f"| 错误文件 | {stats.get('error_files', 0)} |",
            f"| 总大小 | {format_file_size(stats.get('total_size', 0))} |",
        ]
        
        # 添加时间和效率信息
        if stats.get('start_time') and stats.get('end_time'):
            duration = stats.get('duration', 0)
            lines.extend([
                f"| 处理耗时 | {human_readable_time(duration)} |",
                f"| 处理速度 | {stats.get('processed_files', 0)/duration:.1f} 文件/秒 (平均) |" if duration > 0 else "",
                f"| 成功率 | {stats.get('success_rate', 0)*100:.1f}% |",
            ])
        
        lines.append("")
        return lines
    
    def _generate_operations_section(self, operations: List[Dict]) -> List[str]:
        """生成操作详情部分"""
        successful_ops = [op for op in operations if op.get('success', True)]
        
        if not successful_ops:
            return []
        
        lines = [
            "## 操作详情",
            "",
            "<details>",
            "<summary>点击查看详细操作记录 ({count} 项)</summary>".format(count=len(successful_ops)),
            "",
            "| 操作类型 | 源文件 | 目标文件 | 文件大小 | 时间 |",
            "|----------|--------|----------|----------|------|",
        ]
        
        # 按时间排序
        sorted_ops = sorted(successful_ops, key=lambda x: x.get('timestamp', ''))
        
        for op in sorted_ops:
            action_icon = {
                'move': '🔄',
                'copy': '📋',
                'skip': '⏭️',
                'duplicate': '🔁'
            }.get(op.get('action', ''), '❓')
            
            lines.append(
                f"| {action_icon} {op.get('action', '').capitalize()} "
                f"| `{op.get('source_path', '')}` "
                f"| `{op.get('target_path', '')}` "
                f"| {format_file_size(op.get('file_size', 0))} "
                f"| {str(op.get('timestamp', ''))[:19] if op.get('timestamp') else ''} |"
            )
        
        lines.extend([
            "",
            "</details>",
            ""
        ])
        
        return lines
    
    def _generate_errors_section(self, error_operations: List[Dict]) -> List[str]:
        """生成错误信息部分"""
        if not error_operations:
            return []
        
        lines = [
            "## 错误详情",
            "",
            "> ⚠️ 以下操作执行失败，请检查相关文件权限或磁盘空间。",
            "",
            "| 源文件 | 错误信息 | 时间 |",
            "|--------|----------|------|",
        ]
        
        for op in error_operations:
            lines.append(
                f"| `{op.get('source_path', '')}` "
                f"| {op.get('error_message', 'Unknown error')} "
                f"| {str(op.get('timestamp', ''))[:19] if op.get('timestamp') else ''} |"
            )
        
        lines.append("")
        return lines
    
    def _generate_json_report(self, result: Dict) -> str:
        """生成JSON格式报告"""
        # 添加报告元数据
        report_data = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'format': 'json',
                'generator': 'FileOrganizer'
            },
            'execution_result': result
        }
        
        return json.dumps(report_data, indent=2, ensure_ascii=False)
    
    def _generate_html_report(self, result: Dict) -> str:
        """生成HTML格式报告"""
        markdown_content = self._generate_markdown_report(result)
        
        # 简单的HTML模板
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文件整理报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }}
        h1, h2, h3 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f5f5f5; }}
        .success {{ color: #28a745; }}
        .error {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        details {{ margin: 20px 0; }}
        summary {{ cursor: pointer; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📁 文件整理报告</h1>
    <div>{self._markdown_to_html(markdown_content)}</div>
</body>
</html>
        """
        
        return html_template
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """简单的Markdown到HTML转换"""
        import re
        
        # 转换标题
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # 转换表格
        lines = html.split('\n')
        in_table = False
        table_lines = []
        converted_lines = []
        
        for line in lines:
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    table_lines = ['<table>']
                    # 检查是否为表头
                    if '---' in line:
                        continue
                    table_lines.append('<thead><tr>')
                    headers = [cell.strip() for cell in line.split('|')[1:-1]]
                    for header in headers:
                        table_lines.append(f'<th>{header}</th>')
                    table_lines.append('</tr></thead><tbody>')
                else:
                    # 数据行
                    table_lines.append('<tr>')
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    for cell in cells:
                        table_lines.append(f'<td>{cell}</td>')
                    table_lines.append('</tr>')
            else:
                if in_table:
                    table_lines.append('</tbody></table>')
                    converted_lines.extend(table_lines)
                    in_table = False
                    table_lines = []
                converted_lines.append(line)
        
        if in_table:
            table_lines.append('</tbody></table>')
            converted_lines.extend(table_lines)
        
        html = '\n'.join(converted_lines)
        
        # 转换其他元素
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        html = re.sub(r'> (.+)', r'<blockquote>\1</blockquote>', html)
        html = html.replace('\n', '<br>')
        
        return html
    
    def save_report(self, content: str, report_type: str = 'organize', 
                   format_type: str = 'markdown') -> str:
        """
        保存报告到文件
        
        Args:
            content: 报告内容
            report_type: 报告类型
            format_type: 格式类型
            
        Returns:
            保存的文件路径
        """
        # 确定保存目录
        save_dir = Path(self.config.get('report.save_directory', './reports'))
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_type}_report_{timestamp}.{format_type}"
        if format_type == 'markdown':
            filename = f"{report_type}_report_{timestamp}.md"
        elif format_type == 'html':
            filename = f"{report_type}_report_{timestamp}.html"
        
        file_path = save_dir / filename
        
        # 保存文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"报告已保存到: {file_path}")
            return str(file_path)
        except Exception as e:
            self.logger.error(f"保存报告失败: {str(e)}")
            raise
    
    def generate_summary_report(self, results_history: List[Dict]) -> str:
        """
        生成汇总报告（多个整理任务的统计）
        
        Args:
            results_history: 历史结果列表
            
        Returns:
            汇总报告内容
        """
        if not results_history:
            return "# 汇总报告\n\n暂无历史数据"
        
        lines = [
            "# 文件整理汇总报告",
            "",
            f"## 概览",
            f"- **统计周期**: {len(results_history)} 次整理任务",
            f"- **报告生成时间**: {format_datetime(datetime.now(), 'standard')}",
            ""
        ]
        
        # 统计总体数据
        total_stats = {
            'total_files': 0,
            'moved_files': 0,
            'duplicate_files': 0,
            'error_files': 0,
            'total_duration': 0.0
        }
        
        for result in results_history:
            stats = result.get('statistics', {})
            total_stats['total_files'] += stats.get('total_files', 0)
            total_stats['moved_files'] += stats.get('moved_files', 0)
            total_stats['duplicate_files'] += stats.get('duplicate_files', 0)
            total_stats['error_files'] += stats.get('error_files', 0)
            total_stats['total_duration'] += stats.get('duration', 0)
        
        lines.extend([
            "## 总体统计",
            "",
            "| 指标 | 数值 |",
            "|------|------|",
            f"| 总处理文件数 | {total_stats['total_files']} |",
            f"| 总移动文件数 | {total_stats['moved_files']} |",
            f"| 总重复文件数 | {total_stats['duplicate_files']} |",
            f"| 总错误文件数 | {total_stats['error_files']} |",
            f"| 平均处理时间 | {human_readable_time(total_stats['total_duration'] / len(results_history))} |",
            ""
        ])
        
        # 详细历史记录
        lines.extend([
            "## 历史记录",
            "",
            "| 任务时间 | 目标目录 | 处理文件 | 移动文件 | 耗时 | 状态 |",
            "|----------|----------|----------|----------|------|------|"
        ])
        
        for result in results_history[-10:]:  # 只显示最近10次
            stats = result.get('statistics', {})
            timestamp = result.get('timestamp', datetime.now())
            if hasattr(timestamp, 'isoformat'):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)
            directory = result.get('target_directory', 'Unknown')[:30] + '...' if len(result.get('target_directory', '')) > 30 else result.get('target_directory', 'Unknown')
            status = '✅' if result.get('success', False) else '❌'
            
            lines.append(
                f"| {timestamp[:19] if isinstance(timestamp, str) else 'Unknown'} "
                f"| `{directory}` "
                f"| {stats.get('processed_files', 0)} "
                f"| {stats.get('moved_files', 0)} "
                f"| {human_readable_time(stats.get('duration', 0))} "
                f"| {status} |"
            )
        
        lines.append("")
        return "\n".join(lines)


# 便捷函数
def generate_and_save_report(result: Dict, report_type: str = 'organize',
                           format_type: str = 'markdown') -> str:
    """
    生成并保存报告的便捷函数
    
    Args:
        result: 整理结果
        report_type: 报告类型
        format_type: 格式类型
        
    Returns:
        保存的文件路径
    """
    generator = ReportGenerator()
    content = generator.generate_organize_report(result, format_type)
    return generator.save_report(content, report_type, format_type)