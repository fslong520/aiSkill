#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件智能整理器主入口
协调各个模块完成文件整理任务
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from config import setup_logging, get_config
from logger import get_logger
from organizer import FileOrganizer
from duplicate_detector import DuplicateDetector
from reporter import ReportGenerator
from utils import validate_directory_permissions


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='智能文件整理器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s organize /path/to/directory
  %(prog)s organize /path/to/directory --dry-run
  %(prog)s scan-duplicates /path/to/directory
  %(prog)s generate-report /path/to/directory --format json
        """
    )
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 传统整理命令
    organize_parser = subparsers.add_parser('organize', help='传统文件整理')
    organize_parser.add_argument('directory', help='目标目录路径')
    organize_parser.add_argument('-c', '--config', help='配置文件路径')
    organize_parser.add_argument('-d', '--dry-run', action='store_true', 
                               help='试运行模式（不实际移动文件）')
    organize_parser.add_argument('-v', '--verbose', action='store_true',
                               help='详细输出模式')
    
    # 四阶段智能整理命令
    smart_parser = subparsers.add_parser('smart-organize', help='四阶段智能整理')
    smart_parser.add_argument('directory', help='目标目录路径')
    smart_parser.add_argument('-c', '--config', help='配置文件路径')
    smart_parser.add_argument('-d', '--dry-run', action='store_true', 
                            help='试运行模式（不实际移动文件）')
    smart_parser.add_argument('-v', '--verbose', action='store_true',
                            help='详细输出模式')
    
    # 分析阶段命令
    analyze_parser = subparsers.add_parser('analyze-only', help='仅执行文件分析')
    analyze_parser.add_argument('directory', help='目标目录路径')
    analyze_parser.add_argument('-c', '--config', help='配置文件路径')
    analyze_parser.add_argument('-v', '--verbose', action='store_true',
                              help='详细输出模式')
    
    # 增强目录分析命令
    enhanced_analyze_parser = subparsers.add_parser('enhanced-analyze', help='增强目录分析（含tree命令和多方案）')
    enhanced_analyze_parser.add_argument('directory', help='目标目录路径')
    enhanced_analyze_parser.add_argument('-c', '--config', help='配置文件路径')
    enhanced_analyze_parser.add_argument('-v', '--verbose', action='store_true',
                                       help='详细输出模式')
    
    # 决策阶段命令
    plan_parser = subparsers.add_parser('plan-only', help='仅生成整理方案')
    plan_parser.add_argument('directory', help='目标目录路径')
    plan_parser.add_argument('-c', '--config', help='配置文件路径')
    plan_parser.add_argument('-v', '--verbose', action='store_true',
                           help='详细输出模式')
    
    # 执行阶段命令
    execute_parser = subparsers.add_parser('execute-plan', help='执行整理方案')
    execute_parser.add_argument('directory', help='目标目录路径')
    execute_parser.add_argument('--plan', required=True, help='整理方案文件路径')
    execute_parser.add_argument('-c', '--config', help='配置文件路径')
    execute_parser.add_argument('-d', '--dry-run', action='store_true', 
                              help='试运行模式（不实际移动文件）')
    execute_parser.add_argument('-v', '--verbose', action='store_true',
                              help='详细输出模式')
    
    # 撤销命令
    undo_parser = subparsers.add_parser('undo-session', help='撤销整理会话')
    undo_parser.add_argument('session_id', help='会话ID')
    undo_parser.add_argument('-v', '--verbose', action='store_true',
                           help='详细输出模式')
    
    # 会话列表命令
    list_parser = subparsers.add_parser('list-sessions', help='列出整理会话')
    list_parser.add_argument('--status', choices=['running', 'completed', 'failed', 'cancelled'],
                           help='按状态过滤')
    list_parser.add_argument('-v', '--verbose', action='store_true',
                           help='详细输出模式')
    
    # 重复文件扫描命令
    scan_parser = subparsers.add_parser('scan-duplicates', help='扫描重复文件')
    scan_parser.add_argument('directory', help='目标目录路径')
    scan_parser.add_argument('-c', '--config', help='配置文件路径')
    scan_parser.add_argument('-v', '--verbose', action='store_true',
                           help='详细输出模式')
    
    # 报告生成命令
    report_parser = subparsers.add_parser('generate-report', help='生成整理报告')
    report_parser.add_argument('directory', help='目标目录路径')
    report_parser.add_argument('-c', '--config', help='配置文件路径')
    report_parser.add_argument('-f', '--format', choices=['markdown', 'json', 'html'],
                             default='markdown', help='报告格式')
    report_parser.add_argument('-v', '--verbose', action='store_true',
                             help='详细输出模式')
    
    return parser


def handle_organize(args):
    """处理文件整理命令（传统模式）"""
    logger = get_logger()
    
    # 验证目录权限
    has_permission, errors = validate_directory_permissions(args.directory)
    if not has_permission:
        logger.error(f"目录权限不足: {'; '.join(errors)}")
        return False
    
    try:
        # 创建整理器实例
        organizer = FileOrganizer(args.directory, args.config)
        
        # 执行传统整理
        result = organizer.organize(dry_run=args.dry_run)
        
        # 生成报告
        if get_config().get('report.enabled', True):
            generator = ReportGenerator()
            report_content = generator.generate_organize_report(result, 'markdown')
            report_path = generator.save_report(report_content, 'organize', 'markdown')
            logger.info(f"详细报告已保存到: {report_path}")
        
        # 输出结果
        print(f"\n📊 传统整理结果:")
        print(f"   目标目录: {result['target_directory']}")
        print(f"   处理文件: {result['statistics']['processed_files']}")
        print(f"   移动文件: {result['statistics']['moved_files']}")
        print(f"   跳过文件: {result['statistics']['skipped_files']}")
        print(f"   重复文件: {result['statistics']['duplicate_files']}")
        print(f"   错误文件: {result['statistics']['error_files']}")
        print(f"   处理耗时: {result['statistics']['duration']:.2f} 秒")
        print(f"   执行状态: {'✅ 成功' if result['success'] else '❌ 失败'}")
        
        if result['message']:
            print(f"   消息: {result['message']}")
        
        return result['success']
        
    except Exception as e:
        logger.error(f"整理过程出错: {str(e)}")
        print(f"❌ 整理失败: {str(e)}")
        return False

def handle_smart_organize(args):
    """处理四阶段智能整理命令"""
    logger = get_logger()
    
    # 验证目录权限
    has_permission, errors = validate_directory_permissions(args.directory)
    if not has_permission:
        logger.error(f"目录权限不足: {'; '.join(errors)}")
        return False
    
    try:
        # 创建整理器实例
        organizer = FileOrganizer(args.directory, args.config)
        
        # 执行四阶段智能整理
        result = organizer.smart_organize(dry_run=args.dry_run)
        
        # 生成智能报告
        if get_config().get('report.enabled', True):
            generator = ReportGenerator()
            report_content = generator.generate_organize_report(result, 'markdown')
            report_path = generator.save_report(report_content, 'smart_organize', 'markdown')
            logger.info(f"智能整理报告已保存到: {report_path}")
        
        # 输出结果
        print(f"\n🎯 四阶段智能整理结果:")
        print(f"   会话ID: {result.get('session_id', 'N/A')}")
        print(f"   目标目录: {result['target_directory']}")
        print(f"   处理文件: {result['statistics']['processed_files']}")
        print(f"   移动文件: {result['statistics']['moved_files']}")
        print(f"   跳过文件: {result['statistics']['skipped_files']}")
        print(f"   重复文件: {result['statistics']['duplicate_files']}")
        print(f"   错误文件: {result['statistics']['error_files']}")
        print(f"   处理耗时: {result['statistics']['duration']:.2f} 秒")
        print(f"   执行状态: {'✅ 成功' if result['success'] else '❌ 失败'}")
        
        if result['message']:
            print(f"   消息: {result['message']}")
        
        return result['success']
        
    except Exception as e:
        logger.error(f"智能整理过程出错: {str(e)}")
        print(f"❌ 智能整理失败: {str(e)}")
        return False

def handle_analyze_only(args):
    """处理仅分析命令"""
    logger = get_logger()
    
    try:
        organizer = FileOrganizer(args.directory, args.config)
        result = organizer.smart_organize(analyze_only=True)
        
        if result['success']:
            analysis = result['analysis_results']
            print(f"\n📋 文件分析完成:")
            print(f"   总文件数: {analysis['total_files']}")
            print(f"   \n类型分布:")
            for category, count in analysis['type_distribution'].items():
                print(f"   - {category}: {count} 个文件")
            print(f"\n✅ 分析报告已生成")
        
        return result['success']
        
    except Exception as e:
        logger.error(f"分析过程出错: {str(e)}")
        print(f"❌ 分析失败: {str(e)}")
        return False

def handle_enhanced_analyze(args):
    """处理增强目录分析命令"""
    logger = get_logger()
    
    try:
        organizer = FileOrganizer(args.directory, args.config)
        result = organizer.enhanced_analyze_directory()
        
        if not result['success']:
            print(f"❌ 增强分析失败: {result['message']}")
            return False
            
        analysis = result['analysis_result']
        stats = analysis['statistics']
        schemes = result['scheme_previews']
        recommendation = result['recommended_scheme']
        
        print(f"\n🌳 增强目录分析完成:")
        print(f"   目标目录: {analysis['directory']}")
        print(f"   总文件数: {stats['total_files']}")
        print(f"   总目录数: {stats['total_directories']}")
        print(f"   总大小: {stats['total_size_bytes']:,} 字节")
        print(f"   最大深度: {stats['max_depth']} 层")
        
        print(f"\n📋 生成的整理方案 ({len(schemes)} 个):")
        for scheme_dict in schemes:
            risk_icon = {'low': '✅', 'medium': '⚠️', 'high': '❌'}[scheme_dict['risk_level']]
            print(f"   {risk_icon} {scheme_dict['name']} (置信度: {scheme_dict['confidence']:.2f})")
            print(f"      预估移动: {scheme_dict['estimated_moves']} 个文件")
            print(f"      预估时间: {scheme_dict['estimated_time']}")
            print(f"      风险级别: {scheme_dict['risk_level']}")
        
        print(f"\n🎯 推荐方案:")
        print(f"   {recommendation.name}")
        print(f"   置信度: {recommendation.confidence:.2f}")
        print(f"   描述: {recommendation.description}")
        
        print(f"\n📄 详细报告已保存到: {result['report_path']}")
        print(f"\n💡 使用 'plan-only' 命令基于推荐方案生成具体执行计划")
        
        return True
        
    except Exception as e:
        logger.error(f"增强分析过程出错: {str(e)}")
        print(f"❌ 增强分析失败: {str(e)}")
        return False

def handle_plan_only(args):
    """处理仅生成方案命令"""
    logger = get_logger()
    
    try:
        organizer = FileOrganizer(args.directory, args.config)
        result = organizer.smart_organize(plan_only=True)
        
        if result['success']:
            plan = result['plan']
            print(f"\n🧠 整理方案生成完成:")
            print(f"   总文件数: {plan['total_files']}")
            print(f"   移动操作: {len(plan['move_operations'])} 个")
            print(f"   跳过操作: {len(plan['skip_operations'])} 个")
            print(f"   重复处理: {len(plan['duplicate_handling'])} 个")
            print(f"   需要备份: {plan['backup_required']} 个文件")
            print(f"   风险等级: {plan['risk_level']}")
            print(f"   预估耗时: {plan['estimated_time']}")
            print(f"   方案文件: {result['plan_file']}")
            print(f"\n✅ 方案已保存，可使用 'execute-plan' 命令执行")
        
        return result['success']
        
    except Exception as e:
        logger.error(f"方案生成出错: {str(e)}")
        print(f"❌ 方案生成失败: {str(e)}")
        return False

def handle_execute_plan(args):
    """处理执行方案命令"""
    logger = get_logger()
    
    try:
        organizer = FileOrganizer(args.directory, args.config)
        result = organizer.smart_organize(execute_plan=args.plan, dry_run=args.dry_run)
        
        if result['success']:
            print(f"\n🔄 方案执行完成:")
            print(f"   会话ID: {result.get('session_id', 'N/A')}")
            print(f"   移动文件: {result['statistics']['moved_files']} 个")
            print(f"   跳过文件: {result['statistics']['skipped_files']} 个")
            print(f"   处理耗时: {result['statistics']['duration']:.2f} 秒")
            if args.dry_run:
                print(f"   \n⚠️  这是试运行模式，文件未实际移动")
            else:
                print(f"   \n✅ 文件已按方案整理完成")
        
        return result['success']
        
    except Exception as e:
        logger.error(f"方案执行出错: {str(e)}")
        print(f"❌ 方案执行失败: {str(e)}")
        return False

def handle_undo_session(args):
    """处理撤销会话命令"""
    logger = get_logger()
    
    try:
        organizer = FileOrganizer('.', None)  # 使用当前目录，实际会从会话ID恢复
        success, errors = organizer.undo_session(args.session_id)
        
        if success:
            print(f"\n↩️  会话撤销成功:")
            print(f"   会话ID: {args.session_id}")
            print(f"   ✅ 所有文件已恢复到原始位置")
        else:
            print(f"\n❌ 会话撤销失败:")
            print(f"   会话ID: {args.session_id}")
            for error in errors:
                print(f"   - {error}")
        
        return success
        
    except Exception as e:
        logger.error(f"撤销操作出错: {str(e)}")
        print(f"❌ 撤销失败: {str(e)}")
        return False

def handle_list_sessions(args):
    """处理列出会话命令"""
    logger = get_logger()
    
    try:
        organizer = FileOrganizer('.', None)
        sessions = organizer.list_sessions(args.status)
        
        if not sessions:
            print(f"\n📭 未找到符合条件的会话")
            if args.status:
                print(f"   状态过滤: {args.status}")
            return True
        
        print(f"\n📋 会话列表 (共 {len(sessions)} 个):")
        print(f"{'会话ID':<25} {'状态':<10} {'目录':<20} {'备份数':<8} {'时间'}")
        print("-" * 80)
        
        for session in sessions[:10]:  # 只显示最近10个
            status_icon = {
                'completed': '✅',
                'running': '🔄',
                'failed': '❌',
                'cancelled': '↩️'
            }.get(session['status'], '❓')
            
            target_dir = session['target_directory']
            if len(target_dir) > 17:
                target_dir = target_dir[:14] + '...'
            
            print(f"{session['session_id']:<25} {status_icon + ' ' + session['status']:<10} "
                  f"{target_dir:<20} {session['backup_count']:<8} "
                  f"{session['start_time'][:19]}")
        
        if len(sessions) > 10:
            print(f"\n... 还有 {len(sessions) - 10} 个会话")
        
        return True
        
    except Exception as e:
        logger.error(f"列出会话出错: {str(e)}")
        print(f"❌ 列出会话失败: {str(e)}")
        return False


def handle_scan_duplicates(args):
    """处理重复文件扫描命令"""
    logger = get_logger()
    
    try:
        # 创建重复检测器
        detector = DuplicateDetector()
        if args.config:
            config = get_config(args.config)
            detector.strategy = config.get('duplicate_strategy', 'keep_newest')
        
        # 获取目录中的所有文件
        directory = Path(args.directory)
        file_paths = [f for f in directory.rglob('*') if f.is_file()]
        
        logger.info(f"扫描目录: {directory}")
        logger.info(f"发现文件: {len(file_paths)} 个")
        
        # 检测重复文件
        duplicates = detector.detect_duplicates(file_paths, 'smart')
        
        if not duplicates:
            print("🔍 未发现重复文件")
            return True
        
        # 显示结果
        print(f"\n🔍 重复文件检测结果:")
        print(f"   发现重复组: {len(duplicates)} 组")
        
        total_duplicates = sum(len(group) for group in duplicates)
        print(f"   重复文件总数: {total_duplicates} 个")
        
        # 显示详细信息
        print(f"\n📝 重复文件详情:")
        for i, group in enumerate(duplicates, 1):
            print(f"\n   组 {i} ({len(group)} 个文件):")
            keeper, candidates = detector.resolve_duplicates(group)
            print(f"     保留: {keeper.name}")
            for candidate in candidates:
                print(f"     移除: {candidate.name}")
        
        # 生成详细报告
        report_content = detector.generate_duplicate_report()
        generator = ReportGenerator()
        report_path = generator.save_report(report_content, 'duplicates', 'markdown')
        print(f"\n📄 详细报告已保存到: {report_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"重复文件扫描出错: {str(e)}")
        print(f"❌ 扫描失败: {str(e)}")
        return False


def handle_generate_report(args):
    """处理报告生成命令"""
    logger = get_logger()
    
    try:
        # 这里可以实现从历史记录生成报告的功能
        # 目前简化实现：生成目录结构报告
        directory = Path(args.directory)
        
        print(f"📊 生成报告: {directory}")
        
        # 统计目录信息
        file_count = sum(1 for _ in directory.rglob('*') if _.is_file())
        dir_count = sum(1 for _ in directory.rglob('*') if _.is_dir())
        
        # 生成报告内容
        report_content = f"""# 目录分析报告

