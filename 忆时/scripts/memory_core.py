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
import re
import sys
import time
import uuid
import warnings
import contextlib
from datetime import datetime, timedelta
from pathlib import Path

# 静默 ONNX C++ 层 Schema error 滋扰
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
import jieba  # noqa: E402  须在 filterwarnings 之后 import，压 pkg_resources 弃用警告
jieba.setLogLevel(60)  # 静默建词典日志

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

DATA_DIR = os.environ.get("MEMO_DIR") or os.environ.get("YISHI_DATA_DIR") or os.path.join(LOCAL_BASE, "data")

if os.environ.get("YISHI_DATA_DIR") and not os.environ.get("MEMO_DIR"):
    print("⚠️ YISHI_DATA_DIR 已更名 MEMO_DIR，请更新调用", file=sys.stderr)

SKILL_MODEL_BASE = os.path.join(LOCAL_BASE, "models")

# 自动备份文件（JSONL 格式），存于 LOCAL_BASE 而非 data/ 中，
# 即使 data/ 被误删也能用 recover 命令重建记忆库。
# 可用环境变量 MEMO_BAK 覆盖（多实例/测试隔离）。
BACKUP_FILE = os.environ.get("MEMO_BAK") or os.environ.get("YISHI_BACKUP_FILE") or os.path.join(LOCAL_BASE, "memories_backup.jsonl")

# 情绪强度：统一用 0.0~1.0 数值表示（数值越大越重要/强烈）。
# 旧版词语（extreme/high/medium/low）自动映射为数值，兼容历史数据。
EMOTION_WORD_MAP = {"extreme": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2}
EMOTION_WEIGHTS = dict(EMOTION_WORD_MAP)

def norm_emotion(val):
    """把任意情绪输入归一为 0.0~1.0 数值：
    - 数字字符串（"0.85"）→ 原值
    - 旧版词语（"high"）→ 映射数值
    - 无效 → 0.5
    """
    if val is None:
        return 0.5
    s = str(val).strip().lower()
    if s in EMOTION_WORD_MAP:
        return EMOTION_WORD_MAP[s]
    try:
        f = float(s)
        return max(0.0, min(1.0, f))
    except (ValueError, TypeError):
        return 0.5

def emotion_emoji(val):
    """按情绪数值映射 emoji：≥0.9 🔴、≥0.7 🟠、≥0.4 🟡、否则 🟢"""
    w = norm_emotion(val)
    if w >= 0.9: return "🔴"
    if w >= 0.7: return "🟠"
    if w >= 0.4: return "🟡"
    return "🟢"

RECALL_DECAY_DAYS = 90.0
VALID_TYPES = {"emotion", "decision", "task", "time", "preference", "context", "skill"}

# ── 混合检索（BM25 关键词路 + 向量路 RRF 融合）─
RRF_K = 60.0                # RRF 融合常数（标准值 60）
BM25_K1 = 1.5               # BM25 词频饱和参数
BM25_B = 0.75               # BM25 文档长度归一参数
BM25_SEM_CAP = 0.7          # BM25 归一化分封顶：关键词命中 ≠ 语义相关，防虚高顶榜
MERGE_SIM_HIGH = 0.90       # 去重：相似度高于此值 → 自动合并（实测子串包含≈0.91）
MERGE_SIM_WARN = 0.85       # 去重：高于此值 → 警告仍存
BM25_KEYWORD_WEIGHT = 2     # keywords 分词重复次数（权重×2）
_STOP_WORDS = frozenset(
    "的了是在我有和就都而及与或一个不也这那你们我们他们她他它它们被把让从到对向为以于之乎者也"
    "啊呢吧吗哦嗯好行对没啥啥很最更再又还已经正在将要可以可能应该必须不要没有什么怎么为什么"
    "因为所以但是然而如果那么虽然尽管只是还是或者以及关于对于通过由于根据按照例如比如这个那个"
    "自己这里那里时候时候东西事情问题方法方式情况结果原因目的意义价值作用影响关系问题"
)

_embedding_client = None
_embedding_fn = None


