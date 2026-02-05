#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Skills 简化版调度器
不依赖第三方库，使用 time.sleep 实现定时
"""
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 配置
SCRIPT_DIR = Path(__file__).parent
PYTHON = sys.executable

def fetch_news(task_name, sources, limit=15, keyword=None):
    """获取新闻的通用函数"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📰 {task_name}")

    cmd = [
        PYTHON,
        str(SCRIPT_DIR / "fetch_news.py"),
        "--source", sources,
        "--limit", str(limit),
        "--format", "markdown"
    ]

    if keyword:
        cmd.extend(["--keyword", keyword])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ {task_name} 完成")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ {task_name} 失败")
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 错误: {e}")
        return False

def run_immediate():
    """立即运行测试"""
    print("\n" + "="*60)
    print("📋 请选择要执行的任务：")
    print("="*60)
    print("  1. 科技早报 (HN, GitHub, 36Kr, Product Hunt, 腾讯)")
    print("  2. AI 专题 (HN, GitHub, Product Hunt)")
    print("  3. 全网扫描 (所有数据源)")
    print("  4. Hacker News 单独")
    print("  5. GitHub Trending 单独")
    print("  0. 返回")
    print()

    choice = input("请输入选项: ").strip()

    tasks = {
        "1": ("科技早报", "hackernews,github,36kr,producthunt,tencent", 15),
        "2": ("AI 专题", "hackernews,github,producthunt", 20, "AI"),
        "3": ("全网扫描", "all", 10),
        "4": ("Hacker News", "hackernews", 20),
        "5": ("GitHub Trending", "github", 15),
    }

    if choice in tasks:
        task_info = tasks[choice]
        if len(task_info) == 4:
            fetch_news(task_info[0], task_info[1], task_info[2], task_info[3])
        else:
            fetch_news(task_info[0], task_info[1], task_info[2])
    elif choice == "0":
        return
    else:
        print("❌ 无效选项")

def run_scheduled():
    """定时运行模式"""
    print("\n" + "="*60)
    print("⏰ 定时任务模式")
    print("="*60)
    print("\n已配置的定时任务：")
    print("  🌅 08:00 - 科技早报")
    print("  ☀️ 12:00 - AI 专题")
    print("  🌙 20:00 - 全网扫描")
    print("\n调度器运行中... (按 Ctrl+C 停止)")
    print("="*60 + "\n")

    last_tasks = {"morning": None, "noon": None, "evening": None}

    try:
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_date = now.strftime("%Y-%m-%d")

            # 早上 8 点
            if "08:00" <= current_time < "08:01":
                if last_tasks["morning"] != current_date:
                    fetch_news("🌅 科技早报", "hackernews,github,36kr,producthunt,tencent", 15)
                    last_tasks["morning"] = current_date

            # 中午 12 点
            elif "12:00" <= current_time < "12:01":
                if last_tasks["noon"] != current_date:
                    fetch_news("☀️ AI 专题", "hackernews,github,producthunt", 20, "AI")
                    last_tasks["noon"] = current_date

            # 晚上 8 点
            elif "20:00" <= current_time < "20:01":
                if last_tasks["evening"] != current_date:
                    fetch_news("🌙 全网扫描", "all", 10)
                    last_tasks["evening"] = current_date

            # 每分钟检查一次
            time.sleep(60)

    except KeyboardInterrupt:
        print("\n\n✅ 调度器已停止")

def main():
    """主函数"""
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("\n" + "="*60)
    print("📰 News Skills 调度器 v1.0")
    print("="*60)

    while True:
        print("\n请选择模式：")
        print("  1. ⏰ 定时运行模式")
        print("  2. ▶️  立即执行任务")
        print("  3. ❓ 帮助")
        print("  0. 🚪 退出")
        print()

        try:
            choice = input("请输入选项: ").strip()

            if choice == "1":
                run_scheduled()
            elif choice == "2":
                run_immediate()
            elif choice == "3":
                print("\n📖 使用帮助：")
                print("\n【定时运行模式】")
                print("  程序会在后台持续运行，在指定时间自动获取新闻")
                print("  - 08:00 科技早报")
                print("  - 12:00 AI 专题")
                print("  - 20:00 全网扫描")
                print("\n【立即执行】")
                print("  选择一个任务立即执行，用于测试或临时获取")
                print("\n【提示】")
                print("  - 建议将此程序添加到系统启动项")
                print("  - 确保电脑不会进入休眠模式")
                print("  - 报告保存在 reports/ 目录下")
            elif choice == "0":
                print("\n👋 再见！")
                break
            else:
                print("\n❌ 无效选项，请重新输入")

        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")

if __name__ == "__main__":
    main()
