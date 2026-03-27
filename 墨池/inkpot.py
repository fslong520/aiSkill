#!/usr/bin/env python3
"""
InkPot 墨池 - 知识管理工具
提供知识点的增删改查、索引管理、用户画像更新等功能
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class InkPot:
    """墨池知识管理器"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "db"
        self.knowledge_path = self.base_path / "knowledge"

        # 确保目录存在
        self.db_path.mkdir(parents=True, exist_ok=True)

        # 数据库文件路径
        self.index_file = self.db_path / "knowledge_index.json"
        self.profile_file = self.db_path / "user_profile.json"
        self.log_file = self.db_path / "learning_log.json"

        # 加载数据库
        self._load_databases()

    def _load_databases(self):
        """加载数据库"""
        # 加载知识索引
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index_data = json.load(f)
        else:
            self.index_data = {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "stats": {"total_knowledge": 0, "total_categories": 0, "total_learning_events": 0},
                "index": {},
                "search_index": {"by_category": {}, "by_tags": {}}
            }

        # 加载用户画像
        if self.profile_file.exists():
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                self.profile_data = json.load(f)
        else:
            self.profile_data = {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "profile": {
                    "identity": {"primary_role": "", "secondary_roles": [], "confidence": 0},
                    "expertise": {},
                    "interests": [],
                    "common_tasks": [],
                    "learning_patterns": {"preferred_depth": "适中", "preferred_style": "解释+代码"}
                },
                "behavior_log": []
            }

        # 加载学习日志
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.log_data = json.load(f)
        else:
            self.log_data = {"version": "1.0", "logs": []}

    def _save_databases(self):
        """保存数据库"""
        self.index_data["last_updated"] = datetime.now().isoformat()

        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index_data, f, ensure_ascii=False, indent=2)

        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profile_data, ensure_ascii=False, indent=2, fp=f)

        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.log_data, ensure_ascii=False, indent=2, fp=f)

    # ==================== 知识点操作 ====================

    def add_knowledge(self, name: str, category: str, subcategory: str = "",
                      tags: list = None, summary: str = "", related: list = None,
                      source: str = "用户提问") -> dict:
        """添加新知识点"""
        if tags is None:
            tags = []
        if related is None:
            related = []

        # 生成ID
        knowledge_id = f"{category[:3]}_{len(self.index_data['index']) + 1:03d}"

        # 添加到索引
        self.index_data["index"][name] = {
            "id": knowledge_id,
            "file": f"knowledge/{category}/{name}.md",
            "category": category,
            "subcategory": subcategory,
            "tags": tags,
            "summary": summary,
            "learning_count": 1,
            "mastery_level": "了解",
            "first_learned": datetime.now().strftime("%Y-%m-%d"),
            "last_learned": datetime.now().strftime("%Y-%m-%d"),
            "related": related,
            "source": source
        }

        # 更新搜索索引
        if category not in self.index_data["search_index"]["by_category"]:
            self.index_data["search_index"]["by_category"][category] = []
        self.index_data["search_index"]["by_category"][category].append(name)

        for tag in tags:
            if tag not in self.index_data["search_index"]["by_tags"]:
                self.index_data["search_index"]["by_tags"][tag] = []
            self.index_data["search_index"]["by_tags"][tag].append(name)

        # 更新统计
        self.index_data["stats"]["total_knowledge"] = len(self.index_data["index"])
        self.index_data["stats"]["total_categories"] = len(self.index_data["search_index"]["by_category"])
        self.index_data["stats"]["total_learning_events"] += 1

        # 添加学习日志
        self._add_learning_log(knowledge_id, name, "new_learning", source)

        self._save_databases()

        return self.index_data["index"][name]

    def update_knowledge(self, name: str, **kwargs) -> Optional[dict]:
        """更新知识点"""
        if name not in self.index_data["index"]:
            return None

        knowledge = self.index_data["index"][name]

        # 更新字段
        for key, value in kwargs.items():
            if key in knowledge:
                knowledge[key] = value

        # 更新学习次数和日期
        knowledge["learning_count"] += 1
        knowledge["last_learned"] = datetime.now().strftime("%Y-%m-%d")

        # 添加学习日志
        self._add_learning_log(knowledge["id"], name, "reinforcement", kwargs.get("source", "复习"))

        self._save_databases()

        return knowledge

    def get_knowledge(self, name: str) -> Optional[dict]:
        """获取知识点"""
        return self.index_data["index"].get(name)

    def search_knowledge(self, keyword: str = None, category: str = None,
                         tag: str = None, mastery_level: str = None) -> list:
        """搜索知识点"""
        results = []

        for name, knowledge in self.index_data["index"].items():
            # 关键词匹配
            if keyword:
                keyword_lower = keyword.lower()
                if (keyword_lower not in name.lower() and
                    keyword_lower not in knowledge.get("summary", "").lower() and
                    keyword_lower not in " ".join(knowledge.get("tags", [])).lower()):
                    continue

            # 分类匹配
            if category and knowledge.get("category") != category:
                continue

            # 标签匹配
            if tag and tag not in knowledge.get("tags", []):
                continue

            # 掌握程度匹配
            if mastery_level and knowledge.get("mastery_level") != mastery_level:
                continue

            results.append({"name": name, **knowledge})

        return results

    def get_related_knowledge(self, name: str) -> list:
        """获取相关知识点"""
        if name not in self.index_data["index"]:
            return []

        related = self.index_data["index"][name].get("related", [])
        results = []

        for r_name in related:
            if r_name in self.index_data["index"]:
                results.append({"name": r_name, **self.index_data["index"][r_name]})

        return results

    def get_review_candidates(self, limit: int = 5) -> list:
        """获取需要复习的知识点（基于掌握程度和学习次数）"""
        # 优先级：掌握程度低 > 学习次数少
        priority = {"了解": 0, "理解": 1, "熟练": 2, "精通": 3}

        candidates = []
        for name, knowledge in self.index_data["index"].items():
            mastery = knowledge.get("mastery_level", "了解")
            count = knowledge.get("learning_count", 1)
            candidates.append({
                "name": name,
                "mastery_priority": priority.get(mastery, 0),
                "count": count,
                **knowledge
            })

        # 排序：掌握程度低的优先，相同则学习次数少的优先
        candidates.sort(key=lambda x: (x["mastery_priority"], -x["count"]))

        return candidates[:limit]

    # ==================== 学习日志 ====================

    def _add_learning_log(self, knowledge_id: str, knowledge_name: str,
                          event_type: str, trigger: str):
        """添加学习日志"""
        log_entry = {
            "id": f"log_{len(self.log_data['logs']) + 1:03d}",
            "timestamp": datetime.now().isoformat(),
            "knowledge_id": knowledge_id,
            "knowledge_name": knowledge_name,
            "event_type": event_type,
            "trigger": trigger
        }
        self.log_data["logs"].append(log_entry)

    # ==================== 用户画像 ====================

    def update_user_profile(self, action_type: str, topic: str):
        """更新用户行为画像"""
        today = datetime.now().strftime("%Y-%m-%d")

        # 查找今天的日志
        today_log = None
        for log in self.profile_data["behavior_log"]:
            if log["date"] == today:
                today_log = log
                break

        if not today_log:
            today_log = {"date": today, "actions": []}
            self.profile_data["behavior_log"].append(today_log)

        # 添加行为
        today_log["actions"].append({
            "type": action_type,
            "topic": topic,
            "timestamp": datetime.now().strftime("%H:%M")
        })

        # 更新常见任务统计
        task_found = False
        for task in self.profile_data["profile"]["common_tasks"]:
            if task["task"] == action_type:
                task["count"] += 1
                task_found = True
                break

        if not task_found:
            self.profile_data["profile"]["common_tasks"].append({"task": action_type, "count": 1})

        self.profile_data["last_updated"] = datetime.now().isoformat()
        self._save_databases()

    def infer_user_identity(self) -> dict:
        """推断用户身份"""
        tasks = self.profile_data["profile"]["common_tasks"]

        # 根据行为推断身份
        identity_hints = {
            "搬题": "信奥竞赛教练",
            "ask_concept": "学习者",
            "write_code": "开发者",
            "debug_code": "开发者",
            "算法讲解": "教学者"
        }

        # 统计各身份得分
        identity_scores = {}
        for task in tasks:
            identity = identity_hints.get(task["task"], "")
            if identity:
                identity_scores[identity] = identity_scores.get(identity, 0) + task["count"]

        # 找出主要身份
        if identity_scores:
            primary = max(identity_scores.items(), key=lambda x: x[1])
            self.profile_data["profile"]["identity"]["primary_role"] = primary[0]
            self.profile_data["profile"]["identity"]["confidence"] = min(primary[1] / 10, 1.0)

        return self.profile_data["profile"]["identity"]

    # ==================== 统计报告 ====================

    def get_stats(self) -> dict:
        """获取统计信息"""
        stats = {
            "total_knowledge": len(self.index_data["index"]),
            "total_learning_events": self.index_data["stats"]["total_learning_events"],
            "categories": {},
            "mastery_distribution": {"了解": 0, "理解": 0, "熟练": 0, "精通": 0}
        }

        for name, knowledge in self.index_data["index"].items():
            cat = knowledge.get("category", "其他")
            stats["categories"][cat] = stats["categories"].get(cat, 0) + 1

            mastery = knowledge.get("mastery_level", "了解")
            stats["mastery_distribution"][mastery] = stats["mastery_distribution"].get(mastery, 0) + 1

        return stats


