#!/usr/bin/env python3
"""
教学视频生成技能 - 手动渲染脚本
用于渲染已保存的Manim场景文件
"""

import subprocess
import sys
import argparse
from pathlib import Path


def render_file(scene_file: str, quality: str = "medium",
                format: str = "mp4", fps: int = 30,
                output: str = None) -> bool:
    """
    手动渲染Manim场景文件
    
    Args:
        scene_file: 场景文件路径
        quality: 质量
        format: 格式
        fps: 帧率
        output: 输出路径
        
    Returns:
        是否成功
    """
    scene_path = Path(scene_file)
    
    if not scene_path.exists():
        print(f"❌ 文件不存在: {scene_path}")
        return False
    
    # 构建命令
    cmd = ["manim"]
    
    if quality == "low":
        cmd.append("-ql")
    elif quality == "medium":
        cmd.append("-qm")
    elif quality == "high":
        cmd.append("-qh")
    else:
        cmd.append("-qk")
    
    cmd.extend(["-f", format])
    
    if output:
        cmd.extend(["-o", output])
    
    cmd.append(str(scene_path))
    
    print(f"🎬 渲染场景: {scene_path.name}")
    print(f"   命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=False,
            text=True,
            timeout=300
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ 渲染超时")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def render_all_in_dir(directory: str, quality: str = "medium",
                       format: str = "mp4") -> tuple:
    """
    渲染目录下所有.py文件
    
    Returns:
        (成功数, 失败数)
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"❌ 目录不存在: {dir_path}")
        return 0, 0
    
    py_files = list(dir_path.glob("*.py"))
    
    if not py_files:
        print(f"❌ 目录中没有.py文件")
        return 0, 0
    
    print(f"📁 发现 {len(py_files)} 个场景文件")
    
    success = 0
    failed = 0
    
    for py_file in py_files:
        print(f"\n[{success + failed + 1}/{len(py_files)}] {py_file.name}")
        if render_file(str(py_file), quality, format):
            success += 1
        else:
            failed += 1
    
    return success, failed


def main():
    parser = argparse.ArgumentParser(
        description="手动渲染Manim场景文件"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 单文件渲染
    file_parser = subparsers.add_parser("file", help="渲染单个文件")
    file_parser.add_argument("scene_file", help="场景文件路径")
    file_parser.add_argument("-q", "--quality", choices=["low", "medium", "high", "best"],
                            default="medium", help="视频质量")
    file_parser.add_argument("-f", "--format", choices=["mp4", "gif", "webm"],
                            default="mp4", help="输出格式")
    file_parser.add_argument("-o", "--output", help="输出路径")
    
    # 批量渲染
    dir_parser = subparsers.add_parser("dir", help="渲染目录下所有文件")
    dir_parser.add_argument("directory", help="目录路径")
    dir_parser.add_argument("-q", "--quality", choices=["low", "medium", "high", "best"],
                           default="medium", help="视频质量")
    dir_parser.add_argument("-f", "--format", choices=["mp4", "gif", "webm"],
                           default="mp4", help="输出格式")
    
    args = parser.parse_args()
    
    if args.command == "file":
        success = render_file(
            args.scene_file,
            quality=args.quality,
            format=args.format,
            output=args.output
        )
        sys.exit(0 if success else 1)
    
    elif args.command == "dir":
        success, failed = render_all_in_dir(
            args.directory,
            quality=args.quality,
            format=args.format
        )
        print(f"\n✅ 完成: {success} 成功, {failed} 失败")
        sys.exit(0 if failed == 0 else 1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