def get_embedding_fn():
    global _embedding_fn
    if _embedding_fn is None:
        # 仅支持 bge-base-zh-v1.5（768 维）。模型目录：
        #   {SKILL_MODEL_BASE}/bge-base-zh-v1.5/{onnx/model.onnx, tokenizer.json, ...}
        # 安装方法见 modules/08-setup.md。无回退——MiniLM 384 维与 768 维数据不兼容，曾致维度冲突。
        bge_dir = os.path.join(SKILL_MODEL_BASE, "bge-base-zh-v1.5")
        bge_onnx = os.path.join(bge_dir, "onnx", "model.onnx")
        if not os.path.exists(bge_onnx):
            print(
                "❌ 未找到 bge-base-zh-v1.5 模型（768 维）：" + bge_onnx + "\n"
                "   安装方法见 modules/08-setup.md（hf-mirror 下载 Xenova/bge-base-zh-v1.5 至该目录）。",
                file=sys.stderr,
            )
            sys.exit(1)
        with _silent_import():
            _embedding_fn = _BGEONNX(bge_dir)
    return _embedding_fn


class _BGEONNX:
    """bge-base-zh-v1.5 ONNX embedding：768 维，CLS pooling，L2 归一化。

    中文语义检索，显著优于英文模型 all-MiniLM-L6-v2。
    模型目录：{SKILL_MODEL_BASE}/bge-base-zh-v1.5/{onnx/model.onnx, tokenizer.json, ...}
    """

    def __init__(self, model_dir):
        import onnxruntime as ort
        from tokenizers import Tokenizer

        self._np = __import__("numpy")
        self.session = ort.InferenceSession(
            os.path.join(model_dir, "onnx", "model.onnx"),
            providers=["CPUExecutionProvider"],
        )
        self.tok = Tokenizer.from_file(os.path.join(model_dir, "tokenizer.json"))
        self.tok.enable_truncation(max_length=512)
        self.tok.enable_padding(pad_id=0, pad_token="[PAD]")

    @staticmethod
    def name():
        return "bge-base-zh-v1.5"

    def embed_query(self, input):
        # Chroma 1.5.9 embed_query 为 batch 语义：入 ['q'] 出 [[768]]；直调可能传 str——双兼容
        if isinstance(input, str):
            input = [input]
        return self.__call__(input)

    def embed_documents(self, input):
        return self.__call__(input)

    def __call__(self, input):
        np = self._np
        if isinstance(input, str):
            input = [input]
        enc = self.tok.encode_batch(list(input))
        ids = [e.ids for e in enc]
        attn = [e.attention_mask for e in enc]
        tids = [e.type_ids for e in enc]
        out = self.session.run(None, {
            "input_ids": np.array(ids, dtype=np.int64),
            "attention_mask": np.array(attn, dtype=np.int64),
            "token_type_ids": np.array(tids, dtype=np.int64),
        })[0]
        emb = out[:, 0, :]
        emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)
        return emb.astype(np.float32).tolist()


def get_client():
    global _embedding_client
    if _embedding_client is None:
        os.makedirs(DATA_DIR, exist_ok=True)
        last_err = None
        # 2026-08-14 修复：多会话并发时 chroma 偶发抛
        #   InternalError: (code: 8) attempt to write a readonly database
        # （sqlite delete journal 模式写互斥 + 并发窗口）。库已转 WAL，此处再加重试兜底。
        for _ in range(6):
            try:
                _embedding_client = chromadb.PersistentClient(path=DATA_DIR)
                break
            except chromadb.errors.InternalError as e:
                if "readonly" not in str(e).lower() and "locked" not in str(e).lower():
                    raise
                last_err = e
                time.sleep(0.5)
        else:
            raise last_err
    return _embedding_client


def get_collection(client, name):
    ef = get_embedding_fn()
    try:
        if ef:
            return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"}, embedding_function=ef)
        return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})
    except ValueError as e:
        if "embedding function" in str(e) and "conflict" in str(e).lower():
            # 存量 collection 由旧 embedding（onnx_mini_lm_l6_v2）创建，与 bge 维度不兼容：
            # 不传 ef，沿用持久化配置读写，保证新旧数据 embedding 一致（不回退即全部不可用）。
            return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})
        raise


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


