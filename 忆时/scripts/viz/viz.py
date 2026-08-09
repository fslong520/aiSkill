#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""忆时 · 记忆可视化生成器

用法：
  python3 viz.py                       # 导出数据 → 生成 HTML → 打开
  python3 viz.py -o /path/out.html     # 指定输出路径
  python3 viz.py --no-open             # 生成但不打开
  python3 viz.py --data x.json         # 复用已有导出 JSON（跳过导出）

依赖：同目录 template.html；上一级 memory_core.py。
环境：须设 MEMO_DIR（忆时铁律），否则数据路径错。
"""
import json, os, re, subprocess, sys, argparse, tempfile
from pathlib import Path

VIZ_DIR = Path(__file__).resolve().parent
SKILL_DIR = VIZ_DIR.parent.parent          # scripts/viz → scripts → 忆时/
CORE = SKILL_DIR / "scripts" / "memory_core.py"
TPL = VIZ_DIR / "template.html"
# 与 memory_core.py 一致：默认 LOCAL_BASE/data（~/.local/share/opencode/忆时/data）
LOCAL_BASE = Path.home() / ".local" / "share" / "opencode" / "忆时"
DATA_DIR = os.environ.get("MEMO_DIR") or os.environ.get("YISHI_DATA_DIR") or str(LOCAL_BASE / "data")

# ---------- 主题聚类规则（顺序优先，首中即归） ----------
TOPICS = [
    ("纸焰小说", ["纸焰", "沈以南", "颜书瑶", "武戏", "爽点", "红痕", "晶核", "关雎", "老刘", "插图prompt"]),
    ("教学学生", ["备课", "课件", "袁雨", "郭瑾萱", "李铎怡", "李多翊", "张梓爱", "陈韵西", "杨柠瑞",
                  "赵柯豪", "课后反馈", "作业", "出题", "命题", "Scratch", "星火征途", "合卷", "重做闭环", "组卷", "错题"]),
    ("GESP考级", ["GESP", "考级", "真题", "大纲", "CSP", "STL", "等级考试"]),
    ("灵逸OJ", ["灵逸", "01oj", "lingyi-oj", "hustoj", "判题", "MMORPG", "域系统", "OJ", "judge", "Monaco", "Vditor", "RBAC"]),
    ("数学讲义", ["组合数学", "typst", "讲义", "加法原理", "乘法原理", "信竞数学", "竞赛编程", "排列组合", "Pólya", "排列", "组合"]),
    ("技能开发", ["技能", "搬题姬", "图片姬", "笔痕", "WebSketch", "ClawHub", "skill", "析题", "发布"]),
    ("系统运维", ["openKylin", "Manjaro", "内核", "音频", "wayland", "Wayland", "死机", "VLC", "微信", "ntfs",
                  "NTFS", "fstab", "GRUB", "KDE", "pkexec", "sudo", "挂载", "驱动", "dphome", "系统配置"]),
    ("工程配置", ["OpenClacky", "七决策", "opencode", "OpenCode", "模型", "DeepSeek", "SenseNova", "供应商", "config", "zen"]),
    ("忆时系统", ["忆时", "记忆梳理", "consolidat", "记忆"]),
]

def classify(kw):
    if not kw:
        return "其他"
    for name, words in TOPICS:
        for w in words:
            if w in kw:
                return name
    return "其他"

def summarize(content, limit=110):
    c = re.sub(r"\s+", " ", (content or "").strip())
    return c if len(c) <= limit else c[:limit] + "…"

def export_json(tmp):
    """调用 memory_core.py 导出全部记忆为 JSON"""
    env = dict(os.environ, MEMO_DIR=DATA_DIR)
    r = subprocess.run([sys.executable, str(CORE), "export", "--format", "json", "--output", str(tmp)],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"导出失败: {r.stderr.strip() or r.stdout.strip()}")

def build(data, out):
    memories = data.get("memories", [])
    records = []
    for m in memories:
        md = m.get("metadata", {})
        kw = md.get("keywords", "") or ""
        records.append({
            "id": m["id"],
            "type": md.get("type", "context"),
            "emotion": md.get("emotion", "medium"),
            "date": md.get("created_date", "") or (md.get("created_at", "") or "")[:10],
            "keywords": [k for k in kw.split(",") if k][:8],
            "kw_raw": kw,
            "freq": int(md.get("frequency", 1) or 1),
            "recall": int(md.get("recall_count", 0) or 0),
            "topic": classify(kw),
            "c": summarize(m.get("content", "")),
            "full": (m.get("content", "") or "").strip(),
        })
    records.sort(key=lambda r: r["date"], reverse=True)

    type_dist, emo_dist, topic_count, topic_kws = {}, {}, {}, {}
    for r in records:
        type_dist[r["type"]] = type_dist.get(r["type"], 0) + 1
        emo_dist[r["emotion"]] = emo_dist.get(r["emotion"], 0) + 1
        topic_count[r["topic"]] = topic_count.get(r["topic"], 0) + 1
        topic_kws.setdefault(r["topic"], set()).update(r["keywords"][:8])
    month_dist = {}
    for r in records:
        d = r["date"][:7]
        if d:
            month_dist[d] = month_dist.get(d, 0) + 1
    topic_samples = {}
    for t in topic_count:
        rs = sorted([r for r in records if r["topic"] == t],
                    key=lambda r: -(r["freq"] + (1 if r["emotion"] in ("high", "extreme") else 0)))
        topic_samples[t] = [{"c": r["c"], "type": r["type"], "e": r["emotion"], "d": r["date"]} for r in rs[:3]]

    payload = {
        "total": len(records),
        "export_date": data.get("export_date", ""),
        "type_dist": type_dist, "emo_dist": emo_dist,
        "month_dist": dict(sorted(month_dist.items())),
        "topic_count": topic_count,
        "topic_kws": {t: sorted(list(kws))[:14] for t, kws in topic_kws.items()},
        "topic_samples": topic_samples,
        "top_recs": [{"c": r["c"], "type": r["type"], "e": r["emotion"], "date": r["date"], "freq": r["recall"], "full": r["full"]}
                     for r in sorted(records, key=lambda r: -r["recall"])
                     if not (r["type"] == "time" and "记忆梳理" in r["kw_raw"])][:10],
        "records": records,
    }
    template = TPL.read_text(encoding="utf-8")
    if "/*__DATA__*/" not in template:
        raise RuntimeError("template.html 缺少数据占位符 /*__DATA__*/")
    html = template.replace("/*__DATA__*/", "const MEMORIES = " + json.dumps(payload, ensure_ascii=False))
    out.write_text(html, encoding="utf-8")
    return payload

def open_in_browser(path):
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    elif os.name == "nt":
        os.startfile(str(path))  # type: ignore[attr-defined]
    else:
        subprocess.Popen(["xdg-open", str(path)])

def main():
    ap = argparse.ArgumentParser(description="忆时记忆可视化")
    ap.add_argument("-o", "--output", default=str(Path.home() / "Desktop" / "忆时记忆全景.html"))
    ap.add_argument("--no-open", action="store_true", help="生成后不自动打开")
    ap.add_argument("--data", default=None, help="复用已有导出JSON文件")
    args = ap.parse_args()

    if args.data:
        data = json.load(open(args.data, encoding="utf-8"))
    else:
        tmp = Path(tempfile.gettempdir()) / "yishi_all.json"
        export_json(tmp)
        data = json.load(open(tmp, encoding="utf-8"))

    payload = build(data, Path(args.output))
    print(f"✅ 记忆全景已生成: {args.output}")
    print(f"   共 {payload['total']} 条记忆 · 主题 {len(payload['topic_count'])} 类")
    print(f"   " + " · ".join(f"{k} {v}" for k, v in sorted(payload["topic_count"].items(), key=lambda x: -x[1])))
    if not args.no_open:
        open_in_browser(Path(args.output))
        print("   已在浏览器打开")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 可视化失败: {e}", file=sys.stderr)
        sys.exit(1)
