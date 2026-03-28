#!/usr/bin/env python3
"""
InkPot 墨池 - 知识管理工具
使用简单的 KV 文本格式存储，避免 JSON 格式问题
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict


class InkPot:
    """墨池知识管理器 - KV 文本格式版"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "db"
        self.knowledge_path = self.base_path / "knowledge"

        # 确保目录存在
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.knowledge_path.mkdir(parents=True, exist_ok=True)

        # 数据文件路径（改用 .txt）
        self.index_file = self.db_path / "knowledge_index.txt"
        self.profile_file = self.db_path / "user_profile.txt"
        self.log_file = self.db_path / "learning_log.txt"

        # 加载数据
        self._load_data()

    # ==================== KV 格式解析器 ====================

    def _parse_kv_block(self, block: str) -> Dict:
        """解析单个 KV 块"""
        result = {}
        lines = block.strip().split('\n')
        current_key = None
        current_value = []
        
        for line in lines:
            # 空行跳过
            if not line.strip():
                continue
            
            # 检查是否是新字段 (key: value)
            if ':' in line:
                parts = line.split(':', 1)
                # 保存上一个字段
                if current_key:
                    value = '\n'.join(current_value).strip()
                    # 处理列表字段
                    if current_key in ['tags', 'related']:
                        result[current_key] = [t.strip() for t in value.split(',') if t.strip()]
                    else:
                        result[current_key] = value
                # 开始新字段
                current_key = parts[0].strip()
                current_value = [parts[1].strip() if len(parts) > 1 else '']
            else:
                # 续行
                if current_key:
                    current_value.append(line.strip())
        
        # 保存最后一个字段
        if current_key:
            value = '\n'.join(current_value).strip()
            if current_key in ['tags', 'related']:
                result[current_key] = [t.strip() for t in value.split(',') if t.strip()]
            else:
                result[current_key] = value
        
        return result

    def _format_kv_block(self, data: Dict, name: str) -> str:
        """格式化为 KV 块"""
        lines = [f"=== {name} ==="]
        
        for key, value in data.items():
            if key == 'name':
                continue  # 名字已经在标题里
            if isinstance(value, list):
                lines.append(f"{key}: {','.join(value)}")
            elif isinstance(value, str) and '\n' in value:
                # 多行文本，用续行格式
                lines.append(f"{key}: {value.split('\n')[0]}")
                for subline in value.split('\n')[1:]:
                    lines.append(f"  {subline}")
            else:
                lines.append(f"{key}: {value}")
        
        return '\n'.join(lines)

    def _parse_kv_file(self, filepath: Path) -> Dict[str, Dict]:
        """解析整个 KV 文件"""
        if not filepath.exists():
            return {}
        
        content = filepath.read_text(encoding='utf-8')
        blocks = content.split('\n=== ')
        
        result = {}
        for block in blocks:
            if not block.strip():
                continue
            
            # 修复第一个块的前缀
            if block.startswith('=== '):
                block = block[4:]
            
            # 提取名字
            first_line = block.split('\n')[0]
            name = first_line.split('===')[0].strip()
            
            # 解析内容
            data = self._parse_kv_block(block)
            if name:
                result[name] = data
        
        return result

    def _write_kv_file(self, filepath: Path, data: Dict[str, Dict]):
        """写入 KV 文件"""
        blocks = []
        for name, values in data.items():
            blocks.append(self._format_kv_block(values, name))
        
        content = '\n\n'.join(blocks)
        filepath.write_text(content, encoding='utf-8')

    # ==================== 数据加载 ====================

    def _load_data(self):
        """加载所有数据"""
        # 加载知识索引
        self.index_data = self._parse_kv_file(self.index_file)
        
        # 加载用户画像
        self.profile_data = self._parse_kv_file(self.profile_file)
        if 'identity' not in self.profile_data:
            self.profile_data['identity'] = {
                'primary_role': '',
                'confidence': '0'
            }
        
        # 加载学习日志（简单列表格式）
        self.log_data = []
        if self.log_file.exists():
            content = self.log_file.read_text(encoding='utf-8')
            for line in content.strip().split('\n'):
                if line.strip() and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        self.log_data.append({
                            'timestamp': parts[0].strip(),
                            'knowledge': parts[1].strip(),
                            'event': parts[2].strip(),
                            'trigger': parts[3].strip()
                        })

    def _save_data(self):
        """保存所有数据"""
        self._write_kv_file(self.index_file, self.index_data)
        self._write_kv_file(self.profile_file, self.profile_data)
        
        # 写入学习日志（简单行格式）
        log_lines = []
        for log in self.log_data:
            log_lines.append(f"{log['timestamp']} | {log['knowledge']} | {log['event']} | {log['trigger']}")
        self.log_file.write_text('\n'.join(log_lines), encoding='utf-8')

    # ==================== 知识点操作 ====================

    def add_knowledge(self, name: str, category: str, summary: str = "",
                      tags: List[str] = None, related: List[str] = None,
                      source: str = "对话") -> Dict:
        """添加新知识点"""
        if tags is None:
            tags = []
        if related is None:
            related = []

        # 生成 ID
        knowledge_id = f"{category[:2]}_{len(self.index_data) + 1:03d}"

        # 创建知识点文件
        knowledge_file = self.knowledge_path / category / f"{name}.md"
        knowledge_file.parent.mkdir(parents=True, exist_ok=True)

        # 写入 Markdown 文件
        md_content = f"""# {name}

> 分类：{category}
> 标签：{', '.join(tags)}
> 学习次数：1
> 掌握程度：了解

## 概述

{summary}

## 相关知识点

{', '.join(related) if related else '暂无'}

---
*首次学习：{datetime.now().strftime('%Y-%m-%d')}*
"""
        knowledge_file.write_text(md_content, encoding='utf-8')

        # 添加到索引
        self.index_data[name] = {
            'id': knowledge_id,
            'category': category,
            'tags': tags,
            'summary': summary,
            'related': related,
            'file': str(knowledge_file.relative_to(self.base_path)),
            'learning_count': '1',
            'mastery': '了解',
            'first_learned': datetime.now().strftime('%Y-%m-%d'),
            'last_learned': datetime.now().strftime('%Y-%m-%d'),
            'source': source
        }

        # 添加学习日志
        self.log_data.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'knowledge': name,
            'event': '新增',
            'trigger': source
        })

        self._save_data()

        return self.index_data[name]

    def update_knowledge(self, name: str, **kwargs) -> Optional[Dict]:
        """更新知识点"""
        if name not in self.index_data:
            return None

        knowledge = self.index_data[name]

        # 更新字段
        for key, value in kwargs.items():
            knowledge[key] = value

        # 更新学习次数
        count = int(knowledge.get('learning_count', '1'))
        knowledge['learning_count'] = str(count + 1)
        knowledge['last_learned'] = datetime.now().strftime('%Y-%m-%d')

        # 添加学习日志
        self.log_data.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'knowledge': name,
            'event': '复习',
            'trigger': kwargs.get('source', '复习')
        })

        self._save_data()

        return knowledge

    def get_knowledge(self, name: str) -> Optional[Dict]:
        """获取知识点"""
        return self.index_data.get(name)

    def search_knowledge(self, keyword: str = None, category: str = None) -> List[Dict]:
        """搜索知识点"""
        results = []

        for name, knowledge in self.index_data.items():
            # 关键词匹配
            if keyword:
                keyword_lower = keyword.lower()
                if keyword_lower not in name.lower():
                    if keyword_lower not in knowledge.get('summary', '').lower():
                        if keyword_lower not in ','.join(knowledge.get('tags', [])).lower():
                            continue

            # 分类匹配
            if category and knowledge.get('category') != category:
                continue

            results.append({'name': name, **knowledge})

        return results

    def get_review_candidates(self, limit: int = 5) -> List[Dict]:
        """获取需要复习的知识点"""
        # 优先级：掌握程度低 > 学习次数少
        priority = {'了解': 0, '理解': 1, '熟练': 2, '精通': 3}

        candidates = []
        for name, knowledge in self.index_data.items():
            mastery = knowledge.get('mastery', '了解')
            count = int(knowledge.get('learning_count', '1'))
            candidates.append({
                'name': name,
                'priority': priority.get(mastery, 0),
                'count': count,
                **knowledge
            })

        # 排序
        candidates.sort(key=lambda x: (x['priority'], -x['count']))

        return candidates[:limit]

    # ==================== 用户画像 ====================

    def update_user_profile(self, action_type: str, topic: str):
        """更新用户行为画像"""
        # 初始化 identity 块
        if 'identity' not in self.profile_data:
            self.profile_data['identity'] = {
                'primary_role': '',
                'secondary_roles': '',
                'confidence': '0'
            }

        # 每个 action 作为独立块（key 格式: action:<type>）
        action_key = f'action:{action_type}'
        if action_key not in self.profile_data:
            self.profile_data[action_key] = {
                'count': '0',
                'topics': ''
            }
        
        action = self.profile_data[action_key]
        
        # 更新计数
        count = int(action.get('count', '0'))
        action['count'] = str(count + 1)
        
        # 更新 topics（逗号分隔）
        topics = action.get('topics', '')
        if topics:
            action['topics'] = f"{topics},{topic}"
        else:
            action['topics'] = topic

        self._save_data()

    def infer_user_identity(self) -> Dict:
        """推断用户身份"""
        # 根据行为推断身份
        identity_hints = {
            '搬题': '信奥竞赛教练',
            'ask_concept': '学习者',
            'write_code': '开发者',
            '算法讲解': '教学者'
        }

        # 统计各身份得分（从 action:<type> 块读取）
        scores = {}
        for key, data in self.profile_data.items():
            if key.startswith('action:'):
                action_type = key[7:]  # 去掉 'action:' 前缀
                identity = identity_hints.get(action_type, '')
                if identity and isinstance(data, dict):
                    count = int(data.get('count', '0'))
                    scores[identity] = scores.get(identity, 0) + count

        # 找出主要身份
        if scores:
            primary = max(scores.items(), key=lambda x: x[1])
            if 'identity' not in self.profile_data:
                self.profile_data['identity'] = {}
            self.profile_data['identity']['primary_role'] = primary[0]
            self.profile_data['identity']['confidence'] = str(min(primary[1] / 10, 1.0))

        self._save_data()
        return self.profile_data.get('identity', {})

    # ==================== 统计 ====================

    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = {
            'total_knowledge': len(self.index_data),
            'total_logs': len(self.log_data),
            'categories': {},
            'mastery': {'了解': 0, '理解': 0, '熟练': 0, '精通': 0}
        }

        for name, knowledge in self.index_data.items():
            cat = knowledge.get('category', '其他')
            stats['categories'][cat] = stats['categories'].get(cat, 0) + 1

            mastery = knowledge.get('mastery', '了解')
            stats['mastery'][mastery] = stats['mastery'].get(mastery, 0) + 1

        return stats