# ==================== CLI 接口 ====================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="InkPot 墨池知识管理工具")
    parser.add_argument("--path", default=".", help="墨池技能路径")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # add 命令
    add_parser = subparsers.add_parser("add", help="添加知识点")
    add_parser.add_argument("name", help="知识点名称")
    add_parser.add_argument("--category", required=True, help="分类")
    add_parser.add_argument("--subcategory", default="", help="子分类")
    add_parser.add_argument("--tags", default="", help="标签(逗号分隔)")
    add_parser.add_argument("--summary", default="", help="摘要")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索知识点")
    search_parser.add_argument("keyword", help="关键词")
    search_parser.add_argument("--category", help="分类筛选")
    search_parser.add_argument("--tag", help="标签筛选")

    # stats 命令
    subparsers.add_parser("stats", help="统计信息")

    # review 命令
    review_parser = subparsers.add_parser("review", help="获取复习推荐")
    review_parser.add_argument("--limit", type=int, default=5, help="数量限制")

    args = parser.parse_args()

    inkpot = InkPot(args.path)

    if args.command == "add":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        result = inkpot.add_knowledge(
            name=args.name,
            category=args.category,
            subcategory=args.subcategory,
            tags=tags,
            summary=args.summary
        )
        print(f"✓ 添加知识点: {args.name}")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "search":
        results = inkpot.search_knowledge(
            keyword=args.keyword,
            category=args.category,
            tag=args.tag
        )
        print(f"找到 {len(results)} 个知识点:")
        for r in results:
            print(f"  - {r['name']} [{r.get('mastery_level', '了解')}]")

    elif args.command == "stats":
        stats = inkpot.get_stats()
        print("=== 墨池统计 ===")
        print(f"知识点总数: {stats['total_knowledge']}")
        print(f"学习事件总数: {stats['total_learning_events']}")
        print("\n分类分布:")
        for cat, count in stats['categories'].items():
            print(f"  {cat}: {count}")
        print("\n掌握程度分布:")
        for level, count in stats['mastery_distribution'].items():
            print(f"  {level}: {count}")

    elif args.command == "review":
        candidates = inkpot.get_review_candidates(limit=args.limit)
        print("=== 复习推荐 ===")
        for i, c in enumerate(candidates, 1):
            print(f"{i}. {c['name']} [{c.get('mastery_level', '了解')}] - 学习{c.get('learning_count', 0)}次")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()