# ========== 混合检索（BM25 关键词路）==========
def _tokenize(text):
    """jieba 分词 + 过滤停用词/单字中文/纯符号。keywords 以 BM25_KEYWORD_WEIGHT 倍权重入。"""
    toks = []
    parts = text.split("|||")  # 分隔符：content ||| keywords
    for pi, part in enumerate(parts):
        repeat = BM25_KEYWORD_WEIGHT if pi == 1 else 1
        for w in jieba.lcut(part):
            w = w.strip().lower()
            if not w or w in _STOP_WORDS:
                continue
            if len(w) == 1 and "\u4e00" <= w <= "\u9fff":
                continue
            if not re.search(r"[\w\u4e00-\u9fff]", w):
                continue
            toks.extend([w] * repeat)
    return toks


def _bm25_scores(docs, query_tokens, k1=BM25_K1, b=BM25_B):
    """对全部文档打 BM25 分，返回 {mem_id: score}。"""
    N = len(docs)
    if N == 0 or not query_tokens:
        return {}
    df = {}
    doc_len = {}
    for i, (_, toks) in enumerate(docs):
        seen = set()
        for t in toks:
            if t not in seen:
                df[t] = df.get(t, 0) + 1
                seen.add(t)
        doc_len[i] = len(toks)
    avgdl = sum(doc_len.values()) / N
    scores = {}
    for i, (mid, toks) in enumerate(docs):
        tf = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        dl = doc_len[i]
        s = 0.0
        for q in query_tokens:
            if q not in tf:
                continue
            idf = math.log(1.0 + (N - df.get(q, 0) + 0.5) / (df.get(q, 0) + 0.5))
            s += idf * tf[q] * (k1 + 1.0) / (tf[q] + k1 * (1.0 - b + b * dl / avgdl))
        scores[mid] = s
    return scores


def _bm25_search(query, limit):
    """BM25 关键词检索：以 JSONL 备份为数据源，返回 [(mem_id, score), ...] 降序。"""
    records = _load_backups()
    if not records:
        return []
    docs = []
    for rec in records:
        mid = rec.get("id", "")
        content = rec.get("content", "") or ""
        meta = rec.get("metadata", {}) or {}
        kw = meta.get("keywords", "") or ""
        if mid and (content or kw):
            docs.append((mid, _tokenize(f"{content}|||{kw}")))
    if not docs:
        return []
    qt = _tokenize(query)
    scores = _bm25_scores(docs, qt)
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    if limit:
        ranked = ranked[:limit]
    return ranked


def _rrf_merge(ranked_lists, limit):
    """Reciprocal Rank Fusion：多路排名融合，返回 [(mem_id, rrf_score), ...] 降序。"""
    rrf = {}
    for lst in ranked_lists:
        for rank, (mid, _) in enumerate(lst):
            rrf[mid] = rrf.get(mid, 0.0) + 1.0 / (RRF_K + rank + 1.0)
    order = sorted(rrf.items(), key=lambda x: -x[1])
    if limit:
        order = order[:limit]
    return order


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
def _merge_keywords(old_kw, new_kw):
    merged = []
    for kw in (old_kw or "").split(",") + (new_kw or "").split(","):
        k = kw.strip()
        if k and k not in merged:
            merged.append(k)
    return ",".join(merged)


