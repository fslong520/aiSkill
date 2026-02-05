#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News 技能全面测试脚本
"""
import subprocess
import sys
import json
from pathlib import Path

# 设置 UTF-8 输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 设置路径
SCRIPT_DIR = Path(__file__).parent / "scripts"
PYTHON = sys.executable

def run_test(name, args, expected_min=1):
    """运行单个测试"""
    print(f"\n{'='*60}")
    print(f"[TEST] {name}")
    print(f"{'='*60}")

    cmd = [PYTHON, str(SCRIPT_DIR / "fetch_news.py")] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )

        # 提取 JSON 输出（如果有）
        output = result.stdout
        stderr = result.stderr

        if '--format json' in args:
            try:
                # 过滤掉日志行，找到 JSON 数组开始
                lines = output.split('\n')
                json_start = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith('['):
                        json_start = i
                        break

                if json_start >= 0:
                    json_text = '\n'.join(lines[json_start:])
                    data = json.loads(json_text)
                    count = len(data) if isinstance(data, list) else 1
                    print(f"[OK] 获取 {count} 条数据")
                    if count >= expected_min:
                        print(f"[OK] 数据量符合预期 (>={expected_min})")
                        return True
                    else:
                        print(f"[WARN] 数据量不足: {count} < {expected_min}")
                        return False
                else:
                    print(f"[WARN] 未找到 JSON 输出")
                    print(f"[DEBUG] stdout: {output[:200]}")
                    print(f"[DEBUG] stderr: {stderr[:200]}")
                    return False
            except Exception as e:
                print(f"[WARN] JSON 解析失败: {e}")
                print(f"[DEBUG] stdout: {output[:200]}")
                return False
        else:
            # Markdown/HTML 输出检查
            if '##' in output or '###' in output or '<html' in output.lower():
                print(f"[OK] 格式正常")
                return True
            else:
                print(f"[WARN] 格式异常")
                print(f"[DEBUG] output: {output[:200]}")
                return False

    except subprocess.TimeoutExpired:
        print(f"[FAIL] 超时")
        return False
    except Exception as e:
        print(f"[FAIL] 错误: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("[TEST SUITE] News Skill Full Test")
    print("="*60)

    tests = [
        # 测试 1: 单个数据源
        ("Hacker News 数据源", ["--source", "hackernews", "--limit", "5", "--format", "json"], 3),

        # 测试 2: 多个数据源
        ("多数据源组合", ["--source", "hackernews,github", "--limit", "5", "--format", "json"], 5),

        # 测试 3: 关键词过滤
        ("关键词过滤", ["--source", "all", "--keyword", "AI", "--limit", "5", "--format", "json"], 1),

        # 测试 4: Markdown 输出
        ("Markdown 输出", ["--source", "hackernews", "--limit", "3", "--format", "markdown"], 0),

        # 测试 5: HTML 输出
        ("HTML 输出", ["--source", "hackernews", "--limit", "3", "--format", "html"], 0),

        # 测试 6: 微博热搜
        ("微博热搜", ["--source", "weibo", "--limit", "5", "--format", "json"], 3),

        # 测试 7: GitHub Trending
        ("GitHub Trending", ["--source", "github", "--limit", "5", "--format", "json"], 3),

        # 测试 8: 中文数据源
        ("36Kr 中文数据源", ["--source", "36kr", "--limit", "5", "--format", "json"], 3),

        # 测试 9: V2EX
        ("V2EX 数据源", ["--source", "v2ex", "--limit", "5", "--format", "json"], 3),

        # 测试 10: 全网扫描（小规模）
        ("全网扫描", ["--source", "all", "--limit", "3", "--format", "json"], 5),
    ]

    results = []
    for name, args, expected in tests:
        try:
            success = run_test(name, args, expected)
            results.append((name, success))
        except Exception as e:
            print(f"[FAIL] 测试异常: {e}")
            results.append((name, False))

    # 汇总结果
    print("\n" + "="*60)
    print("[SUMMARY] Test Results")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {name}")

    print(f"\n[RESULT] {passed}/{total} passed")

    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
