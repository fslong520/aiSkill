#!/usr/bin/env python3
"""
教学视频生成技能 - 输出验证脚本
验证生成的视频文件是否有效
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional


class VideoValidator:
    def __init__(self):
        self.scripts_dir = Path(__file__).parent.parent
        self.output_dir = self.scripts_dir / "output"
    
    def check_file_exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        if not os.path.exists(file_path):
            print(f"   ✗ 文件不存在: {file_path}")
            return False
        return True
    
    def check_file_size(self, file_path: str, min_size_kb: int = 10) -> bool:
        """检查文件大小"""
        size = os.path.getsize(file_path)
        size_kb = size / 1024
        
        if size_kb < min_size_kb:
            print(f"   ⚠️  文件过小 ({size_kb:.1f}KB)，可能生成失败")
            return False
        return True
    
    def check_video_format(self, file_path: str) -> bool:
        """检查视频格式"""
        valid_extensions = [".mp4", ".gif", ".webm"]
        ext = Path(file_path).suffix.lower()
        
        if ext not in valid_extensions:
            print(f"   ⚠️  未知格式: {ext}")
            return False
        
        return True
    
    def check_video_header(self, file_path: str) -> bool:
        """检查视频文件头"""
        try:
            with open(file_path, "rb") as f:
                header = f.read(12)
                
            # MP4 头
            if file_path.endswith(".mp4"):
                if not (header[:4] == b'\x00\x00\x00' or header[:4] == b'ftyp'):
                    print("   ⚠️  MP4文件头可能损坏")
                    return False
            
            # GIF 头
            elif file_path.endswith(".gif"):
                if header[:3] != b'GIF':
                    print("   ⚠️  GIF文件头损坏")
                    return False
            
            return True
        except Exception as e:
            print(f"   ✗ 读取文件失败: {e}")
            return False
    
    def validate_single(self, file_path: str) -> bool:
        """验证单个视频文件"""
        print(f"\n🔍 验证: {file_path}")
        
        if not self.check_file_exists(file_path):
            return False
        
        if not self.check_file_size(file_path):
            return False
        
        if not self.check_video_format(file_path):
            return False
        
        if not self.check_video_header(file_path):
            return False
        
        print(f"   ✓ 文件验证通过")
        return True
    
    def validate_output_dir(self) -> bool:
        """验证输出目录中的所有文件"""
        if not self.output_dir.exists():
            print(f"   ✗ 输出目录不存在: {self.output_dir}")
            return False
        
        files = list(self.output_dir.glob("*.mp4")) + \
                list(self.output_dir.glob("*.gif")) + \
                list(self.output_dir.glob("*.webm"))
        
        if not files:
            print(f"   ✗ 输出目录中没有视频文件")
            return False
        
        print(f"\n📁 验证输出目录: {self.output_dir}")
        print(f"   找到 {len(files)} 个视频文件")
        
        valid_count = 0
        for file_path in files:
            if self.validate_single(str(file_path)):
                valid_count += 1
        
        print(f"\n✓ 验证完成: {valid_count}/{len(files)} 通过")
        return valid_count == len(files)
    
    def print_info(self, file_path: str) -> None:
        """打印文件信息"""
        if not self.check_file_exists(file_path):
            return
        
        stat = os.stat(file_path)
        print(f"\n📊 文件信息:")
        print(f"   路径: {file_path}")
        print(f"   大小: {stat.st_size / 1024:.1f} KB")
        print(f"   修改时间: {stat.st_mtime}")
        print(f"   格式: {Path(file_path).suffix}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate generated video files"
    )
    parser.add_argument("path", nargs="?", help="Path to video file or directory")
    parser.add_argument("--info", action="store_true", help="Show file info")
    parser.add_argument("--dir", action="store_true", help="Validate output directory")
    
    args = parser.parse_args()
    
    validator = VideoValidator()
    
    if args.dir or (args.path and os.path.isdir(args.path)):
        target = args.path or str(validator.output_dir)
        return 0 if validator.validate_output_dir() else 1
    
    elif args.path:
        if args.info:
            validator.print_info(args.path)
        return 0 if validator.validate_single(args.path) else 1
    
    else:
        # 默认验证输出目录
        return 0 if validator.validate_output_dir() else 1


if __name__ == "__main__":
    sys.exit(main())