def cmd_store(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    now = _now()
    emo_val = norm_emotion(args.emotion)
    mem_type = args.type or "context"

    metadata = {
        "type": mem_type,
        "emotion": emo_val,
        "emotion_weight": emo_val,
        "created_at": now.isoformat(),
        "created_date": now.strftime("%Y-%m-%d"),
        "updated_at": now.isoformat(),
        "keywords": args.keywords or "",
        "source": args.source or "manual",
        "source_session": args.session or "",
        "frequency": 1,
        "recall_count": 0,
    }
    # 场景与活动时间段（段段时间语义，借鉴分层记忆场景块）
    if getattr(args, "scene", None):
        metadata["scene"] = args.scene
    if getattr(args, "activity_start", None):
        metadata["activity_start"] = args.activity_start
    if getattr(args, "activity_end", None):
        metadata["activity_end"] = args.activity_end
    # skill 类型自动追加 "skill" 标签
    if mem_type == "skill":
        if "skill" not in (args.keywords or ""):
            args.keywords = (args.keywords + ",skill") if args.keywords else "skill"
        metadata["keywords"] = args.keywords
    # 传播 --skill-* 参数到 metadata
    for key in ("skill_name", "skill_summary", "skill_strategy", "skill_avoid",
                 "skill_triggers", "skill_input", "skill_output", "skill_version"):
        val = getattr(args, key.replace("-", "_"), None)
        if val is not None:
            metadata[key] = val

    # ── 去重合并：存前查最相似记忆 ──
    if not getattr(args, "force", False):
        try:
            dup = mem_col.query(query_texts=[args.content], n_results=1)
            if dup["ids"] and dup["ids"][0]:
                did = dup["ids"][0][0]
                ddist = dup["distances"][0][0] if dup["distances"] else 1.0
                dsim = 1.0 - ddist
                if dsim > MERGE_SIM_HIGH:
                    old = mem_col.get(ids=[did])
                    if old["ids"]:
                        om = old["metadatas"][0]
                        ocontent = old["documents"][0]
                        new_content = ocontent
                        if args.content.strip() not in ocontent:
                            new_content = f"{ocontent}。{args.content.strip()}"
                        nm = dict(om)
                        nm["content"] = new_content
                        nm["keywords"] = _merge_keywords(om.get("keywords", ""), args.keywords or "")
                        nm["frequency"] = int(om.get("frequency", 1)) + 1
                        nm["updated_at"] = now.isoformat()
                        if emo_val > float(om.get("emotion_weight", 0.5)):
                            nm["emotion"] = emo_val
                            nm["emotion_weight"] = emo_val
                        for f in ("scene", "activity_start", "activity_end"):
                            if getattr(args, f, None) and not om.get(f):
                                nm[f] = getattr(args, f)
                        mem_col.update(ids=[did], documents=[new_content], metadatas=[nm])
                        _append_backup(did, new_content, nm)
                        print(f"记忆已合并（相似 {dsim:.0%} > {MERGE_SIM_HIGH:.0%}）")
                        print(f"  ID: {did}  frequency: {nm['frequency']}")
                        print(f"  合并内容: {new_content[:120]}")
                        return did
        except Exception:
            pass

    mem_id = str(uuid.uuid4())
    mem_col.add(documents=[args.content], metadatas=[metadata], ids=[mem_id])
    _update_meta_total(client, "total_memories", 1)

    # 自动备份到 JSONL（与 data/ 独立，不怕误删）
    _append_backup(mem_id, args.content, metadata)

    # 去重警告（相似但未达合并阈值）
    if not getattr(args, "force", False):
        try:
            wq = mem_col.query(query_texts=[args.content], n_results=1)
            if wq["ids"] and wq["ids"][0]:
                wdist = wq["distances"][0][0] if wq["distances"] else 1.0
                wsim = 1.0 - wdist
                if wsim > MERGE_SIM_WARN and wq["ids"][0][0] != mem_id:
                    print(f"  ⚠️ 提示: 与已有记忆相似 {wsim:.0%}（ID: {wq['ids'][0][0]}），可能重复")
        except Exception:
            pass

    # 自动建语义关联：找相似记忆，写入 relationships 集合
    # 关键词各自保留，不做跨记忆融合（避免关键词雪球式膨胀）
    try:
        rel_col = get_collection(client, "relationships")
        similar = mem_col.query(query_texts=[args.content], n_results=6)
        if similar["ids"] and similar["ids"][0]:
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
            _update_meta_total(client, "total_relationships", 1)
    except Exception:
        pass

    print(f"记忆已存储")
    print(f"  ID: {mem_id}")
    print(f"  类型: {mem_type}  情绪: {emo_val} {emotion_emoji(emo_val)}")
    if metadata.get("scene"):
        print(f"  场景: {metadata['scene']}")
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

    # ── 混合检索：向量路 + BM25 关键词路，RRF 融合成候选池 ──
    no_embed = getattr(args, "no_embed", False)
    vec_ranked = []
    vec_semantic = {}
    if not no_embed:
        try:
            vec_results = mem_col.query(query_texts=[query], n_results=limit * 6)
            if vec_results["ids"] and vec_results["ids"][0]:
                for j in range(len(vec_results["ids"][0])):
                    mid = vec_results["ids"][0][j]
                    dist = vec_results["distances"][0][j] if vec_results["distances"] else 1.0
                    sem = 1.0 - dist
                    vec_ranked.append((mid, sem))
                    vec_semantic[mid] = sem
        except Exception:
            vec_ranked = []
            vec_semantic = {}

    bm25_ranked = _bm25_search(query, limit * 6)
    bm25_semantic = {}
    if bm25_ranked:
        bmax = max((s for _, s in bm25_ranked), default=0.0)
        if bmax > 0:
            for mid, s in bm25_ranked:
                bm25_semantic[mid] = s / bmax

    fused = _rrf_merge([vec_ranked, bm25_ranked], limit * 3)
    if not fused:
        print("没有找到相关记忆")
        return

    scored = []
    seen = set()
    cand_ids = [mid for mid, _ in fused]
    pool = {}
    try:
        pg = mem_col.get(ids=cand_ids)
        if pg["ids"]:
            for pi in range(len(pg["ids"])):
                pool[pg["ids"][pi]] = (
                    pg["documents"][pi] if pg["documents"] else "",
                    pg["metadatas"][pi] if pg["metadatas"] else {},
                )
    except Exception:
        pass

    for mid in cand_ids:
        if mid in seen or mid not in pool:
            continue
        seen.add(mid)
        doc, meta = pool[mid]
        semantic = max(vec_semantic.get(mid, 0.0), bm25_semantic.get(mid, 0.0) * BM25_SEM_CAP)
        em_w = float(meta.get("emotion_weight", 0.5))
        recall_count = int(meta.get("recall_count", 0))
        freq = int(meta.get("frequency", 1))
        freq_boost = min(math.log2(freq + 1) * 0.1, 0.2) + min(math.log2(recall_count + 1) * 0.02, 0.06)
        created = datetime.fromisoformat(meta.get("created_at", now.isoformat()))
        days_ago = (now - created).total_seconds() / 86400.0
        recency = math.exp(-math.log(2) * days_ago / RECALL_DECAY_DAYS)

        # 语义主导 0.60；情绪/近因/频率仅作微调（合计 0.40）
        score = 0.60 * semantic + 0.08 * em_w + 0.12 * recency + 0.20 * (0.3 + freq_boost)
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
            "scene": meta.get("scene", ""),
            "activity_start": meta.get("activity_start", ""),
            "activity_end": meta.get("activity_end", ""),
            "is_capsule": meta.get("is_capsule", "false") == "true",
            "capsule_unlock_at": meta.get("capsule_unlock_at", ""),
            "frequency": freq, "recall_count": recall_count, "is_expanded": False,
        })

    # === Trigger 关键词匹配（针对 type=skill 记忆） ===
    try:
        trigger_results = mem_col.get(where={"type": "skill"})
        if trigger_results["ids"]:
            query_lower = query.lower()
            for i in range(len(trigger_results["ids"])):
                tid = trigger_results["ids"][i]
                if tid in seen:
                    continue
                meta = trigger_results["metadatas"][i] if trigger_results["metadatas"] else {}
                kws = meta.get("keywords", "")
                triggers = [k.strip().split(":", 1)[1] for k in kws.split(",") if k.strip().startswith("trigger:")]
                if not any(t.lower() in query_lower for t in triggers if t.strip()):
                    continue
                doc = trigger_results["documents"][i] if trigger_results["documents"] else ""
                em_w = float(meta.get("emotion_weight", 0.5))
                freq = int(meta.get("frequency", 1))
                rc = int(meta.get("recall_count", 0))
                created = datetime.fromisoformat(meta.get("created_at", now.isoformat()))
                scored.append({
                    "id": tid, "content": doc, "score": 0.85,
                    "semantic": 0.7, "emotion": meta.get("emotion", "medium"),
                    "emotion_weight": em_w, "type": "skill",
                    "created_at": meta.get("created_at", ""), "created_date": meta.get("created_date", ""),
                    "keywords": kws,
                    "is_capsule": meta.get("is_capsule", "false") == "true",
                    "capsule_unlock_at": meta.get("capsule_unlock_at", ""),
                    "frequency": freq, "recall_count": rc, "is_expanded": True, "is_trigger_match": True,
                })
                seen.add(tid)
    except Exception:
        pass

    # === 联想扩散（两阶段），统一用真实语义值计分 ===
    def _compute_score(semantic, em_w, freq, recall_count, created):
        freq_boost = min(math.log2(freq + 1) * 0.1, 0.2) + min(math.log2(recall_count + 1) * 0.02, 0.06)
        days_ago = (now - created).total_seconds() / 86400.0
        recency = math.exp(-math.log(2) * days_ago / RECALL_DECAY_DAYS)
        # 语义主导 0.60；情绪/近因/频率仅作微调（合计 0.40）
        return 0.60 * semantic + 0.08 * em_w + 0.12 * recency + 0.20 * (0.3 + freq_boost)

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

    type_emoji = {"task": "📋", "decision": "⚖️", "preference": "⭐", "emotion": "💜", "time": "⏰", "context": "📌", "imported": "📥", "skill": "🔧"}

    total = len(scored)
    print(f"\n  记忆检索 ── 查询「{query}」 命中 {total} 条\n")

    TRUNC_SUFFIX = "…（已截断）"
    max_per = getattr(args, "max_chars_per_item", 0) or 0
    max_total = getattr(args, "max_total_chars", 0) or 0
    used_chars = 0

    for idx, item in enumerate(scored, 1):
        e_emoji = emotion_emoji(item.get("emotion"))
        emo_val = norm_emotion(item.get("emotion"))
        t_emoji = type_emoji.get(item.get("type", ""), "📄")
        capsule_tag = " 🔒" if item["is_capsule"] else ""
        assoc_tag = " ⟡关联" if item.get("is_expanded") else ""
        trigger_tag = " ⚡触发" if item.get("is_trigger_match") else ""
        scene_tag = f" | {item['scene']}" if item.get("scene") else ""
        type_label = item['type'].upper()
        score_pct = int(item.get("score", 0) * 100)

        kw = item.get("keywords", "")
        kw_display = ""
        if kw:
            kw_list = [k.strip() for k in kw.split(",") if k.strip()]
            if len(kw_list) > 6:
                kw_display = "、".join(kw_list[:6]) + f" 等{len(kw_list)}个"
            else:
                kw_display = "、".join(kw_list)

        content = item['content'].replace('\n', ' ').strip()
        per_limit = max_per if max_per else 100
        if len(content) > per_limit:
            content = content[:max(0, per_limit - len(TRUNC_SUFFIX))].rstrip() + TRUNC_SUFFIX

        line_est = len(content) + len(kw_display) + len(item.get("activity_start", "")) + len(item.get("activity_end", "")) + 60
        if max_total and used_chars + line_est > max_total:
            if idx == 1:
                content = content[: max(0, max_total - len(TRUNC_SUFFIX))].rstrip() + TRUNC_SUFFIX
            else:
                print(f"  ……（已达注入预算 {max_total} 字符，余 {total - idx + 1} 条省略）")
                break
        used_chars += line_est

        print(f"  {idx}. {e_emoji} {type_label}{scene_tag}{capsule_tag}{assoc_tag}{trigger_tag}  ──  {item['created_date']}  情绪{emo_val:.2f}  被检索{item['recall_count']}次  匹配{score_pct}%")

        if kw_display:
            print(f"     │ 🏷️ {kw_display}")

        activity = ""
        if item.get("activity_start") or item.get("activity_end"):
            a = item.get("activity_start", "") or "?"
            b = item.get("activity_end", "") or "?"
            activity = f" (活动时间: {a} ~ {b})" if item.get("activity_start") and item.get("activity_end") else f" (活动时间: {a or b})"
        print(f"     │ 📝 {content}{activity}")
        print()


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
        emo = norm_emotion(args.emotion)
        meta["emotion"] = emo
        meta["emotion_weight"] = emo
    if args.type is not None: meta["type"] = args.type
    if args.scene is not None: meta["scene"] = args.scene
    if args.activity_start is not None: meta["activity_start"] = args.activity_start
    if args.activity_end is not None: meta["activity_end"] = args.activity_end
    mem_col.update(ids=[args.id], documents=[content], metadatas=[meta])
    _append_backup(args.id, content, meta)
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
    type_counts = {}; emo_buckets = {"高(≥0.7)": 0, "中(0.4~0.7)": 0, "低(<0.4)": 0}; capsule_count = 0
    result = mem_col.get()
    if result["metadatas"]:
        for m in result["metadatas"]:
            t = m.get("type", "context"); type_counts[t] = type_counts.get(t, 0) + 1
            w = norm_emotion(m.get("emotion"))
            if w >= 0.7: emo_buckets["高(≥0.7)"] += 1
            elif w >= 0.4: emo_buckets["中(0.4~0.7)"] += 1
            else: emo_buckets["低(<0.4)"] += 1
            if m.get("is_capsule") == "true": capsule_count += 1
    print(f"\n  按类型:")
    for t, c in sorted(type_counts.items()): print(f"    {t}: {c}")
    print(f"\n  按情绪强度(数值):")
    for e, c in emo_buckets.items(): print(f"    {e}: {c}")
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
            "type": "context", "emotion": 0.5,
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
    current = {"content": "", "date": "", "emotion": 0.5, "keywords": ""}
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            if current["content"]: entries.append(dict(current))
            current = {"content": line.lstrip("#"), "date": "", "emotion": 0.5, "keywords": ""}
            try:
                datetime.strptime(line.lstrip("#").strip()[:10], "%Y-%m-%d")
                current["date"] = line.lstrip("#").strip()[:10]
            except (ValueError, IndexError): pass
        elif line.startswith(">"):
            ml = line[1:].strip()
            emo_m = re.search(r"情绪[:：]\s*([0-9.]+|[A-Za-z]+)", ml)
            if emo_m:
                current["emotion"] = norm_emotion(emo_m.group(1))
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
        entries.append({"content": content, "date": date, "emotion": 0.5, "keywords": ""})
    return entries


