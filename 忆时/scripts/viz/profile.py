#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""忆时 · 人物画像助手

两步用法：
  ① 取素材（AI 消费）：
     python3 profile.py
     → 输出画像素材报告：分布统计 / 高频检索 / extreme 条目 / 活跃日 / 事件候选

  ② 生成页面（注入画像正文）：
     python3 profile.py --content 画像正文.md --out /path/out.html [--open]
     → 正文（markdown/HTML 片段）注入模板数据区，生成孟菲斯风单页
     → 生成后自动封存时间胶囊（3个月后解锁），--no-capsule 可关

依赖：同目录 viz.py（复用导出与主题聚类）；profile_template.html。
环境：须设 MEMO_DIR。
"""
import json, os, re, sys, subprocess, argparse, calendar, datetime
from pathlib import Path

VIZ_DIR = Path(__file__).resolve().parent
SKILL_DIR = VIZ_DIR.parent.parent
sys.path.insert(0, str(VIZ_DIR))
import viz  # 复用 export_json / classify / summarize / build

TPL = VIZ_DIR / "profile_template.html"

def load_data():
    import tempfile
    tmp = Path(tempfile.gettempdir()) / "yishi_all.json"
    viz.export_json(tmp)
    return json.load(open(tmp, encoding="utf-8"))

def make_records(data):
    memories = data.get("memories", [])
    records = []
    for m in memories:
        md = m.get("metadata", {})
        kw = md.get("keywords", "") or ""
        records.append({
            "id": m["id"], "type": md.get("type", "context"),
            "emotion": viz._norm_emo(md.get("emotion")),
            "date": md.get("created_date", "") or (md.get("created_at", "") or "")[:10],
            "keywords": [k for k in kw.split(",") if k][:8],
            "kw_raw": kw,
            "freq": int(md.get("frequency", 1) or 1),
            "recall": int(md.get("recall_count", 0) or 0),
            "topic": viz.classify(kw),
            "c": viz.summarize(m.get("content", ""), 100),
        })
    return records

def report(records):
    from collections import Counter
    lines = []
    lines.append("=" * 48)
    lines.append("忆时 · 画像素材报告")
    lines.append("=" * 48)
    lines.append(f"总记忆: {len(records)} 条 | 跨度: {min(r['date'] for r in records if r['date'])} → {max(r['date'] for r in records if r['date'])}")
    td = Counter(r["type"] for r in records)
    ed = Counter("≥0.7" if r["emotion"] >= 0.7 else ("0.4~0.7" if r["emotion"] >= 0.4 else "<0.4") for r in records)
    tp = Counter(r["topic"] for r in records)
    lines.append(f"\n【类型分布】 " + " · ".join(f"{k} {v}" for k, v in td.most_common()))
    lines.append(f"【情绪分布】 " + " · ".join(f"{k} {v}" for k, v in ed.most_common()))
    lines.append(f"【主题分布】 " + " · ".join(f"{k} {v}" for k, v in tp.most_common()))
    lines.append("\n【高频检索 Top10】")
    for r in sorted(records, key=lambda r: -r["recall"])[:10]:
        lines.append(f"  [{r['recall']}次] {r['date']} {r['type']}: {r['c']}")
    ext = [r for r in records if r["emotion"] >= 0.9]
    lines.append(f"\n【高情绪(≥0.9) {len(ext)} 条——最在意之事】")
    for r in ext:
        lines.append(f"  · {r['date']}: {r['c']}")
    days = Counter(r["date"] for r in records if r["date"])
    lines.append("\n【最活跃日期 Top6】")
    for d, c in days.most_common(6):
        lines.append(f"  {d}: {c} 条")
    lines.append("\n【事件候选——每日取高情绪/高频之条目，供画像时间线】")
    by_day = {}
    for r in records:
        if r["date"]:
            by_day.setdefault(r["date"], []).append(r)
    for d in sorted(by_day)[::1]:
        rs = sorted(by_day[d], key=lambda r: -(r["recall"] + (1 if r["emotion"] >= 0.7 else 0)))[:1]
        for r in rs:
            lines.append(f"  {d} [{r['topic']}] {r['c']}")
    return "\n".join(lines)

def chart_html(records):
    from collections import Counter
    td = Counter(r["type"] for r in records)
    ed = Counter("≥0.7" if r["emotion"] >= 0.7 else ("0.4~0.7" if r["emotion"] >= 0.4 else "<0.4") for r in records)
    tmax = max(td.values()) if td else 1
    emax = max(ed.values()) if ed else 1
    cols = {"≥0.7": "#dc2626", "0.4~0.7": "#ea580c", "<0.4": "#16a34a"}
    h = ['<div class="panel"><h3>记忆类型分布</h3><div>']
    for k, v in td.most_common():
        h.append(f'<div class="bar-row"><span class="k">{k}</span><div class="bar"><i style="width:{v/tmax*100:.0f}%"></i></div><span class="n">{v}</span></div>')
    h.append('</div></div><div class="panel"><h3>情绪分布</h3><div>')
    for k, v in ed.most_common():
        h.append(f'<div class="bar-row"><span class="k">{k}</span><div class="bar"><i style="width:{v/emax*100:.0f}%;background:{cols.get(k, "#ec5b13")}"></i></div><span class="n">{v}</span></div>')
    h.append("</div></div>")
    return "".join(h)

def add_months(dt, months):
    """日期加 N 个月（处理跨年与月末截断）"""
    m = dt.month - 1 + months
    y = dt.year + m // 12
    m = m % 12 + 1
    d = min(dt.day, calendar.monthrange(y, m)[1])
    return dt.replace(year=y, month=m, day=d)

def capsule_lock(content, unlock_date, summary="人物画像", keywords="画像,人物画像"):
    """调用 memory_core 封存时间胶囊"""
    r = subprocess.run(
        [sys.executable, str(viz.CORE), "capsule", "lock",
         "--unlock-at", unlock_date, "--content", content,
         "--summary", summary, "--keywords", keywords],
        capture_output=True, text=True,
        env=dict(os.environ, MEMO_DIR=viz.DATA_DIR))
    if r.returncode != 0:
        raise RuntimeError(f"胶囊封存失败: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout

def main():
    ap = argparse.ArgumentParser(description="忆时人物画像助手")
    ap.add_argument("--content", default=None, help="画像正文文件（markdown/HTML 片段），注入模板")
    ap.add_argument("-o", "--out", default=str(Path.home() / "Desktop" / "哥哥人物画像.html"))
    ap.add_argument("--open", action="store_true", help="生成后打开浏览器")
    ap.add_argument("--no-capsule", action="store_true", help="生成后不封存时间胶囊（默认封存，3个月后解锁）")
    ap.add_argument("--data", default=None, help="复用已有导出 JSON")
    args = ap.parse_args()

    data = json.load(open(args.data, encoding="utf-8")) if args.data else load_data()
    records = make_records(data)

    if not args.content:
        print(report(records))
        print("\n用法：将画像正文写入文件后，运行 profile.py --content 正文.md --out 输出.html --open")
        return

    content = Path(args.content).read_text(encoding="utf-8").strip()
    template = TPL.read_text(encoding="utf-8")
    if "<!--CONTENT-->" not in template:
        raise RuntimeError("profile_template.html 缺占位符 <!--CONTENT-->")
    total = len(records)
    span = f"{min(r['date'] for r in records if r['date'])} → {max(r['date'] for r in records if r['date'])}"
    html = (template
            .replace("<!--CONTENT-->", content)
            .replace("<!--DATA-->", chart_html(records))
            .replace("<!--TOTAL-->", str(total))
            .replace("<!--SPAN-->", span))
    Path(args.out).write_text(html, encoding="utf-8")
    print(f"✅ 画像页已生成: {args.out}（{total} 条记忆 · {span}）")
    if args.open:
        viz.open_in_browser(Path(args.out))
        print("   已在浏览器打开")

    # 自动封存时间胶囊：3个月后解锁
    if not args.no_capsule:
        now = datetime.date.today()
        unlock_date = add_months(now, 3).isoformat()
        plain = re.sub(r"<[^>]+>", " ", content)
        plain = re.sub(r"\s+", " ", plain).strip()
        capsule_text = (f"人物画像 - 生成于 {now.isoformat()}\n"
                        f"文件: {args.out}\n"
                        f"画像摘要: {plain[:280]}")
        out = capsule_lock(capsule_text, unlock_date)
        print("🔒 画像已封存为时间胶囊，解锁日:", unlock_date)
        print("   " + " | ".join(l.strip() for l in out.splitlines() if l.strip()))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 画像失败: {e}", file=sys.stderr)
        sys.exit(1)
