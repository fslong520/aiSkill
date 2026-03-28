#!/usr/bin/env python3
"""
墨池快速记录接口
用于 AI 在对话中自动记录知识点
使用简单 KV 文本格式，避免 JSON 格式问题
"""

import sys
from pathlib import Path
from datetime import datetime

# 导入 InkPot 类
sys.path.insert(0, str(Path(__file__).parent))
from inkpot import InkPot


def record_knowledge(topic: str, category: str, summary: str, tags: str = ""):
    """
    快速记录知识点
    
    Args:
        topic: 知识点名称
        category: 分类（如：算法数据结构、编程语言、数学等）
        summary: 知识点摘要
        tags: 标签（逗号分隔）
    """
    try:
        base_path = Path(__file__).parent
        inkpot = InkPot(str(base_path))
        
        # 检查是否已存在
        existing = inkpot.get_knowledge(topic)
        
        # 解析标签
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        
        if existing:
            # 更新已有知识点
            result = inkpot.update_knowledge(
                topic,
                summary=summary,
                source="对话学习",
                tags=tag_list
            )
            print(f"✓ 更新知识点：{topic}")
        else:
            # 添加新知识点
            result = inkpot.add_knowledge(
                name=topic,
                category=category,
                tags=tag_list,
                summary=summary,
                source="对话学习"
            )
            print(f"✓ 新增知识点：{topic}")
        
        # 同时记录用户行为
        inkpot.update_user_profile("ask_concept", topic)
        
        return result
        
    except Exception as e:
        print(f"✗ 记录失败：{e}")
        return None


def record_code_practice(topic: str, language: str = "C++"):
    """记录代码练习行为"""
    try:
        base_path = Path(__file__).parent
        inkpot = InkPot(str(base_path))
        inkpot.update_user_profile("write_code", f"{language}:{topic}")
        print(f"✓ 记录代码练习：{topic} ({language})")
    except Exception as e:
        print(f"✗ 记录失败：{e}")


def record_teaching(topic: str):
    """记录教学行为"""
    try:
        base_path = Path(__file__).parent
        inkpot = InkPot(str(base_path))
        inkpot.update_user_profile("算法讲解", topic)
        print(f"✓ 记录教学：{topic}")
    except Exception as e:
        print(f"✗ 记录失败：{e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="墨池快速记录接口")
    parser.add_argument("--action", required=True, 
                       choices=["knowledge", "code", "teaching"],
                       help="记录类型")
    parser.add_argument("--topic", required=True, help="主题")
    parser.add_argument("--category", default="通用", help="分类（仅 knowledge）")
    parser.add_argument("--summary", default="", help="摘要（仅 knowledge）")
    parser.add_argument("--tags", default="", help="标签（仅 knowledge）")
    parser.add_argument("--language", default="C++", help="编程语言（仅 code）")
    
    args = parser.parse_args()
    
    if args.action == "knowledge":
        record_knowledge(args.topic, args.category, args.summary, args.tags)
    elif args.action == "code":
        record_code_practice(args.topic, args.language)
    elif args.action == "teaching":
        record_teaching(args.topic)