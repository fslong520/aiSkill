"""
忆时 Memory Core - 记忆胶囊系统核心引擎

功能:
  - 记忆向量化存储 (ChromaDB)
  - 类人检索 (语义 + 近因 + 情绪 + 频率 + 联想)
  - 时间胶囊管理
  - 批量导入导出
  - 关系图谱维护

用法示例:
  python3 memory_core.py init
  python3 memory_core.py store "今天学会了Python装饰器" --type task --emotion high
  python3 memory_core.py recall "Python学习" --limit 5 --expand
  python3 memory_core.py capsule lock --unlock-at "2026-01-01" --summary "年度记忆"
  python3 memory_core.py capsule list
  python3 memory_core.py import-file memories.md --format markdown
  python3 memory_core.py export --format timeline --output "2026回顾.md"
  python3 memory_core.py stats
"""

import argparse
import json
import math
import os
import sys
import uuid
import warnings
import contextlib
from datetime import datetime, timedelta
from pathlib import Path

# 静默 ONNX C++ 层 Schema error 滋扰
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

@contextlib.contextmanager
def _silent_import():
    """OS 级重定向 stderr，连 C++ std::cerr 一并静默"""
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_fd2 = os.dup(2)          # 备份原 stderr
    os.dup2(devnull, 2)          # fd 2 → /dev/null
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_fd2, 2)      # 恢复原 stderr
        os.close(old_fd2)

with _silent_import():
    import chromadb

# 模型和数据统一存到 ~/.local/share/opencode/忆时/ 下，
# 不放在技能目录（更新技能会覆盖），也不放在 ~/.cache/（清缓存会被删除）。
LOCAL_BASE = os.path.join(Path.home(), ".local", "share", "opencode", "忆时")

DATA_DIR = os.environ.get(
    "YISHI_DATA_DIR",
    os.path.join(LOCAL_BASE, "data"),
)

SKILL_MODEL_BASE = os.path.join(LOCAL_BASE, "models")

# Chroma ONNXMiniLM_L6_V2 的 DOWNLOAD_PATH 即模型根目录：
#   {DOWNLOAD_PATH}/onnx/model.onnx
CHROMA_MODEL_DIR = os.path.join(SKILL_MODEL_BASE, "onnx")
CHROMA_MODEL_ONNX = os.path.join(CHROMA_MODEL_DIR, "model.onnx")

# 自动备份文件（JSONL 格式），存于 LOCAL_BASE 而非 data/ 中，
# 即使 data/ 被误删也能用 recover 命令重建记忆库。
BACKUP_FILE = os.path.join(LOCAL_BASE, "memories_backup.jsonl")

EMOTION_WEIGHTS = {"extreme": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2}
RECALL_DECAY_DAYS = 30.0
VALID_TYPES = {"emotion", "decision", "task", "time", "preference", "context"}
VALID_EMOTIONS = {"extreme", "high", "medium", "low"}
_embedding_client = None
_embedding_fn = None