# ==================== CLI ====================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="墨池知识管理工具")
    parser.add_argument("--path", default=".", help="墨池技能路径")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="添加知识点")
    add_parser.add_argument("name", help="知识点名称")
    add_parser.add_argument("--category", required=True, help="分类")
    add_parser.add_argument("--tags", default="", help="标签(逗号分隔)")
    add_parser.add_argument("--summary", default="", help="摘要")

    # search
    search_parser = subparsers.add_parser("search", help="搜索")
    search_parser.add_argument("keyword", help="关键词")

    # stats
    subparsers.add_parser("stats", help="统计")

    # review
    review_parser = subparsers.add_parser("review", help="复习推荐")
    review_parser.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()
    inkpot = InkPot(args.path)

    if args.command == "add":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        result = inkpot.add_knowledge(args.name, args.category, args.summary, tags)
        print(f"✓ 添加: {args.name}")

    elif args.command == "search":
        results = inkpot.search_knowledge(args.keyword)
        print(f"找到 {len(results)} 个:")
        for r in results:
            print(f"  - {r['name']} [{r.get('mastery', '了解')}]")

    elif args.command == "stats":
        stats = inkpot.get_stats()
        print(f"知识点: {stats['total_knowledge']}")
        print(f"日志: {stats['total_logs']}")
        print("分类:")
        for cat, count in stats['categories'].items():
            print(f"  {cat}: {count}")

    elif args.command == "review":
        candidates = inkpot.get_review_candidates(args.limit)
        for i, c in enumerate(candidates, 1):
            print(f"{i}. {c['name']} [{c.get('mastery', '了解')}]")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()