## 基本信息
- **目录路径**: `{directory}`
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **文件数量**: {file_count}
- **目录数量**: {dir_count}

## 目录结构
```
{directory}
├── [文件: {file_count}个]
└── [子目录: {dir_count}个]
```

## 文件类型分布
（需要进一步分析实现）
"""
        
        # 保存报告
        generator = ReportGenerator()
        report_path = generator.save_report(report_content, 'directory_analysis', args.format)
        
        print(f"✅ 报告生成完成")
        print(f"📄 报告已保存到: {report_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"报告生成出错: {str(e)}")
        print(f"❌ 报告生成失败: {str(e)}")
        return False


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # 设置日志
    setup_logging(args.config)
    logger = get_logger()
    
    logger.info(f"启动文件整理器: {args.command}")
    
    # 根据命令执行相应功能
    try:
        if args.command == 'organize':
            success = handle_organize(args)
        elif args.command == 'smart-organize':
            success = handle_smart_organize(args)
        elif args.command == 'analyze-only':
            success = handle_analyze_only(args)
        elif args.command == 'enhanced-analyze':
            success = handle_enhanced_analyze(args)
        elif args.command == 'plan-only':
            success = handle_plan_only(args)
        elif args.command == 'execute-plan':
            success = handle_execute_plan(args)
        elif args.command == 'undo-session':
            success = handle_undo_session(args)
        elif args.command == 'list-sessions':
            success = handle_list_sessions(args)
        elif args.command == 'scan-duplicates':
            success = handle_scan_duplicates(args)
        elif args.command == 'generate-report':
            success = handle_generate_report(args)
        else:
            logger.error(f"未知命令: {args.command}")
            return 1
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        print("\n⚠️  操作已被用户中断")
        return 1
    except Exception as e:
        logger.error(f"未预期的错误: {str(e)}")
        print(f"❌ 发生未预期的错误: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())