def cmd_import(args):
    client = get_client()
    mem_col = get_collection(client, "memories")
    fmt = args.format

    if not os.path.exists(args.filepath):
        print(f"错误: 文件不存在: {args.filepath}")
        sys.exit(1)

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
                "emotion": norm_emotion(mem.get("emotion")),
                "emotion_weight": norm_emotion(mem.get("emotion")),
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
        emo = norm_emotion(entry.get("emotion"))
        metadata = {
            "type": "imported", "emotion": emo,
            "emotion_weight": emo,
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

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if not os.path.isdir(out_dir):
        print(f"错误: 输出目录不存在: {out_dir}")
        sys.exit(1)

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
        for m in memories:
            ds = m["metadata"].get("created_date", "")[:10]
            meta = m["metadata"]; mt = meta.get("type", "context")
            ee = emotion_emoji(meta.get("emotion"))
            if ds != current_date:
                current_date = ds; lines.append(f"## {ds}"); lines.append("")
            ct = " 🔒" if meta.get("is_capsule") == "true" else ""
            lines.append(f"### {ee} [{mt.upper()}]{ct}")
            lines.append(f"- 关键字: {meta.get('keywords', '无')}")
            lines.append(f"- 情绪: {norm_emotion(meta.get('emotion')):.2f}")
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
        lines.append(f"**类型**: {mt}  |  **情绪**: {norm_emotion(meta.get('emotion')):.2f}  |  **日期**: {meta.get('created_date', '')}")
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

    # 同 id 多条时取最后版本（合并/更新会追加同 id 记录）
    latest = {}
    for rec in records:
        mid = rec.get("id")
        if mid:
            latest[mid] = rec
    for mid, rec in latest.items():
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
    p.add_argument("--emotion", help="情绪强度（0.0~1.0 数值，如 0.9；兼容旧词 high/medium/low）")
    p.add_argument("--keywords", help="关键字")
    p.add_argument("--source", help="来源"); p.add_argument("--session", help="会话ID")
    p.add_argument("--scene", help="场景（如: 教学课后反馈）")
    p.add_argument("--activity-start", help="活动开始时间（如 2025-05-01）")
    p.add_argument("--activity-end", help="活动结束时间（如 2025-05-10）")
    p.add_argument("--force", action="store_true", help="跳过去重合并，强制新增")
    p.add_argument("--skill-name", help="技能名称")
    p.add_argument("--skill-summary", help="技能一句话概括")
    p.add_argument("--skill-strategy", help="技能策略/步骤")
    p.add_argument("--skill-avoid", help="技能禁忌/注意事项")
    p.add_argument("--skill-triggers", help="技能触发关键词")
    p.add_argument("--skill-input", help="技能输入")
    p.add_argument("--skill-output", help="技能输出")
    p.add_argument("--skill-version", default="1.0.0", help="技能版本")
    p.set_defaults(func=cmd_store)

    p = sub.add_parser("recall", help="检索记忆")
    p.add_argument("query", help="查询内容")
    p.add_argument("--limit", type=int, default=10, help="返回数量")
    p.add_argument("--mode", choices=["all", "recent", "emotion", "semantic"], help="检索模式")
    p.add_argument("--min-weight", type=float, default=0.0, help="最低权重分数")
    p.add_argument("--type-filter", choices=VALID_TYPES, help="按类型过滤")
    p.add_argument("--expand", action="store_true", help="联想扩散")
    p.add_argument("--no-embed", action="store_true", help="仅 BM25 关键词检索（快速，不加载 embedding）")
    p.add_argument("--max-chars-per-item", type=int, default=0, help="单条注入字符上限（0=不限）")
    p.add_argument("--max-total-chars", type=int, default=0, help="总注入字符预算（0=不限）")
    p.set_defaults(func=cmd_recall)

    p = sub.add_parser("update", help="更新记忆")
    p.add_argument("--id", required=True, help="记忆ID")
    p.add_argument("--content", help="新内容"); p.add_argument("--keywords", help="新关键字")
    p.add_argument("--emotion", help="新情绪（0.0~1.0 数值，或旧词）"); p.add_argument("--type", choices=VALID_TYPES, help="新类型")
    p.add_argument("--scene", help="新场景")
    p.add_argument("--activity-start", help="新活动开始时间")
    p.add_argument("--activity-end", help="新活动结束时间")
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

    # 2026-08-14 修复：忆时为单写者 sqlite 库，多 opencode 会话并发操作会互相踩
    # （曾现 "attempt to write a readonly database"）。此处对整条命令加进程排他锁，
    # 并发时最多等待约 8 秒，超时报友好错误而非让 chroma 抛底层异常。
    lock_fd = None
    try:
        import fcntl
        os.makedirs(DATA_DIR, exist_ok=True)
        lock_path = os.path.join(DATA_DIR, ".memory.lock")
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
        waited = 0
        while True:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if waited >= 8:
                    print("⚠️ 另一忆时进程正在操作（并发写锁），请稍后再试", file=sys.stderr)
                    os.close(lock_fd); sys.exit(1)
                time.sleep(0.2)
                waited += 0.2
    except ImportError:
        pass  # 非 POSIX 平台退化：无进程锁，仅靠 WAL + 重试兜底

    try:
        args.func(args)
    finally:
        if lock_fd is not None:
            try:
                import fcntl
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            except Exception:
                pass
            os.close(lock_fd)


if __name__ == "__main__":
    main()