def _skill_models_dir():
    """返回技能目录下的 models/ 路径（即 SKILL.md 所在目录之 models/ 子目录）。"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")


def _install_model():
    """确保 embedding 模型位于 skill-local models/ 目录，而非 ~/.cache/chroma/."""
    if os.path.exists(CHROMA_MODEL_ONNX):
        return True

    import shutil

    # 检查旧版路径（models/onnx/ 结构），若有则迁移
    old_onnx_dir = os.path.join(SKILL_MODEL_BASE, "onnx")
    old_model = os.path.join(old_onnx_dir, "model.onnx")
    if os.path.exists(old_model):
        os.makedirs(CHROMA_MODEL_DIR, exist_ok=True)
        for f in os.listdir(old_onnx_dir):
            shutil.copy2(os.path.join(old_onnx_dir, f), os.path.join(CHROMA_MODEL_DIR, f))
        if os.path.exists(CHROMA_MODEL_ONNX):
            return True

    # 检查技能自身 models/onnx/（完整解压目录）
    skill_onnx = os.path.join(_skill_models_dir(), "onnx")
    if os.path.isdir(skill_onnx) and os.path.exists(os.path.join(skill_onnx, "model.onnx")):
        os.makedirs(CHROMA_MODEL_DIR, exist_ok=True)
        for f in os.listdir(skill_onnx):
            shutil.copy2(os.path.join(skill_onnx, f), os.path.join(CHROMA_MODEL_DIR, f))
        if os.path.exists(CHROMA_MODEL_ONNX):
            return True

    # 尝试从本地 onnx.tar.gz 安装（优先技能目录，其次 LOCAL_BASE）
    skill_tar = os.path.join(_skill_models_dir(), "onnx.tar.gz")
    local_tar = os.path.join(SKILL_MODEL_BASE, "onnx.tar.gz")
    onnx_tar = skill_tar if os.path.exists(skill_tar) else local_tar
    if os.path.exists(onnx_tar):
        import tarfile, tempfile
        os.makedirs(CHROMA_MODEL_DIR, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            with tarfile.open(onnx_tar, "r:gz") as tar:
                tar.extractall(path=tmp, filter="data")
            # tarball 结构可能是 onnx/xxx 或直接是文件
            src = os.path.join(tmp, "onnx")
            if os.path.isdir(src):
                for f in os.listdir(src):
                    shutil.move(os.path.join(src, f), CHROMA_MODEL_DIR)
            else:
                for f in os.listdir(tmp):
                    fp = os.path.join(tmp, f)
                    if os.path.isfile(fp):
                        shutil.move(fp, CHROMA_MODEL_DIR)
        return os.path.exists(CHROMA_MODEL_ONNX)

    return False


def get_embedding_fn():
    global _embedding_fn
    if _embedding_fn is None:
        from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2
        _install_model()
        _embedding_fn = ONNXMiniLM_L6_V2()
        # ★ 关键：永远指向 skill-local，远离 ~/.cache/chroma/ ★
        _embedding_fn.DOWNLOAD_PATH = SKILL_MODEL_BASE
    return _embedding_fn


def get_client():
    global _embedding_client
    if _embedding_client is None:
        os.makedirs(DATA_DIR, exist_ok=True)
        _embedding_client = chromadb.PersistentClient(path=DATA_DIR)
    return _embedding_client


def get_collection(client, name):
    ef = get_embedding_fn()
    if ef:
        return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"}, embedding_function=ef)
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def _update_meta_total(client, field, delta):
    try:
        meta = get_collection(client, "meta")
        if meta.count() == 0:
            return
        s = json.loads(meta.get(ids=["state"])["documents"][0])
        s[field] = s.get(field, 0) + delta
        meta.update(documents=[json.dumps(s)], ids=["state"], metadatas=[{"key": "state"}])
    except Exception:
        pass


def _now():
    return datetime.now()


# ========== 自动备份 ==========
def _append_backup(mem_id, content, metadata):
    """每次存储记忆时追加一条 JSONL 到备份文件，与 data/ 独立存放。"""
    try:
        record = {"id": mem_id, "content": content, "metadata": metadata, "backup_at": _now().isoformat()}
        line = json.dumps(record, ensure_ascii=False)
        with open(BACKUP_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"  ⚠️ 备份写入失败: {e}", file=sys.stderr)


def _load_backups():
    """读取全部备份记录，返回列表。"""
    if not os.path.exists(BACKUP_FILE):
        return []
    records = []
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


# ========== init ==========
def cmd_init(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    rel_col = get_collection(client, "relationships")
    meta_col = get_collection(client, "meta")

    if meta_col.count() == 0:
        state = {
            "version": "1.0.0",
            "created_at": _now().isoformat(),
            "total_memories": 0,
            "total_capsules": 0,
            "total_relationships": 0,
        }
        meta_col.add(documents=[json.dumps(state)], metadatas=[{"key": "state"}], ids=["state"])

    print(f"忆时记忆系统初始化完成")
    print(f"  存储路径: {DATA_DIR}")
    print(f"  记忆集合: {mem_col.count()} 条")
    print(f"  关系集合: {rel_col.count()} 条")
    print(f"  ChromaDB: {chromadb.__version__}")


# ========== store ==========
def cmd_store(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    now = _now()
    emotion = args.emotion or "medium"
    mem_type = args.type or "context"

    metadata = {
        "type": mem_type,
        "emotion": emotion,
        "emotion_weight": EMOTION_WEIGHTS.get(emotion, 0.5),
        "created_at": now.isoformat(),
        "created_date": now.strftime("%Y-%m-%d"),
        "updated_at": now.isoformat(),
        "keywords": args.keywords or "",
        "source": args.source or "manual",
        "source_session": args.session or "",
        "frequency": 1,
        "recall_count": 0,
    }

    mem_id = str(uuid.uuid4())
    mem_col.add(documents=[args.content], metadatas=[metadata], ids=[mem_id])
    _update_meta_total(client, "total_memories", 1)

    # 自动备份到 JSONL（与 data/ 独立，不怕误删）
    _append_backup(mem_id, args.content, metadata)

    # 自动建语义关联：找相似记忆，写入 relationships 集合
    try:
        rel_col = get_collection(client, "relationships")
        similar = mem_col.query(query_texts=[args.content], n_results=6)
        if similar["ids"] and similar["ids"][0]:
            merged_kw = set(k.strip() for k in (metadata.get("keywords", "").split(",")) if k.strip())
            for j in range(len(similar["ids"][0])):
                sid = similar["ids"][0][j]
                if sid == mem_id:
                    continue
                sdist = similar["distances"][0][j] if similar["distances"] else 1.0
                ssem = 1.0 - sdist
                if ssem > 0.50:
                    rel_col.add(
                        documents=[f"{mem_id}->{sid}"],
                        metadatas=[{"source": mem_id, "target": sid, "score": round(ssem, 3)}],
                        ids=[str(uuid.uuid4())],
                    )
                    # 跨记忆融合关键词，增强检索覆盖
                    try:
                        tgt = mem_col.get(ids=[sid])
                        if tgt["metadatas"]:
                            tk = tgt["metadatas"][0].get("keywords", "")
                            for kw in tk.split(","):
                                kw = kw.strip()
                                if kw:
                                    merged_kw.add(kw)
                    except Exception:
                        pass
            if merged_kw:
                new_kw = ",".join(sorted(merged_kw))
                metadata["keywords"] = new_kw
                mem_col.update(ids=[mem_id], metadatas=[metadata])
            _update_meta_total(client, "total_relationships", 1)
    except Exception:
        pass

    print(f"记忆已存储")
    print(f"  ID: {mem_id}")
    print(f"  类型: {mem_type}  情绪: {emotion}")
    if metadata["keywords"]:
        print(f"  关键字: {metadata['keywords']}")
    print(f"  已自动备份到: {BACKUP_FILE}")
    return mem_id


# ========== recall ==========
def cmd_recall(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    rel_col = get_collection(client, "relationships")
    query = args.query
    limit = args.limit or 10
    min_weight = args.min_weight or 0.0
    type_filter = args.type_filter or None
    now = _now()

    results = mem_col.query(query_texts=[query], n_results=limit * 3)
    if not results["ids"] or not results["ids"][0]:
        print("没有找到相关记忆")
        return

    scored = []
    seen = set()

    for i in range(len(results["ids"][0])):
        mid = results["ids"][0][i]
        if mid in seen:
            continue
        seen.add(mid)

        meta = results["metadatas"][0][i] if results["metadatas"] else {}
        doc = results["documents"][0][i] if results["documents"] else ""
        dist = results["distances"][0][i] if results["distances"] else 0.0
        semantic = 1.0 - dist
        em_w = float(meta.get("emotion_weight", 0.5))
        recall_count = int(meta.get("recall_count", 0))
        freq = int(meta.get("frequency", 1))
        freq_boost = min(math.log2(freq + 1) * 0.1, 0.2) + min(math.log2(recall_count + 1) * 0.05, 0.15)
        created = datetime.fromisoformat(meta.get("created_at", now.isoformat()))
        days_ago = (now - created).total_seconds() / 86400.0
        recency = math.exp(-math.log(2) * days_ago / RECALL_DECAY_DAYS)

        score = 0.40 * semantic + 0.15 * em_w + 0.20 * recency + 0.25 * (0.6 + freq_boost)
        if score < min_weight:
            continue
        if type_filter and meta.get("type") != type_filter:
            continue

        scored.append({
            "id": mid, "content": doc, "score": round(score, 3),
            "semantic": round(semantic, 3), "emotion": meta.get("emotion", "medium"),
            "emotion_weight": em_w, "type": meta.get("type", "context"),
            "created_at": meta.get("created_at", ""), "created_date": meta.get("created_date", ""),
            "keywords": meta.get("keywords", ""),
            "is_capsule": meta.get("is_capsule", "false") == "true",
            "capsule_unlock_at": meta.get("capsule_unlock_at", ""),
            "frequency": freq, "recall_count": recall_count, "is_expanded": False,
        })

    # === 联想扩散（两阶段），统一用真实语义值计分 ===
    def _compute_score(semantic, em_w, freq, recall_count, created):
        freq_boost = min(math.log2(freq + 1) * 0.1, 0.2) + min(math.log2(recall_count + 1) * 0.05, 0.15)
        days_ago = (now - created).total_seconds() / 86400.0
        recency = math.exp(-math.log(2) * days_ago / RECALL_DECAY_DAYS)
        return 0.40 * semantic + 0.15 * em_w + 0.20 * recency + 0.25 * (0.6 + freq_boost)

    if args.expand and scored:
        expanded = set(s["id"] for s in scored)

        # 阶段一：关系链扩散（relationships 集合，按 metadata 精确查找）
        top_ids = [s["id"] for s in scored[:3]]
        for sid in top_ids:
            try:
                for rel in [rel_col.get(where={"source": sid}), rel_col.get(where={"target": sid})]:
                    if not rel["ids"]:
                        continue
                    for j in range(len(rel["ids"])):
                        rm = rel["metadatas"][j] if rel["metadatas"] else {}
                        partner = rm.get("target") if rm.get("source") == sid else rm.get("source")
                        if not partner or partner in expanded:
                            continue
                        expanded.add(partner)
                        pdoc = mem_col.get(ids=[partner])
                        if pdoc["documents"]:
                            pm = pdoc["metadatas"][0] if pdoc["metadatas"] else {}
                            rsem = float(rm.get("score", 0.40)) * 0.7
                            rew = float(pm.get("emotion_weight", 0.5))
                            rf = int(pm.get("frequency", 1))
                            rr = int(pm.get("recall_count", 0))
                            rc = datetime.fromisoformat(pm.get("created_at", now.isoformat()))
                            scored.append({
                                "id": partner, "content": pdoc["documents"][0],
                                "score": round(_compute_score(rsem, rew, rf, rr, rc), 3),
                                "semantic": round(rsem, 3),
                                "emotion": pm.get("emotion", "medium"),
                                "emotion_weight": rew,
                                "type": pm.get("type", "context"),
                                "created_at": pm.get("created_at", ""),
                                "created_date": pm.get("created_date", ""),
                                "keywords": pm.get("keywords", ""),
                                "is_capsule": pm.get("is_capsule", "false") == "true",
                                "capsule_unlock_at": pm.get("capsule_unlock_at", ""),
                                "frequency": rf,
                                "recall_count": rr,
                                "is_expanded": True,
                            })
            except Exception:
                pass

        # 阶段二：语义二次检索——取 top-2 结果之内容/关键字作新查询
        extra_queries = []
        for s in scored[:2]:
            if s.get("keywords"):
                extra_queries.append(s["keywords"])
            extra_queries.append(s["content"][:150])
        for eq in extra_queries:
            if not eq.strip():
                continue
            try:
                extra = mem_col.query(query_texts=[eq], n_results=4)
                if extra["ids"] and extra["ids"][0]:
                    for j in range(len(extra["ids"][0])):
                        eid = extra["ids"][0][j]
                        if eid in expanded:
                            continue
                        expanded.add(eid)
                        em = extra["metadatas"][0][j] if extra["metadatas"] else {}
                        edist = extra["distances"][0][j] if extra["distances"] else 1.0
                        esem = (1.0 - edist) * 0.7
                        eew = float(em.get("emotion_weight", 0.5))
                        ef = int(em.get("frequency", 1))
                        er = int(em.get("recall_count", 0))
                        ec = datetime.fromisoformat(em.get("created_at", now.isoformat()))
                        scored.append({
                            "id": eid,
                            "content": extra["documents"][0][j] if extra["documents"] else "",
                            "score": round(_compute_score(esem, eew, ef, er, ec), 3),
                            "semantic": round(esem, 3),
                            "emotion": em.get("emotion", "medium"),
                            "emotion_weight": eew,
                            "type": em.get("type", "context"),
                            "created_at": em.get("created_at", ""),
                            "created_date": em.get("created_date", ""),
                            "keywords": em.get("keywords", ""),
                            "is_capsule": em.get("is_capsule", "false") == "true",
                            "capsule_unlock_at": em.get("capsule_unlock_at", ""),
                            "frequency": ef,
                            "recall_count": er,
                            "is_expanded": True,
                        })
            except Exception:
                pass

    scored.sort(key=lambda x: x["score"], reverse=True)
    scored = scored[:limit]

    for item in scored:
        try:
            old = mem_col.get(ids=[item["id"]])
            if old["metadatas"]:
                m = old["metadatas"][0]
                m["recall_count"] = int(m.get("recall_count", 0)) + 1
                m["updated_at"] = now.isoformat()
                mem_col.update(ids=[item["id"]], metadatas=[m])
        except Exception:
            pass

    emoji_map = {"extreme": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
    print(f"检索到 {len(scored)} 条相关记忆 (查询: '{query}')\n")
    print("=" * 60)
    for idx, item in enumerate(scored, 1):
        e_emoji = emoji_map.get(item["emotion"], "⚪")
        capsule_tag = " [CAPSULE]" if item["is_capsule"] else ""
        assoc_tag = " [关联]" if item.get("is_expanded") else ""
        print(f"\n#{idx} {e_emoji} [{item['type'].upper()}]{capsule_tag}{assoc_tag}")
        print(f"   得分: {item['score']} | 语义: {item['semantic']} | 情绪: {item['emotion']}")
        print(f"   日期: {item['created_date']} | 被检索: {item['recall_count']}次")
        if item["keywords"]:
            print(f"   关键字: {item['keywords']}")
        print(f"   内容: {item['content']}")
    print(f"\n{'='*60}")


# ========== update ==========
def cmd_update(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    if not args.id:
        print("错误: 请提供记忆 ID (--id)"); sys.exit(1)
    try:
        old = mem_col.get(ids=[args.id])
    except Exception:
        print(f"错误: 未找到记忆 {args.id}"); sys.exit(1)
    if not old["ids"]:
        print(f"错误: 未找到记忆 {args.id}"); sys.exit(1)
    meta = old["metadatas"][0].copy() if old["metadatas"] else {}
    meta["updated_at"] = _now().isoformat()
    content = args.content if args.content is not None else old["documents"][0]
    if args.keywords is not None: meta["keywords"] = args.keywords
    if args.emotion is not None:
        meta["emotion"] = args.emotion
        meta["emotion_weight"] = EMOTION_WEIGHTS.get(args.emotion, 0.5)
    if args.type is not None: meta["type"] = args.type
    mem_col.update(ids=[args.id], documents=[content], metadatas=[meta])
    print(f"记忆已更新: {args.id}")


# ========== delete ==========
def cmd_delete(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    if not args.id:
        print("错误: 请提供记忆 ID (--id)"); sys.exit(1)
    try:
        old = mem_col.get(ids=[args.id])
    except Exception:
        print(f"错误: 未找到记忆 {args.id}"); sys.exit(1)
    if not old["ids"]:
        print(f"错误: 未找到记忆 {args.id}"); sys.exit(1)
    mem_col.delete(ids=[args.id])
    _update_meta_total(client, "total_memories", -1)
    print(f"记忆已删除: {args.id}")


# ========== stats ==========
def cmd_stats(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    rel_col = get_collection(client, "relationships")
    total = mem_col.count()
    print(f"忆时 · 记忆统计")
    print(f"{'='*40}")
    print(f"  总记忆数: {total}")
    print(f"  关系数量: {rel_col.count()}")
    if total == 0: return
    type_counts = {}; emotion_counts = {}; capsule_count = 0
    result = mem_col.get()
    if result["metadatas"]:
        for m in result["metadatas"]:
            t = m.get("type", "context"); type_counts[t] = type_counts.get(t, 0) + 1
            e = m.get("emotion", "medium"); emotion_counts[e] = emotion_counts.get(e, 0) + 1
            if m.get("is_capsule") == "true": capsule_count += 1
    print(f"\n  按类型:")
    for t, c in sorted(type_counts.items()): print(f"    {t}: {c}")
    print(f"\n  按情绪:")
    for e, c in sorted(emotion_counts.items()): print(f"    {e}: {c}")
    print(f"\n  时间胶囊: {capsule_count}")


# ========== capsule ==========
def cmd_capsule(args):
    action = args.capsule_action
    client = get_client()
    mem_col = get_collection(client, "memories")

    if action == "lock":
        now = _now()
        unlock_at = args.unlock_at or (now + timedelta(days=30)).strftime("%Y-%m-%d")
        metadata = {
            "type": "context", "emotion": "medium",
            "created_at": now.isoformat(), "created_date": now.strftime("%Y-%m-%d"),
            "updated_at": now.isoformat(), "keywords": args.keywords or "",
            "frequency": 1, "recall_count": 0,
            "is_capsule": "true", "capsule_unlock_at": unlock_at,
        }
        cid = str(uuid.uuid4())
        content = args.content or f"时间胶囊 - 创建于 {now.strftime('%Y-%m-%d')}, 解锁日期: {unlock_at}"
        mem_col.add(documents=[content], metadatas=[metadata], ids=[cid])
        _update_meta_total(client, "total_capsules", 1)
        print(f"时间胶囊已封存")
        print(f"  ID: {cid}")
        print(f"  创建日期: {now.strftime('%Y-%m-%d')}")
        print(f"  解锁日期: {unlock_at}")
        if args.summary: print(f"  摘要: {args.summary}")

    elif action == "unseal":
        if not args.capsule_id:
            print("错误: 请提供胶囊 ID (--capsule-id)"); sys.exit(1)
        try:
            old = mem_col.get(ids=[args.capsule_id])
        except Exception:
            print(f"错误: 未找到胶囊 {args.capsule_id}"); sys.exit(1)
        if not old["ids"]:
            print(f"错误: 未找到胶囊 {args.capsule_id}"); sys.exit(1)
        meta = old["metadatas"][0]
        if meta.get("is_capsule") != "true":
            print("错误: 该记忆不是时间胶囊"); sys.exit(1)
        unlock_at = datetime.fromisoformat(meta["capsule_unlock_at"])
        now = _now()
        if now < unlock_at:
            resp = input(f"警告: 胶囊尚未到期 (解锁: {unlock_at.strftime('%Y-%m-%d')}), 继续? [yes]: ").strip().lower()
            if resp != "yes": print("已取消"); return
        meta["is_capsule"] = "false"
        meta["updated_at"] = now.isoformat()
        mem_col.update(ids=[args.capsule_id], metadatas=[meta])
        print(f"时间胶囊已解封!")
        print(f"  内容: {old['documents'][0]}")
        print(f"  封存: {meta.get('created_date', '')} -> 解锁: {unlock_at.strftime('%Y-%m-%d')}")

    elif action == "list":
        result = mem_col.get()
        capsules = []
        if result["metadatas"]:
            for i, m in enumerate(result["metadatas"]):
                if m.get("is_capsule") == "true":
                    capsules.append({
                        "id": result["ids"][i], "created": m.get("created_date", ""),
                        "unlock_at": m.get("capsule_unlock_at", ""),
                        "content": result["documents"][i] if result["documents"] else "",
                        "keywords": m.get("keywords", ""),
                    })
        if not capsules:
            print("没有封存的时间胶囊"); return
        print(f"时间胶囊 ({len(capsules)} 个)\n{'='*60}")
        now = _now()
        for c in capsules:
            unlock = datetime.fromisoformat(c["unlock_at"])
            status = "已到期" if now >= unlock else f"剩余 {(unlock - now).days} 天"
            print(f"  ID: {c['id']}")
            print(f"  创建: {c['created']} | 解锁: {c['unlock_at']} | 状态: {status}")
            print(f"  内容: {c['content']}")
            if c["keywords"]: print(f"  关键字: {c['keywords']}")
            print()

    elif action == "check-expired":
        result = mem_col.get()
        expired = []; now = _now()
        if result["metadatas"]:
            for i, m in enumerate(result["metadatas"]):
                if m.get("is_capsule") == "true":
                    unlock = datetime.fromisoformat(m["capsule_unlock_at"])
                    if now >= unlock:
                        expired.append({
                            "id": result["ids"][i], "unlock_at": m["capsule_unlock_at"],
                            "content": result["documents"][i] if result["documents"] else "",
                            "created": m.get("created_date", ""),
                        })
        if not expired:
            print("没有到期的时间胶囊"); return
        print(f"发现 {len(expired)} 个已到期的时间胶囊!\n{'='*60}")
        for e in expired:
            print(f"  ID: {e['id']}")
            print(f"  封存: {e['created']}, 解锁: {e['unlock_at']}")
            print(f"  内容: {e['content']}")
            print()


# ========== import ==========
def _parse_markdown(text):
    entries = []
    current = {"content": "", "date": "", "emotion": "medium", "keywords": ""}
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            if current["content"]: entries.append(dict(current))
            current = {"content": line.lstrip("#"), "date": "", "emotion": "medium", "keywords": ""}
            try:
                datetime.strptime(line.lstrip("#").strip()[:10], "%Y-%m-%d")
                current["date"] = line.lstrip("#").strip()[:10]
            except (ValueError, IndexError): pass
        elif line.startswith(">"):
            ml = line[1:].strip()
            for tag in ["extreme", "high", "medium", "low"]:
                if tag in ml.lower(): current["emotion"] = tag; break
        elif line:
            current["content"] = (current["content"] + "\n" + line).strip() if current["content"] else line
    if current["content"]: entries.append(dict(current))
    return entries


def _parse_text(text):
    entries = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block: continue
        lines = block.split("\n"); date = ""; content = block
        try:
            datetime.strptime(lines[0][:10], "%Y-%m-%d")
            date = lines[0][:10]; content = "\n".join(lines[1:]) if len(lines) > 1 else block
        except (ValueError, IndexError): pass
        entries.append({"content": content, "date": date, "emotion": "medium", "keywords": ""})
    return entries


def cmd_import(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    fmt = args.format

    if fmt == "json":
        with open(args.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        memories = data if isinstance(data, list) else data.get("memories", [data])
        count = 0
        for mem in memories:
            content = mem.get("content", mem.get("text", ""))
            if not content.strip(): continue
            metadata = {
                "type": mem.get("type", "imported"),
                "emotion": mem.get("emotion", "medium"),
                "emotion_weight": EMOTION_WEIGHTS.get(mem.get("emotion", "medium"), 0.5),
                "created_at": mem.get("created_at", _now().isoformat()),
                "created_date": mem.get("created_date", ""),
                "updated_at": _now().isoformat(),
                "keywords": mem.get("keywords", ""),
                "frequency": 1, "recall_count": 0,
            }
            mid = mem.get("id", str(uuid.uuid4()))
            try:
                mem_col.add(documents=[content], metadatas=[metadata], ids=[mid])
            except Exception:
                mem_col.add(documents=[content], metadatas=[metadata], ids=[str(uuid.uuid4())])
            count += 1
        print(f"已从 JSON 导入 {count} 条记忆")
        return

    with open(args.filepath, "r", encoding="utf-8") as f:
        content = f.read()
    entries = _parse_markdown(content) if fmt == "markdown" else _parse_text(content)
    count = 0
    for entry in entries:
        metadata = {
            "type": "imported", "emotion": entry.get("emotion", "medium"),
            "emotion_weight": EMOTION_WEIGHTS.get(entry.get("emotion", "medium"), 0.5),
            "created_at": entry.get("date", _now().isoformat()),
            "created_date": entry.get("date", "")[:10],
            "updated_at": _now().isoformat(),
            "keywords": entry.get("keywords", ""),
            "source": f"imported_{fmt}",
            "frequency": 1, "recall_count": 0,
        }
        mem_col.add(documents=[entry["content"]], metadatas=[metadata], ids=[str(uuid.uuid4())])
        count += 1
    print(f"已从 {fmt} 导入 {count} 条记忆")


# ========== export ==========
def cmd_export(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    result = mem_col.get()
    if not result["ids"]:
        print("没有可导出的记忆"); return

    memories = []
    for i in range(len(result["ids"])):
        meta = result["metadatas"][i] if result["metadatas"] else {}
        memories.append({
            "id": result["ids"][i],
            "content": result["documents"][i] if result["documents"] else "",
            "metadata": meta,
        })
    memories.sort(key=lambda m: m["metadata"].get("created_at", ""))

    if args.format == "json":
        data = {"version": "1.0.0", "export_date": _now().isoformat(), "total": len(memories), "memories": memories}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已导出 {len(memories)} 条记忆到 JSON: {args.output}")
        return

    if args.format == "timeline":
        lines = [f"# 忆时 · 记忆时间线", f"导出日期: {_now().strftime('%Y-%m-%d %H:%M:%S')}", f"总记忆数: {len(memories)}", ""]
        current_date = None
        e_map = {"extreme": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        for m in memories:
            ds = m["metadata"].get("created_date", "")[:10]
            meta = m["metadata"]; mt = meta.get("type", "context")
            ee = e_map.get(meta.get("emotion", ""), "⚪")
            if ds != current_date:
                current_date = ds; lines.append(f"## {ds}"); lines.append("")
            ct = " 🔒" if meta.get("is_capsule") == "true" else ""
            lines.append(f"### {ee} [{mt.upper()}]{ct}")
            lines.append(f"- 关键字: {meta.get('keywords', '无')}")
            lines.append(f"- 情绪: {meta.get('emotion', 'medium')}")
            lines.append(f"- {m['content']}")
            lines.append("")
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"已导出 {len(memories)} 条记忆到时间线: {args.output}")
        return

    lines = ["# 忆时 · 记忆导出", f"导出日期: {_now().strftime('%Y-%m-%d %H:%M:%S')}", f"总记忆数: {len(memories)}", ""]
    for m in memories:
        meta = m["metadata"]; mt = meta.get("type", "context")
        lines.append("---")
        lines.append(f"**类型**: {mt}  |  **情绪**: {meta.get('emotion', 'medium')}  |  **日期**: {meta.get('created_date', '')}")
        if meta.get("keywords"): lines.append(f"**关键字**: {meta['keywords']}")
        lines.append(""); lines.append(m["content"]); lines.append("")
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"已导出 {len(memories)} 条记忆到 Markdown: {args.output}")


# ========== forget ==========
def cmd_forget(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    result = mem_col.get()
    if not result["ids"]:
        print("没有记忆可处理"); return
    now = _now(); candidates = []
    for i in range(len(result["ids"])):
        meta = result["metadatas"][i] if result["metadatas"] else {}
        try: created = datetime.fromisoformat(meta.get("created_at", now.isoformat()))
        except (ValueError, TypeError): continue
        if args.before and created >= datetime.fromisoformat(args.before): continue
        if args.low_freq is not None and (int(meta.get("frequency", 1)) > args.low_freq or int(meta.get("recall_count", 0)) > args.low_freq): continue
        candidates.append({"id": result["ids"][i], "date": created.strftime("%Y-%m-%d"), "meta": meta})
    if not candidates:
        print("没有符合条件的记忆"); return
    print(f"发现 {len(candidates)} 条可处理记忆:")
    for c in candidates: print(f"  {c['id']} (创建: {c['date']})")
    if args.auto:
        for c in candidates:
            m = dict(c["meta"]); m["archived"] = "true"; m["updated_at"] = now.isoformat()
            mem_col.update(ids=[c["id"]], metadatas=[m])
        print(f"\n已将 {len(candidates)} 条记忆标记为已归档")
    else:
        print("\n使用 --auto 自动标记归档")


# ========== recover ==========
def cmd_recover(args):
    """从备份文件恢复所有记忆到 ChromaDB。"""
    records = _load_backups()
    if not records:
        print(f"未找到备份文件: {BACKUP_FILE}")
        print("尚无自动备份，若曾用 export 导出过 JSON，可用 import-file 恢复。")
        return

    client = get_client()
    mem_col = get_collection(client, "memories")
    meta_col = get_collection(client, "meta")
    now = _now()
    restored = 0

    for rec in records:
        mid = rec.get("id", str(uuid.uuid4()))
        content = rec.get("content", "")
        meta = rec.get("metadata", {})
        # 确保元数据字段完整
        meta.setdefault("frequency", 1)
        meta.setdefault("recall_count", 0)
        meta.setdefault("updated_at", now.isoformat())
        # 跳过已存在的（按 id 去重）
        try:
            existing = mem_col.get(ids=[mid])
            if existing["ids"]:
                continue
        except Exception:
            pass
        try:
            mem_col.add(documents=[content], metadatas=[meta], ids=[mid])
            restored += 1
        except Exception as e:
            print(f"  ⚠️ 恢复失败 ({mid}): {e}", file=sys.stderr)

    # 更新 meta 统计
    total = mem_col.count()
    try:
        if meta_col.count() > 0:
            s = json.loads(meta_col.get(ids=["state"])["documents"][0])
            s["total_memories"] = total
            s["updated_at"] = now.isoformat()
            meta_col.update(documents=[json.dumps(s)], ids=["state"], metadatas=[{"key": "state"}])
    except Exception:
        pass

    print(f"恢复完成: 备份 {len(records)} 条, 恢复 {restored} 条")
    print(f"  当前记忆总数: {total}")
    print(f"  备份文件: {BACKUP_FILE}")
    if restored < len(records):
        print(f"  跳过 {len(records) - restored} 条（已存在）")


def main():
    parser = argparse.ArgumentParser(description="忆时 Memory Core", formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("init"); p.set_defaults(func=cmd_init)

    p = sub.add_parser("store", help="存储新记忆")
    p.add_argument("content", help="记忆内容")
    p.add_argument("--type", choices=VALID_TYPES, help="记忆类型")
    p.add_argument("--emotion", choices=VALID_EMOTIONS, help="情绪强度")
    p.add_argument("--keywords", help="关键字")
    p.add_argument("--source", help="来源"); p.add_argument("--session", help="会话ID")
    p.set_defaults(func=cmd_store)

    p = sub.add_parser("recall", help="检索记忆")
    p.add_argument("query", help="查询内容")
    p.add_argument("--limit", type=int, default=10, help="返回数量")
    p.add_argument("--mode", choices=["all", "recent", "emotion", "semantic"], help="检索模式")
    p.add_argument("--min-weight", type=float, default=0.0, help="最低权重分数")
    p.add_argument("--type-filter", choices=VALID_TYPES, help="按类型过滤")
    p.add_argument("--expand", action="store_true", help="联想扩散")
    p.set_defaults(func=cmd_recall)

    p = sub.add_parser("update", help="更新记忆")
    p.add_argument("--id", required=True, help="记忆ID")
    p.add_argument("--content", help="新内容"); p.add_argument("--keywords", help="新关键字")
    p.add_argument("--emotion", choices=VALID_EMOTIONS, help="新情绪"); p.add_argument("--type", choices=VALID_TYPES, help="新类型")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("delete", help="删除记忆")
    p.add_argument("--id", required=True, help="记忆ID")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("stats", help="统计信息"); p.set_defaults(func=cmd_stats)

    p = sub.add_parser("recover", help="从备份文件恢复记忆库（data/ 被误删时使用）"); p.set_defaults(func=cmd_recover)

    p = sub.add_parser("forget", help="遗忘/归档旧记忆")
    p.add_argument("--before", help="归档此日期之前的记忆"); p.add_argument("--low-freq", type=int, help="频率阈值"); p.add_argument("--auto", action="store_true", help="自动标记")
    p.set_defaults(func=cmd_forget)

    cap = sub.add_parser("capsule", help="时间胶囊")
    cap.add_argument("capsule_action", choices=["lock", "unseal", "list", "check-expired"])
    cap.add_argument("--content", help="胶囊内容"); cap.add_argument("--summary", help="摘要")
    cap.add_argument("--keywords", help="关键字"); cap.add_argument("--unlock-at", help="解锁日期")
    cap.add_argument("--capsule-id", help="胶囊ID")
    cap.set_defaults(func=cmd_capsule)

    imp = sub.add_parser("import-file", help="导入")
    imp.add_argument("filepath", help="文件路径")
    imp.add_argument("--format", choices=["markdown", "text", "json"], default="text")
    imp.set_defaults(func=cmd_import)

    exp = sub.add_parser("export", help="导出")
    exp.add_argument("--format", choices=["markdown", "timeline", "json"], default="markdown")
    exp.add_argument("--output", required=True, help="输出文件")
    exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    if not args.command:
        parser.print_help(); sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
