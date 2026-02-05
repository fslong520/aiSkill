#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Skills 定时调度器
支持每天定时推送新闻到指定位置
"""
import schedule
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 配置
SCRIPT_DIR = Path(__file__).parent
PYTHON = sys.executable
REPORTS_DIR = SCRIPT_DIR / "reports"

def fetch_daily_news():
    """获取每日科技新闻"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始获取每日科技早报...")

    cmd = [
        PYTHON,
        str(SCRIPT_DIR / "fetch_news.py"),
        "--source", "hackernews,github,36kr,producthunt,tencent",
        "--limit", "15",
        "--format", "markdown"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 科技早报获取成功")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 获取失败")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 错误: {e}")
        return False

def fetch_ai_news():
    """获取 AI 专题新闻"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始获取 AI 专题新闻...")

    cmd = [
        PYTHON,
        str(SCRIPT_DIR / "fetch_news.py"),
        "--source", "hackernews,github,producthunt",
        "--keyword", "AI",
        "--limit", "20",
        "--format", "markdown"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ AI 专题获取成功")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 获取失败")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 错误: {e}")
        return False

def fetch_global_scan():
    """全网扫描"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始全网扫描...")

    cmd = [
        PYTHON,
        str(SCRIPT_DIR / "fetch_news.py"),
        "--source", "all",
        "--limit", "10",
        "--format", "markdown"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 全网扫描完成")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 扫描失败")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 错误: {e}")
        return False

def show_menu():
    """显示菜单"""
    print("\n" + "="*60)
    print("News Skills 定时调度器")
    print("="*60)
    print("\n请选择模式：")
    print("  1. 自动运行（按计划执行）")
    print("  2. 立即测试 - 科技早报")
    print("  3. 立即测试 - AI 专题")
    print("  4. 立即测试 - 全网扫描")
    print("  5. 退出")
    print("\n")

def main():
    """主函数"""
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    show_menu()

    while True:
        try:
            choice = input("请输入选项 (1-5): ").strip()

            if choice == "1":
                # 自动运行模式
                print("\n已设置的定时任务：")
                print("  - 每天 08:00: 科技早报")
                print("  - 每天 12:00: AI 专题")
                print("  - 每天 20:00: 全网扫描")
                print("\n调度器运行中... (按 Ctrl+C 停止)")
                print("="*60 + "\n")

                # 设置定时任务
                schedule.clear()
                schedule.every().day.at("08:00").do(fetch_daily_news)
                schedule.every().day.at("12:00").do(fetch_ai_news)
                schedule.every().day.at("20:00").do(fetch_global_scan)

                try:
                    while True:
                        schedule.run_pending()
                        time.sleep(60)
                except KeyboardInterrupt:
                    print("\n\n调度器已停止")
                    show_menu()

            elif choice == "2":
                print("\n正在测试：科技早报")
                fetch_daily_news()
                print("\n测试完成！")
                show_menu()

            elif choice == "3":
                print("\n正在测试：AI 专题")
                fetch_ai_news()
                print("\n测试完成！")
                show_menu()

            elif choice == "4":
                print("\n正在测试：全网扫描")
                fetch_global_scan()
                print("\n测试完成！")
                show_menu()

            elif choice == "5":
                print("\n再见！")
                break

            else:
                print("\n❌ 无效选项，请重新输入")

        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            show_menu()

if __name__ == "__main__":
    main()
