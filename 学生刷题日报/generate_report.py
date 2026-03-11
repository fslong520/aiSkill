#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智国 OJ 学生刷题日报生成器
自动抓取 24 小时内的提交数据，生成 Markdown 和 HTML 日报
"""

import json
import re
from datetime import datetime
from collections import defaultdict

# 管理员/教师排除名单
ADMIN_USERS = {
    'long long', 'lihong', 'shawn_liu', 'arling', 'admin',
    'teacher', 'test', 'hoj', 'system'
}

# 题目类型映射
PROBLEM_TYPES = {
    '字符串': ['字符串', '加密', '解密', '反转', '单词', '字符'],
    '循环嵌套': ['循环', '图形', '打印', '图案'],
    '模拟算法': ['模拟', '管理', '过程', '游戏'],
    '动态规划': ['动态', 'dp', '最优', '计数'],
    '贪心算法': ['贪心', '局部'],
    '搜索算法': ['dfs', 'bfs', '搜索', '遍历'],
    '数组': ['数组', '列表', '序列'],
    '数学': ['数学', '计算', '数论', '质数', '因子'],
}

def parse_time(time_str):
    """解析时间字符串，返回是否在 24 小时内"""
    time_str = time_str.strip()
    if '分钟前' in time_str:
        return True
    elif '小时前' in time_str:
        match = re.search(r'(\d+) 小时前', time_str)
        if match:
            hours = int(match.group(1))
            return hours < 24
    elif '天前' in time_str:
        return False
    return True

def identify_problem_type(problem_name):
    """识别题目类型"""
    for ptype, keywords in PROBLEM_TYPES.items():
        for keyword in keywords:
            if keyword in problem_name:
                return ptype
    return '其他'

def generate_report(submissions):
    """生成刷题日报"""
    # 过滤管理员
    student_subs = [s for s in submissions if s['user'] not in ADMIN_USERS]
    
    # 按学生分组
    student_data = defaultdict(lambda: {'ac_problems': set(), 'failed_problems': defaultdict(list)})
    
    for sub in student_subs:
        user = sub['user']
        problem = sub['problem'].split()[0]  # 只取题目 ID
        status = sub['status']
        
        if status == 'Accepted':
            student_data[user]['ac_problems'].add(problem)
        else:
            student_data[user]['failed_problems'][problem].append(status)
    
    # 生成总榜单
    ranking = []
    for user, data in student_data.items():
        ac_count = len(data['ac_problems'])
        if ac_count > 0:
            ranking.append((user, ac_count))
    
    ranking.sort(key=lambda x: -x[1])
    
    return ranking, student_data

def main():
    # 示例数据（从浏览器抓取的两页）
    sample_submissions = [
        # 第一页
        {'runId': '90264', 'problem': 'P7060', 'status': 'Accepted', 'user': 'ranchengxuan', 'time': '4 分钟前'},
        {'runId': '90263', 'problem': 'P7060', 'status': 'Accepted', 'user': 'long long', 'time': '6 分钟前'},
        {'runId': '90261', 'problem': 'P7060', 'status': 'Accepted', 'user': 'ranchengxuan', 'time': '10 分钟前'},
        {'runId': '90260', 'problem': 'D1527', 'status': 'Wrong Answer', 'user': 'yanwenyang', 'time': '18 分钟前'},
        {'runId': '90259', 'problem': 'D1527', 'status': 'Wrong Answer', 'user': 'yanwenyang', 'time': '21 分钟前'},
        {'runId': '90258', 'problem': 'P6706', 'status': 'Accepted', 'user': 'liuxiao', 'time': '26 分钟前'},
        {'runId': '90257', 'problem': 'D1527', 'status': 'Wrong Answer', 'user': 'yanwenyang', 'time': '27 分钟前'},
        {'runId': '90256', 'problem': 'P6706', 'status': 'Partial Accepted', 'user': 'liuxiao', 'time': '27 分钟前'},
        {'runId': '90255', 'problem': 'D1527', 'status': 'Wrong Answer', 'user': 'yanwenyang', 'time': '29 分钟前'},
        {'runId': '90254', 'problem': '4329', 'status': 'Partial Accepted', 'user': 'guojinxuan', 'time': '31 分钟前'},
        {'runId': '90253', 'problem': 'P6704', 'status': 'Accepted', 'user': 'liuxiao', 'time': '31 分钟前'},
        {'runId': '90252', 'problem': 'P7429', 'status': 'Accepted', 'user': 'liuxiao', 'time': '34 分钟前'},
        {'runId': '90251', 'problem': 'P6856', 'status': 'Accepted', 'user': 'long long', 'time': '37 分钟前'},
        {'runId': '90250', 'problem': 'T1126', 'status': 'Accepted', 'user': 'liuxiao', 'time': '44 分钟前'},
        # 第二页
        {'runId': '90249', 'problem': 'P7056', 'status': 'Accepted', 'user': 'ranchengxuan', 'time': '1 小时前'},
        {'runId': '90248', 'problem': 'D1159', 'status': 'Accepted', 'user': 'yanwenyang', 'time': '1 小时前'},
        {'runId': '90247', 'problem': 'D1159', 'status': 'Wrong Answer', 'user': 'yanwenyang', 'time': '1 小时前'},
        {'runId': '90246', 'problem': 'D1159', 'status': 'Wrong Answer', 'user': 'yanwenyang', 'time': '1 小时前'},
        {'runId': '90245', 'problem': 'CIE202603L3TEST8B', 'status': 'Accepted', 'user': 'ranchengxuan', 'time': '1 小时前'},
        {'runId': '90244', 'problem': 'CIE202603L3TEST8B', 'status': 'Time Limit Exceeded', 'user': 'ranchengxuan', 'time': '1 小时前'},
        {'runId': '90243', 'problem': 'CIE-202509-3-C', 'status': 'Accepted', 'user': 'ranchengxuan', 'time': '1 小时前'},
        {'runId': '90242', 'problem': 'CIE-202509-3-C', 'status': 'Accepted', 'user': 'long long', 'time': '1 小时前'},
        {'runId': '90241', 'problem': 'XH1035', 'status': 'Accepted', 'user': 'chenyunxi', 'time': '2 小时前'},
        {'runId': '90240', 'problem': 'XH1035', 'status': 'Accepted', 'user': 'chenyunxi', 'time': '2 小时前'},
        {'runId': '90239', 'problem': 'XH1035', 'status': 'Accepted', 'user': 'long long', 'time': '2 小时前'},
        {'runId': '90238', 'problem': 'XH1035', 'status': 'Accepted', 'user': 'chenyunxi', 'time': '2 小时前'},
        {'runId': '90237', 'problem': 'XH1035', 'status': 'Wrong Answer', 'user': 'chenyunxi', 'time': '2 小时前'},
        {'runId': '90236', 'problem': 'XH1035', 'status': 'Wrong Answer', 'user': 'chenyunxi', 'time': '2 小时前'},
        {'runId': '90235', 'problem': 'XH1035', 'status': 'Wrong Answer', 'user': 'chenyunxi', 'time': '2 小时前'},
    ]
    
    ranking, student_data = generate_report(sample_submissions)
    
    print("=== 智国 OJ 刷题日报 ===")
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("🏆 总榜单")
    print("-" * 40)
    for i, (user, ac_count) in enumerate(ranking, 1):
        medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else '🏅'
        print(f"{medal} {i}. {user}: {ac_count} 题 AC")
    print()
    print("📊 学生详情")
    print("-" * 40)
    for user, data in student_data.items():
        ac_list = list(data['ac_problems'])
        failed = {k: v for k, v in data['failed_problems'].items() if k not in ac_list}
        print(f"\n👤 {user}")
        if ac_list:
            print(f"   ✅ AC: {', '.join(ac_list)}")
        if failed:
            print(f"   🔍 未 AC: {', '.join(failed.keys())}")

if __name__ == '__main__':
    main()
