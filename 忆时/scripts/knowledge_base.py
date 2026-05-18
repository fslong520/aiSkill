#!/usr/bin/env python3
"""
忆时 Knowledge Base - 个人知识库引擎

功能:
  - SQLite 文件清单 (路径/大小/mtime/类型/标签)
  - 增量 scandir 扫描 (效 Everything 之速)
  - 项目自动识别 (git/package.json/CMakeLists 等)
  - AI 延迟标注 (规则粗标即时, AI 精准标注延迟)
  - 虚拟分类管理
  - 文件关系图谱
  - 融合搜索 (ChromaDB 记忆 + SQLite 文件)
  - 跨平台文件管理器打开
  - inotify/FSEvents 实时变更监听

用法示例:
  python3 knowledge_base.py init
  python3 knowledge_base.py add ~/Documents --label "文档"
  python3 knowledge_base.py index ~/Documents
  python3 knowledge_base.py find "机器学习" --ext pdf
  python3 knowledge_base.py search "注意力机制"
  python3 knowledge_base.py open <file_id>
  python3 knowledge_base.py status
"""

import argparse
import fnmatch
import hashlib
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ── 路径常量 ───────────────────────────────────────────

HOME = Path.home()
SKILL_DIR = Path(__file__).resolve().parent.parent
DB_DIR = os.environ.get(
    "YISHI_DATA_DIR",
    str(HOME / ".local" / "share" / "opencode" / "忆时" / "data"),
)
KB_DB = os.path.join(DB_DIR, "kb.db")
KB_CONFIG = os.path.join(DB_DIR, "kb_config.json")
MEMORY_CORE_PY = str(SKILL_DIR / "scripts" / "memory_core.py")

# ── 文件类型映射 ───────────────────────────────────────

DOC_EXTS = {'.pdf', '.doc', '.docx', '.txt', '.md', '.markdown', '.rst', '.tex', '.odt', '.rtf', '.epub', '.mobi'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.tif', '.ico', '.psd', '.ai', '.eps', '.raw', '.heic'}
VIDEO_EXTS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.ogv', '.ts'}
AUDIO_EXTS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.ape', '.aiff'}
CODE_EXTS = {
    '.py', '.js', '.ts', '.cpp', '.c', '.h', '.hpp', '.cc', '.cxx',
    '.java', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.cs',
    '.scala', '.lua', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat',
    '.sql', '.r', '.m', '.ipynb', '.html', '.htm', '.css', '.scss',
    '.sass', '.less', '.vue', '.jsx', '.tsx', '.svelte',
    '.toml', '.yaml', '.yml', '.json', '.xml', '.ini', '.cfg', '.conf',
    '.cmake', '.makefile', '.gradle', '.dockerfile',
}
ARCHIVE_EXTS = {'.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar', '.tgz', '.tar.gz', '.tar.xz', '.tar.bz2'}

PROJECT_MARKERS = {
    '.git': '通用项目',
    'package.json': 'Node.js/前端',
    'Cargo.toml': 'Rust',
    'CMakeLists.txt': 'C/C++',
    'setup.py': 'Python',
    'pyproject.toml': 'Python',
    'go.mod': 'Go',
    'Makefile': '通用构建',
    'Dockerfile': 'Docker',
    'docker-compose.yml': 'Docker Compose',
    'pom.xml': 'Java/Maven',
    'build.gradle': 'Java/Gradle',
    'CNAME': '文档站点',
}

EXCLUDE_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv',
    '.env', '.cache', '.mypy_cache', '.pytest_cache', '.tox',
    '.eggs', 'dist', 'build', 'target', '.next', '.nuxt',
    '.idea', '.vscode', '.vs', 'bower_components',
}

PREVIEW_EXTENSIONS = {'.txt', '.md', '.markdown', '.py', '.js', '.ts', '.cpp', '.c', '.h',
                       '.java', '.go', '.rs', '.rb', '.sh', '.bash', '.zsh',
                       '.toml', '.yaml', '.yml', '.json', '.xml', '.html', '.css',
                       '.tex', '.rst', '.ini', '.cfg', '.conf'}

# ── 规则标注关键词 ─────────────────────────────────────

PATH_TAG_MAP = {
    'ml': '机器学习', 'machine': '机器学习', 'deep': '深度学习',
    'dl': '深度学习', 'ai': 'AI', 'nlp': 'NLP', 'cv': '计算机视觉',
    'transformer': 'Transformer', 'attention': '注意力机制',
    '论文': '论文', 'paper': '论文', 'thesis': '论文',
    '笔记': '笔记', 'note': '笔记', 'notes': '笔记',
    '项目': '项目', 'project': '项目',
    '竞赛': '竞赛', 'oi': 'OI', 'noi': 'NOI', 'csp': 'CSP',
    '备课': '备课', 'teaching': '教学', '教案': '教案',
    '代码': '代码', 'code': '代码', 'src': '代码',
    '数据': '数据', 'data': '数据', 'dataset': '数据集',
    '实验': '实验', 'experiment': '实验',
    'test': '测试', '测试': '测试', 'tests': '测试',
    '文档': '文档', 'doc': '文档', 'documents': '文档',
    '图片': '图片', 'image': '图片', 'photo': '照片',
    '视频': '视频', 'video': '视频',
    '音乐': '音乐', 'music': '音乐', 'audio': '音频',
    'config': '配置', 'conf': '配置',
    'docker': 'Docker', 'k8s': 'Kubernetes', 'kubernetes': 'Kubernetes',
    'api': 'API', 'rest': 'API',
    'db': '数据库', 'database': '数据库', 'sql': '数据库',
    '日志': '日志', 'log': '日志',
    '备份': '备份', 'backup': '备份',
    '简历': '简历', 'resume': '简历', 'cv': '简历',
    '合同': '合同', 'contract': '合同',
}

EXT_TAG_MAP = {
    '.pdf': 'PDF', '.md': 'Markdown', '.py': 'Python',
    '.ipynb': 'Jupyter', '.cpp': 'C++', '.c': 'C', '.h': 'C',
    '.js': 'JavaScript', '.ts': 'TypeScript', '.go': 'Go',
    '.rs': 'Rust', '.java': 'Java',
    '.xlsx': '表格', '.xls': '表格', '.csv': '表格',
    '.pptx': '幻灯片', '.ppt': '幻灯片',
    '.jpg': '图片', '.png': '图片', '.svg': '矢量图',
    '.mp4': '视频', '.mp3': '音频',
    '.zip': '压缩包', '.tar': '压缩包', '.gz': '压缩包',
    '.html': 'HTML', '.css': 'CSS',
}


# ── 数据库层 ──────────────────────────────────────────

def _now():
    return datetime.now()


def get_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(KB_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA cache_size=-64000")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS directories (
            id TEXT PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            label TEXT DEFAULT '',
            scan_depth INTEGER DEFAULT 0,
            is_project INTEGER DEFAULT 0,
            is_online INTEGER DEFAULT 1,
            summary TEXT DEFAULT '',
            touch_count INTEGER DEFAULT 0,
            indexed_at TEXT,
            last_seen TEXT
        );

        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            dir_id TEXT REFERENCES directories(id) ON DELETE CASCADE,
            rel_path TEXT NOT NULL,
            abs_path TEXT NOT NULL UNIQUE,
            file_type TEXT NOT NULL,
            extension TEXT,
            size INTEGER,
            mtime REAL,
            md5 TEXT,
            rules_tags TEXT DEFAULT '',
            ai_tags TEXT DEFAULT '',
            ai_summary TEXT DEFAULT '',
            annotated INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT,
            UNIQUE(dir_id, rel_path)
        );

        CREATE TABLE IF NOT EXISTS file_relations (
            id TEXT PRIMARY KEY,
            source_id TEXT REFERENCES files(id) ON DELETE CASCADE,
            target_id TEXT REFERENCES files(id) ON DELETE CASCADE,
            rel_type TEXT NOT NULL,
            confidence REAL DEFAULT 0.5,
            reason TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            query_json TEXT NOT NULL,
            description TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS scan_snapshots (
            id TEXT PRIMARY KEY,
            dir_id TEXT REFERENCES directories(id) ON DELETE CASCADE,
            scanned_at TEXT,
            total INTEGER,
            new_files INTEGER,
            modified INTEGER,
            deleted INTEGER
        );

        CREATE INDEX IF NOT EXISTS idx_files_dir ON files(dir_id);
        CREATE INDEX IF NOT EXISTS idx_files_type ON files(file_type);
        CREATE INDEX IF NOT EXISTS idx_files_ext ON files(extension);
        CREATE INDEX IF NOT EXISTS idx_files_abs ON files(abs_path);
        CREATE INDEX IF NOT EXISTS idx_files_annotated ON files(annotated);
        CREATE INDEX IF NOT EXISTS idx_files_rules_tags ON files(rules_tags);
        CREATE INDEX IF NOT EXISTS idx_files_ai_tags ON files(ai_tags);
        CREATE INDEX IF NOT EXISTS idx_relations_source ON file_relations(source_id);
        CREATE INDEX IF NOT EXISTS idx_relations_target ON file_relations(target_id);
        CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
    """)
    conn.commit()
    conn.close()


# ── 配置文件 ──────────────────────────────────────────

DEFAULT_CONFIG = {
    "version": "1.0.0",
    "directories": [],
    "exclude": {
        "patterns": ["*.tmp", "*.cache", "*.log", "Thumbs.db", ".DS_Store", "desktop.ini", "kb.db", "kb.db-wal", "kb.db-shm"],
        "hidden": True,
        "max_depth": 8,
        "max_file_size_mb": 500,
    },
    "auto_watch": False,
    "categories": [],
}


def load_config():
    if not os.path.exists(KB_CONFIG):
        return DEFAULT_CONFIG.copy()
    try:
        with open(KB_CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        # 深度合并：新默认值补入旧配置
        merged = _deep_merge(DEFAULT_CONFIG.copy(), cfg)
        return merged
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG.copy()


def _deep_merge(base, override):
    for key, val in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(val, dict):
            base[key] = _deep_merge(base[key], val)
        else:
            base[key] = val
    return base


def save_config(cfg):
    os.makedirs(DB_DIR, exist_ok=True)
    with open(KB_CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ── 文件分类 ──────────────────────────────────────────

def classify_file(filename):
    ext = Path(filename).suffix.lower()
    if ext in DOC_EXTS:
        return 'doc'
    if ext in IMAGE_EXTS:
        return 'image'
    if ext in VIDEO_EXTS:
        return 'video'
    if ext in AUDIO_EXTS:
        return 'audio'
    if ext in CODE_EXTS:
        return 'code'
    if ext in ARCHIVE_EXTS:
        return 'archive'
    return 'other'


def auto_rules_tags(filename, rel_path, parent_label=''):
    tags = set()
    name = Path(filename).stem.lower()
    ext = Path(filename).suffix.lower()
    full_path = rel_path.lower()

    if ext in EXT_TAG_MAP:
        tags.add(EXT_TAG_MAP[ext])

    for kw, tag in PATH_TAG_MAP.items():
        if kw in name or kw in full_path:
            tags.add(tag)

    date_match = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', filename)
    if date_match:
        tags.add(f"{date_match.group(1)}年")

    season_match = re.search(r'(20\d{2})[qQ]([1-4])', filename)
    if season_match:
        tags.add(f"{season_match.group(1)}Q{season_match.group(2)}")

    if parent_label:
        tags.add(parent_label)

    return ','.join(sorted(tags)) if tags else ''


# ── 项目检测 ──────────────────────────────────────────

def detect_project(path):
    path = Path(path).expanduser().resolve()
    if not path.is_dir():
        return None, None

    for marker, ptype in PROJECT_MARKERS.items():
        if (path / marker).exists():
            readme_summary = ''
            for candidate in ['README.md', 'README.rst', 'README.txt', 'README', 'readme.md']:
                rp = path / candidate
                if rp.exists() and rp.is_file():
                    try:
                        with open(rp, 'r', encoding='utf-8', errors='ignore') as f:
                            readme_summary = f.read(800).strip()
                    except Exception:
                        pass
                    break

            if not readme_summary and (path / 'package.json').exists():
                try:
                    with open(path / 'package.json', 'r', encoding='utf-8') as f:
                        pj = json.load(f)
                        readme_summary = pj.get('description', '') or ''
                except Exception:
                    pass

            if not readme_summary and (path / 'pyproject.toml').exists():
                try:
                    with open(path / 'pyproject.toml', 'r', encoding='utf-8') as f:
                        for line in f:
                            m = re.match(r'description\s*=\s*"(.+)"', line.strip())
                            if m:
                                readme_summary = m.group(1)
                                break
                except Exception:
                    pass

            if not readme_summary and (path / 'Cargo.toml').exists():
                try:
                    with open(path / 'Cargo.toml', 'r', encoding='utf-8') as f:
                        for line in f:
                            m = re.match(r'description\s*=\s*"(.+)"', line.strip())
                            if m:
                                readme_summary = m.group(1)
                                break
                except Exception:
                    pass

            return ptype, readme_summary[:300] if readme_summary else ''

    return None, None


# ── 文件扫描引擎 ──────────────────────────────────────

def get_preview(abs_path, max_chars=500):
    ext = Path(abs_path).suffix.lower()
    if ext not in PREVIEW_EXTENSIONS:
        return ''
    try:
        with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read(max_chars).strip()
    except Exception:
        return ''


def scan_directory(directory, exclude_cfg, recursive=True):
    """扫描目录返回文件列表. 效 Everything 之 scandir 直读."""
    files = []
    p = Path(directory).expanduser().resolve()
    if not p.is_dir():
        return files

    max_size = exclude_cfg.get('max_file_size_mb', 500) * 1024 * 1024
    skip_hidden = exclude_cfg.get('hidden', True)
    exclude_patterns = exclude_cfg.get('patterns', [])
    max_depth = exclude_cfg.get('max_depth', 8)

    def _scandir_recurse(current_path, depth, rel_prefix):
        if depth > max_depth:
            return
        try:
            with os.scandir(current_path) as entries:
                subdirs = []
                for entry in entries:
                    name = entry.name

                    if skip_hidden and name.startswith('.'):
                        continue
                    if name in EXCLUDE_DIRS:
                        continue

                    # Check exclude patterns
                    matched = False
                    for pat in exclude_patterns:
                        if fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(name.lower(), pat.lower()):
                            matched = True
                            break
                    if matched:
                        continue

                    if entry.is_dir(follow_symlinks=False):
                        subdirs.append(entry)
                    elif entry.is_file(follow_symlinks=False):
                        try:
                            stat = entry.stat()
                            if stat.st_size > max_size:
                                continue
                            rel_path = f"{rel_prefix}{name}"
                            files.append({
                                'rel_path': rel_path,
                                'abs_path': str(Path(entry.path).resolve()),
                                'file_type': classify_file(name),
                                'extension': Path(name).suffix.lower(),
                                'size': stat.st_size,
                                'mtime': stat.st_mtime,
                                'name': name,
                            })
                        except (PermissionError, FileNotFoundError, OSError):
                            pass

                if recursive:
                    for sd in subdirs:
                        _scandir_recurse(sd.path, depth + 1, f"{rel_prefix}{sd.name}/")
        except (PermissionError, OSError):
            pass

    _scandir_recurse(str(p), 1, '')
    return files


def quick_diff(dir_id, dir_path, exclude_cfg):
    """mtime 快检: 对比磁盘与数据库, 返回增/改/删三列表."""
    conn = get_db()
    db_map = {}
    for row in conn.execute('SELECT abs_path, mtime, size FROM files WHERE dir_id=?', (dir_id,)):
        db_map[row['abs_path']] = {'mtime': row['mtime'], 'size': row['size']}

    current_entries = scan_directory(dir_path, exclude_cfg, recursive=True)
    current_map = {e['abs_path']: e for e in current_entries}

    new_files = []
    modified_files = []
    for path, entry in current_map.items():
        if path not in db_map:
            new_files.append(entry)
        elif db_map[path]['mtime'] != entry['mtime'] or db_map[path]['size'] != entry['size']:
            modified_files.append(entry)

    deleted_paths = [p for p in db_map if p not in current_map]
    conn.close()
    return new_files, modified_files, deleted_paths


# ── 帮助函数 ──────────────────────────────────────────

def _expand(path):
    return str(Path(path).expanduser().resolve())


def _relpath(abs_path, base):
    try:
        return str(Path(abs_path).relative_to(Path(base).expanduser().resolve()))
    except ValueError:
        return str(Path(abs_path).name)


# ── init ──────────────────────────────────────────────

def cmd_init(args):
    init_db()
    cfg = load_config()

    if not cfg['directories']:
        print("忆时 · 知识库初始化")
        print("=" * 50)
        print("\n请告知哪些目录需要纳入知识库：\n")
        defaults = [
            str(HOME / "Documents"),
            str(HOME / "Downloads"),
            str(HOME / "projects"),
        ]
        for i, d in enumerate(defaults):
            p = Path(d).expanduser()
            status = "✓ 存在" if p.exists() else "✗ 不存在"
            print(f"  [{i+1}] {d} ({status})")

        print("\n直接回车使用默认目录，或输入自定义目录路径（每行一个，空行结束）：")

        dirs = []
        for d in defaults:
            if Path(d).expanduser().exists():
                dirs.append({'path': str(Path(d).expanduser().resolve()), 'label': Path(d).name})

        if dirs:
            cfg['directories'] = dirs
            save_config(cfg)
            print(f"\n已注册 {len(dirs)} 个目录:")
            for d in dirs:
                print(f"  📁 {d['label']}: {d['path']}")
    else:
        print(f"知识库已初始化，注册 {len(cfg['directories'])} 个目录")
        for d in cfg['directories']:
            print(f"  📁 {d.get('label', '')}: {d['path']}")

    print(f"\n配置: {KB_CONFIG}")
    print(f"数据库: {KB_DB}")
    print("\n下一步: python3 knowledge_base.py index <目录>  建立索引")


# ── add / remove ──────────────────────────────────────

def cmd_add(args):
    init_db()
    cfg = load_config()
    target = _expand(args.path)
    label = args.label or Path(target).name

    for d in cfg['directories']:
        if _expand(d['path']) == target:
            print(f"目录已注册: {target}")
            return

    cfg['directories'].append({'path': target, 'label': label})
    save_config(cfg)

    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO directories (id, path, label) VALUES (?, ?, ?)",
        (str(uuid.uuid4()), target, label),
    )
    conn.commit()
    conn.close()
    print(f"已注册: 📁 {label} → {target}")


def cmd_remove(args):
    cfg = load_config()
    target = _expand(args.path)

    conn = get_db()
    row = conn.execute("SELECT id FROM directories WHERE path=?", (target,)).fetchone()
    if row:
        conn.execute("DELETE FROM files WHERE dir_id=?", (row['id'],))
        conn.execute("DELETE FROM directories WHERE id=?", (row['id'],))
        conn.commit()
    conn.close()

    cfg['directories'] = [d for d in cfg['directories'] if _expand(d['path']) != target]
    save_config(cfg)
    print(f"已移除: {target}")


# ── index ─────────────────────────────────────────────

def cmd_index(args):
    init_db()
    cfg = load_config()
    target = _expand(args.path)

    if not Path(target).is_dir():
        print(f"错误: 目录不存在 - {target}")
        sys.exit(1)

    conn = get_db()
    dir_row = conn.execute("SELECT * FROM directories WHERE path=?", (target,)).fetchone()

    if not dir_row:
        dir_id = str(uuid.uuid4())
        label = Path(target).name
        conn.execute(
            "INSERT INTO directories (id, path, label, indexed_at) VALUES (?, ?, ?, ?)",
            (dir_id, target, label, _now().isoformat()),
        )
        cfg['directories'].append({'path': target, 'label': label})
        save_config(cfg)
    else:
        dir_id = dir_row['id']

    is_project = args.project
    is_quick = args.quick
    project_type = None
    project_summary = ''

    # ── 项目检测 ──
    if is_project:
        project_type, project_summary = detect_project(target)
        if project_type:
            conn.execute(
                "UPDATE directories SET is_project=1, summary=?, scan_depth=0 WHERE id=?",
                (f"[{project_type}] {project_summary}" if project_summary else f"[{project_type}]", dir_id),
            )
        else:
            print(f"  未检测到项目标志，按普通目录索引")

    now = _now()
    exclude_cfg = cfg.get('exclude', DEFAULT_CONFIG['exclude'])

    # ── 快速模式 ──
    if is_quick:
        new_files, modified_files, deleted_paths = quick_diff(dir_id, target, exclude_cfg)
        changed = False

        if deleted_paths:
            for dp in deleted_paths:
                conn.execute("DELETE FROM files WHERE abs_path=?", (dp,))
            changed = True

        for entry in modified_files:
            conn.execute(
                "UPDATE files SET size=?, mtime=?, updated_at=? WHERE abs_path=?",
                (entry['size'], entry['mtime'], now.isoformat(), entry['abs_path']),
            )
            changed = True

        for entry in new_files:
            fid = str(uuid.uuid4())
            base_rel = _relpath(entry['abs_path'], target)
            rules_tags = auto_rules_tags(entry['name'], base_rel, Path(target).name)
            conn.execute(
                """INSERT OR REPLACE INTO files
                   (id, dir_id, rel_path, abs_path, file_type, extension, size, mtime,
                    rules_tags, annotated, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)""",
                (fid, dir_id, base_rel, entry['abs_path'], entry['file_type'],
                 entry['extension'], entry['size'], entry['mtime'],
                 rules_tags, now.isoformat(), now.isoformat()),
            )
            changed = True

        if changed:
            conn.execute("UPDATE directories SET indexed_at=? WHERE id=?", (now.isoformat(), dir_id))

        total = conn.execute("SELECT COUNT(*) as cnt FROM files WHERE dir_id=?", (dir_id,)).fetchone()['cnt']
        conn.commit()
        conn.close()
        print(f"快速更新: {target}")
        print(f"  新增: {len(new_files)}  修改: {len(modified_files)}  删除: {len(deleted_paths)}  总计: {total}")
        return

    # ── 全量索引 ──
    entries = scan_directory(target, exclude_cfg, recursive=not is_project)

    # 清除旧文件
    conn.execute("DELETE FROM files WHERE dir_id=?", (dir_id,))

    count = 0
    for entry in entries:
        fid = str(uuid.uuid4())
        base_rel = _relpath(entry['abs_path'], target)
        rules_tags = auto_rules_tags(entry['name'], base_rel, Path(target).name)
        conn.execute(
            """INSERT INTO files
               (id, dir_id, rel_path, abs_path, file_type, extension, size, mtime,
                rules_tags, annotated, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)""",
            (fid, dir_id, base_rel, entry['abs_path'], entry['file_type'],
             entry['extension'], entry['size'], entry['mtime'],
             rules_tags, now.isoformat(), now.isoformat()),
        )
        count += 1

    conn.execute("UPDATE directories SET indexed_at=?, last_seen=?, is_online=1 WHERE id=?",
                 (now.isoformat(), now.isoformat(), dir_id))

    # 记录快照
    snap_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO scan_snapshots (id, dir_id, scanned_at, total, new_files, modified, deleted) VALUES (?, ?, ?, ?, ?, 0, 0)",
        (snap_id, dir_id, now.isoformat(), count, count),
    )

    conn.commit()
    conn.close()

    _touch_dir(dir_id)

    prefix = "🏗" if is_project and project_type else "📁"
    print(f"{prefix} 索引完成: {target}")
    print(f"  文件数: {count}")
    if project_type:
        print(f"  项目类型: {project_type}")
        if project_summary:
            print(f"  摘要: {project_summary[:120]}..." if len(project_summary) > 120 else f"  摘要: {project_summary}")
    print(f"  规则标注: 已自动生成标签")


def _touch_dir(dir_id):
    conn = get_db()
    conn.execute(
        "UPDATE directories SET touch_count=touch_count+1, last_seen=? WHERE id=?",
        (_now().isoformat(), dir_id),
    )
    conn.commit()
    conn.close()


# ── find ──────────────────────────────────────────────

def _parse_date_filter(date_str):
    """解析日期过滤: today, thisweek, lastmonth, 2026-01-01..2026-05-18, >2026-01-01"""
    now = _now()
    date_constants = {
        'today': (now.replace(hour=0, minute=0, second=0, microsecond=0),
                   now.replace(hour=23, minute=59, second=59, microsecond=999999)),
        'yesterday': (now - timedelta(days=1), now - timedelta(days=1)),
        'thisweek': (now - timedelta(days=now.weekday()), now),
        'lastweek': (now - timedelta(days=now.weekday() + 7), now - timedelta(days=now.weekday())),
        'thismonth': (now.replace(day=1), now),
        'lastmonth': ((now.replace(day=1) - timedelta(days=1)).replace(day=1),
                       now.replace(day=1) - timedelta(days=1)),
        'thisyear': (now.replace(month=1, day=1), now),
    }

    date_str = date_str.strip().lower().replace(' ', '')
    if date_str in date_constants:
        a, b = date_constants[date_str]
        return a.timestamp(), b.timestamp()

    if '..' in date_str:
        parts = date_str.split('..')
        try:
            a = datetime.fromisoformat(parts[0]) if parts[0] else datetime(1970, 1, 1)
            b = datetime.fromisoformat(parts[1]) if parts[1] else now
            return a.timestamp(), b.timestamp()
        except (ValueError, TypeError):
            return None, None

    if date_str.startswith('>'):
        try:
            return datetime.fromisoformat(date_str[1:]).timestamp(), now.timestamp()
        except (ValueError, TypeError):
            return None, None
    if date_str.startswith('<'):
        try:
            return 0, datetime.fromisoformat(date_str[1:]).timestamp()
        except (ValueError, TypeError):
            return None, None

    return None, None


def _parse_size_filter(size_str):
    """解析大小过滤: >1mb, <500kb, 100kb..10mb"""
    units = {'b': 1, 'kb': 1024, 'mb': 1024**2, 'gb': 1024**3}
    size_str = size_str.strip().lower().replace(' ', '')

    def _to_bytes(s):
        for u, mult in sorted(units.items(), key=lambda x: -len(x[0])):
            if s.endswith(u):
                val = float(s[:-len(u)])
                return int(val * mult)
        return int(s) if s.isdigit() else None

    if '..' in size_str:
        parts = size_str.split('..')
        a = _to_bytes(parts[0]) if parts[0] else 0
        b = _to_bytes(parts[1]) if parts[1] else None
        return a, b

    if size_str.startswith('>'):
        return _to_bytes(size_str[1:]), None
    if size_str.startswith('<'):
        return None, _to_bytes(size_str[1:])

    return None, None


def cmd_find(args):
    init_db()
    conn = get_db()
    query = args.query.strip() if args.query else ''

    conditions = []
    params = []

    if query:
        # 支持 * 通配转 SQL LIKE
        if '*' in query or '?' in query:
            like_pat = query.replace('*', '%').replace('?', '_')
            conditions.append("(rel_path LIKE ? OR abs_path LIKE ? OR rules_tags LIKE ? OR ai_tags LIKE ?)")
            params.extend([f"%{like_pat}%", f"%{like_pat}%", f"%{like_pat}%", f"%{like_pat}%"])
        else:
            words = query.split()
            for w in words:
                wc = f"%{w}%"
                conditions.append("(rel_path LIKE ? OR abs_path LIKE ? OR rules_tags LIKE ? OR ai_tags LIKE ?)")
                params.extend([wc, wc, wc, wc])

    if args.ext:
        conditions.append("extension=?")
        params.append(args.ext.lower() if args.ext.startswith('.') else f".{args.ext.lower()}")

    if args.type:
        conditions.append("file_type=?")
        params.append(args.type.lower())

    if args.mtime:
        t_from, t_to = _parse_date_filter(args.mtime)
        if t_from is not None and t_to is not None:
            conditions.append("mtime >= ? AND mtime <= ?")
            params.extend([t_from, t_to])

    if args.size:
        s_from, s_to = _parse_size_filter(args.size)
        if s_from is not None:
            conditions.append("size >= ?")
            params.append(s_from)
        if s_to is not None:
            conditions.append("size <= ?")
            params.append(s_to)

    if args.dir:
        dir_exp = _expand(args.dir)
        conditions.append("(abs_path LIKE ? OR rel_path LIKE ?)")
        params.append(f"%{dir_exp}%")
        params.append(f"%{args.dir}%")

    where = " AND ".join(conditions) if conditions else "1=1"
    limit = args.limit or 50

    sql = f"SELECT * FROM files WHERE {where} ORDER BY mtime DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    if not rows:
        print(f"未找到匹配文件 (查询: '{query}')")
        return

    total = len(rows)
    print(f"找到 {total} 个文件" + (f" (查询: '{query}')" if query else ''))
    print("=" * 60)

    type_emoji = {
        'doc': '📄', 'image': '🖼', 'video': '🎬', 'audio': '🎵',
        'code': '💻', 'archive': '📦', 'other': '📎',
    }

    for idx, row in enumerate(rows, 1):
        emoji = type_emoji.get(row['file_type'], '📎')
        size_kb = row['size'] / 1024 if row['size'] else 0
        size_str = f"{size_kb:.1f}KB" if size_kb < 1024 else f"{size_kb/1024:.1f}MB"
        mtime_str = datetime.fromtimestamp(row['mtime']).strftime('%Y-%m-%d') if row['mtime'] else '未知'
        ann_mark = ' ✨' if row['annotated'] else ''
        tags = row['ai_tags'] or row['rules_tags'] or ''

        print(f"\n#{idx} {emoji} [{row['file_type'].upper()}]{ann_mark}")
        print(f"   路径: {row['abs_path']}")
        print(f"   大小: {size_str}  |  修改: {mtime_str}")
        if tags:
            print(f"   标签: {tags}")
        if row['ai_summary']:
            sm = row['ai_summary'][:120]
            print(f"   摘要: {sm}{'...' if len(row['ai_summary']) > 120 else ''}")
        print(f"   ID: {row['id']}")

    print(f"\n{'=' * 60}")

    # 输出 JSON 供 AI 解析
    if args.json:
        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'name': Path(row['abs_path']).name,
                'path': row['abs_path'],
                'type': row['file_type'],
                'ext': row['extension'],
                'size': row['size'],
                'mtime': row['mtime'],
                'tags': row['ai_tags'] or row['rules_tags'],
                'summary': row['ai_summary'],
                'annotated': bool(row['annotated']),
            })
        print("\n--- JSON ---")
        print(json.dumps(results, ensure_ascii=False, indent=2))


# ── open ──────────────────────────────────────────────

def cmd_open(args):
    target = args.target

    # 先尝试作为 file_id 查找
    conn = get_db()
    row = conn.execute("SELECT abs_path FROM files WHERE id=?", (target,)).fetchone()
    conn.close()

    if row:
        path = row['abs_path']
    else:
        path = _expand(target)

    if not os.path.exists(path):
        print(f"路径不存在: {path}")
        sys.exit(1)

    path_obj = Path(path)
    if path_obj.is_file():
        open_path = str(path_obj.parent)
    else:
        open_path = str(path_obj)

    opener = _get_file_manager_cmd(open_path)
    print(f"打开: {open_path}")
    subprocess.run(opener, shell=False)


def _get_file_manager_cmd(path):
    if sys.platform == 'linux':
        return ['xdg-open', path]
    elif sys.platform == 'darwin':
        return ['open', path]
    elif sys.platform == 'win32':
        return ['explorer', '/select,', str(Path(path))]
    return ['xdg-open', path]


# ── annotate ──────────────────────────────────────────

def cmd_annotate(args):
    init_db()
    conn = get_db()
    now = _now().isoformat()

    # 查看待标注列表
    if args.pending:
        limit = args.limit or 20
        rows = conn.execute(
            "SELECT * FROM files WHERE annotated=0 ORDER BY mtime DESC LIMIT ?",
            (limit,),
        ).fetchall()

        if not rows:
            print("所有文件已标注")
            conn.close()
            return

        result = []
        for row in rows:
            item = {
                'id': row['id'],
                'name': Path(row['abs_path']).name,
                'path': row['abs_path'],
                'type': row['file_type'],
                'ext': row['extension'],
                'size': row['size'],
                'rules_tags': row['rules_tags'],
            }
            preview = get_preview(row['abs_path'], 300)
            if preview:
                item['preview'] = preview
            result.append(item)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        conn.close()
        return

    # 标注指定文件
    if args.file:
        tags = args.tags or ''
        summary = args.summary or ''
        if not tags and not summary:
            print("请提供 --tags 或 --summary")
            conn.close()
            sys.exit(1)

        conn.execute(
            "UPDATE files SET ai_tags=?, ai_summary=?, annotated=1, updated_at=? WHERE id=?",
            (tags, summary, now, args.file),
        )
        conn.commit()
        conn.close()
        print(f"已标注: {args.file}")
        if tags:
            print(f"  标签: {tags}")
        if summary:
            print(f"  摘要: {summary}")
        return

    # 批量标注某目录下未标注文件 (仅列出，AI 需逐文件标注)
    if args.path:
        target = _expand(args.path)
        dir_row = conn.execute("SELECT id FROM directories WHERE path=?", (target,)).fetchone()
        if not dir_row:
            print(f"目录未注册: {target}")
            conn.close()
            sys.exit(1)

        rows = conn.execute(
            "SELECT * FROM files WHERE dir_id=? AND annotated=0 ORDER BY mtime DESC LIMIT ?",
            (dir_row['id'], args.limit or 10),
        ).fetchall()

        if not rows:
            print(f"该目录下所有文件已标注")
            conn.close()
            return

        result = []
        for row in rows:
            item = {
                'id': row['id'],
                'name': Path(row['abs_path']).name,
                'path': row['abs_path'],
                'type': row['file_type'],
                'ext': row['extension'],
                'size': row['size'],
                'rules_tags': row['rules_tags'],
            }
            preview = get_preview(row['abs_path'], 300)
            if preview:
                item['preview'] = preview
            result.append(item)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        conn.close()
        return

    print("用法: annotate --pending | --file <id> --tags '...' --summary '...' | <path>")


# ── category ──────────────────────────────────────────

def cmd_category(args):
    init_db()
    conn = get_db()
    now = _now().isoformat()

    if args.subcmd == 'list':
        rows = conn.execute("SELECT * FROM categories ORDER BY created_at DESC").fetchall()
        if not rows:
            print("暂无分类")
            conn.close()
            return
        for row in rows:
            print(f"📂 {row['name']}")
            print(f"   描述: {row['description'] or '无'}")
            print(f"   查询: {row['query_json'][:120]}")
            print(f"   ID: {row['id']}")
            print()

    elif args.subcmd == 'add':
        if not args.name:
            print("请提供分类名称 --name")
            conn.close()
            sys.exit(1)
        qj = args.query or '{}'
        try:
            json.loads(qj)
        except json.JSONDecodeError:
            print("query 须为合法 JSON")
            conn.close()
            sys.exit(1)

        cid = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO categories (id, name, query_json, description, created_at) VALUES (?, ?, ?, ?, ?)",
            (cid, args.name, qj, args.desc or '', now),
        )
        conn.commit()
        print(f"已创建分类: {args.name}")

    elif args.subcmd == 'show':
        if not args.name:
            print("请提供分类名称 --name")
            conn.close()
            sys.exit(1)

        row = conn.execute("SELECT * FROM categories WHERE name=?", (args.name,)).fetchone()
        if not row:
            print(f"分类不存在: {args.name}")
            conn.close()
            return

        try:
            q = json.loads(row['query_json'])
        except json.JSONDecodeError:
            q = {}

        conditions = []
        params = []
        if 'ext' in q:
            exts = q['ext'] if isinstance(q['ext'], list) else [q['ext']]
            placeholders = ','.join(['?'] * len(exts))
            conditions.append(f"extension IN ({placeholders})")
            params.extend(exts)
        if 'tags' in q:
            tags = q['tags'] if isinstance(q['tags'], list) else [q['tags']]
            for t in tags:
                conditions.append("(ai_tags LIKE ? OR rules_tags LIKE ?)")
                params.extend([f"%{t}%", f"%{t}%"])
        if 'is_project' in q:
            conditions.append("dir_id IN (SELECT id FROM directories WHERE is_project=1)")

        where = " AND ".join(conditions) if conditions else "1=1"
        file_rows = conn.execute(
            f"SELECT * FROM files WHERE {where} ORDER BY mtime DESC LIMIT 50",
            params,
        ).fetchall()

        print(f"📂 {row['name']}")
        print(f"   描述: {row['description'] or '无'}")
        print(f"   文件数: {len(file_rows)}")
        print("-" * 40)
        for fr in file_rows:
            name = Path(fr['abs_path']).name
            print(f"   {name}")
            print(f"   → {fr['abs_path']}")

    elif args.subcmd == 'remove':
        if not args.name:
            print("请提供分类名称 --name")
            conn.close()
            sys.exit(1)
        conn.execute("DELETE FROM categories WHERE name=?", (args.name,))
        conn.commit()
        print(f"已删除分类: {args.name}")

    conn.close()


# ── relate / related ──────────────────────────────────

def cmd_relate(args):
    init_db()
    conn = get_db()
    now = _now().isoformat()

    rid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO file_relations (id, source_id, target_id, rel_type, confidence, reason, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (rid, args.source, args.target, args.type, args.confidence or 0.5, args.reason or '', now),
    )
    conn.commit()
    conn.close()
    print(f"已建立关联: {args.source} ─{args.type}→ {args.target}")


def cmd_related(args):
    init_db()
    conn = get_db()

    rows = conn.execute(
        """SELECT fr.*, f1.abs_path as source_path, f2.abs_path as target_path
           FROM file_relations fr
           LEFT JOIN files f1 ON fr.source_id=f1.id
           LEFT JOIN files f2 ON fr.target_id=f2.id
           WHERE fr.source_id=? OR fr.target_id=?
           ORDER BY fr.confidence DESC""",
        (args.id, args.id),
    ).fetchall()

    if not rows:
        print("无关联文件")
        conn.close()
        return

    print(f"关联文件 (ID: {args.id})")
    print("=" * 50)
    for row in rows:
        direction = '→' if row['source_id'] == args.id else '←'
        other_path = row['target_path'] if row['source_id'] == args.id else row['source_path']
        print(f"  {direction} [{row['rel_type']}] {Path(other_path).name if other_path else '未知'}")
        if row['reason']:
            print(f"    理由: {row['reason']}")
        if other_path:
            print(f"    路径: {other_path}")
        print()

    conn.close()


# ── search (统一搜索) ─────────────────────────────────

def cmd_search(args):
    init_db()
    query = args.query
    limit = args.limit or 10

    # ── 1. 搜 SQLite 文件 ──
    conn = get_db()
    wc = f"%{query}%"
    file_rows = conn.execute(
        """SELECT * FROM files
           WHERE rel_path LIKE ? OR abs_path LIKE ?
              OR rules_tags LIKE ? OR ai_tags LIKE ?
              OR ai_summary LIKE ?
           ORDER BY mtime DESC LIMIT ?""",
        (wc, wc, wc, wc, wc, limit * 2),
    ).fetchall()
    conn.close()

    # ── 2. 搜 ChromaDB 记忆 ──
    memory_results = []
    try:
        result = subprocess.run(
            [sys.executable, MEMORY_CORE_PY, 'recall', query, '--limit', str(limit)],
            capture_output=True, text=True, timeout=30,
            env={**os.environ, 'YISHI_DATA_DIR': DB_DIR},
        )
        if result.returncode == 0:
            memory_results = _parse_memory_output(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass

    # ── 3. 融合排序 ──
    scored = []

    # 文件得分
    for row in file_rows:
        name = Path(row['abs_path']).name.lower()
        tag_text = (row['ai_tags'] + ' ' + row['rules_tags']).lower()
        path_text = row['abs_path'].lower()
        ql = query.lower()

        path_score = 0.0
        if ql in name: path_score = 0.9
        elif ql in path_text: path_score = 0.6
        tag_score = 0.3 if any(w in tag_text for w in ql.split()) else 0.0
        recency = 0.0
        if row['mtime']:
            days = (_now() - datetime.fromtimestamp(row['mtime'])).days
            recency = math.exp(-math.log(2) * days / 90.0)

        score = 0.4 * path_score + 0.30 * tag_score + 0.30 * recency
        scored.append({
            'source': 'file',
            'score': round(score, 3),
            'data': dict(row),
            'name': Path(row['abs_path']).name,
            'path': row['abs_path'],
        })

    # 记忆得分
    for mem in memory_results:
        scored.append({
            'source': 'memory',
            'score': mem.get('score', 0.5),
            'data': mem,
            'content': mem.get('content', ''),
            'type': mem.get('type', 'context'),
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    scored = scored[:limit]

    if not scored:
        print(f"未找到匹配 (查询: '{query}')")
        return

    print(f"统一搜索: '{query}'  →  共 {len(scored)} 条")
    print("=" * 60)

    type_emoji = {
        'doc': '📄', 'image': '🖼', 'video': '🎬', 'audio': '🎵',
        'code': '💻', 'archive': '📦', 'other': '📎',
    }

    for idx, item in enumerate(scored, 1):
        if item['source'] == 'file':
            row = item['data']
            emoji = type_emoji.get(row['file_type'], '📎')
            mtime_str = datetime.fromtimestamp(row['mtime']).strftime('%Y-%m-%d') if row['mtime'] else ''
            tags = row['ai_tags'] or row['rules_tags'] or ''
            ann_mark = ' ✨' if row['annotated'] else ''
            print(f"\n#{idx} [文件]{ann_mark} {emoji} [{row['file_type'].upper()}]")
            print(f"   路径: {row['abs_path']}")
            print(f"   修改: {mtime_str}")
            if tags:
                print(f"   标签: {tags}")
            if row['ai_summary']:
                sm = row['ai_summary'][:120]
                print(f"   摘要: {sm}{'...' if len(row['ai_summary']) > 120 else ''}")
            print(f"   ID: {row['id']}")
        else:
            emoji_map = {"extreme": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
            e_emoji = emoji_map.get(item.get('type', 'medium'), '⚪')
            print(f"\n#{idx} [记忆] {e_emoji} [{item.get('type', 'context').upper()}]")
            print(f"   得分: {item['score']}")
            print(f"   内容: {item.get('content', '')}")

    print(f"\n{'=' * 60}")


def _parse_memory_output(output):
    """解析 memory_core.py recall 的文本输出"""
    results = []
    lines = output.split('\n')
    current = {}
    for line in lines:
        line = line.strip()
        if line.startswith('#') and not line.startswith('##'):
            if current and 'content' in current:
                results.append(current)
            current = {}
            # #1 🟡 [TASK]
            m = re.search(r'\[(\w+)\]', line)
            if m:
                current['type'] = m.group(1).lower()
        elif line.startswith('   得分:'):
            m = re.search(r'([\d.]+)', line)
            if m:
                current['score'] = float(m.group(1))
        elif line.startswith('   内容:'):
            current['content'] = line[7:].strip()
    if current and 'content' in current:
        results.append(current)
    return results


# ── status ────────────────────────────────────────────

def cmd_status(args):
    init_db()
    conn = get_db()

    if args.path:
        target = _expand(args.path)
        dir_row = conn.execute("SELECT * FROM directories WHERE path=?", (target,)).fetchone()
        if not dir_row:
            print(f"目录未注册: {target}")
            conn.close()
            return

        file_rows = conn.execute(
            "SELECT file_type, COUNT(*) as cnt FROM files WHERE dir_id=? GROUP BY file_type",
            (dir_row['id'],),
        ).fetchall()

        print(f"📁 {dir_row['label'] or Path(target).name}")
        print(f"   路径: {dir_row['path']}")
        print(f"   项目: {'是' if dir_row['is_project'] else '否'}")
        if dir_row['summary']:
            print(f"   摘要: {dir_row['summary']}")
        print(f"   提及: {dir_row['touch_count']} 次")
        print(f"   索引: {dir_row['indexed_at'] or '未索引'}")
        print(f"   文件分布:")
        total = 0
        for fr in file_rows:
            print(f"     {fr['file_type']}: {fr['cnt']}")
            total += fr['cnt']
        print(f"     总计: {total}")

        annotated = conn.execute(
            "SELECT COUNT(*) as cnt FROM files WHERE dir_id=? AND annotated=1",
            (dir_row['id'],),
        ).fetchone()
        print(f"   已AI标注: {annotated['cnt']}/{total}")

    else:
        dir_rows = conn.execute("SELECT * FROM directories ORDER BY indexed_at DESC").fetchall()
        total_files = conn.execute("SELECT COUNT(*) as cnt FROM files").fetchone()['cnt']
        total_relations = conn.execute("SELECT COUNT(*) as cnt FROM file_relations").fetchone()['cnt']
        total_categories = conn.execute("SELECT COUNT(*) as cnt FROM categories").fetchone()['cnt']
        total_annotated = conn.execute("SELECT COUNT(*) as cnt FROM files WHERE annotated=1").fetchone()['cnt']

        print("忆时 · 知识库状态")
        print("=" * 50)
        print(f"  注册目录: {len(dir_rows)}")
        print(f"  文件总数: {total_files}")
        print(f"  已AI标注: {total_annotated}")
        print(f"  关联关系: {total_relations}")
        print(f"  虚拟分类: {total_categories}")
        print()

        for d in dir_rows:
            fcnt = conn.execute("SELECT COUNT(*) as cnt FROM files WHERE dir_id=?", (d['id'],)).fetchone()['cnt']
            p_mark = '🏗' if d['is_project'] else '📁'
            online = '' if d['is_online'] else ' [离线]'
            touch = f" 提及{d['touch_count']}次" if d['touch_count'] > 0 else ''
            print(f"  {p_mark} {d['label']}{online} → {d['path']} ({fcnt} 文件){touch}")

    conn.close()


# ── watch ─────────────────────────────────────────────

def cmd_watch(args):
    """inotify/FSEvents 实时监听 (需 pip install watchdog)"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("请安装 watchdog: pip install watchdog")
        sys.exit(1)

    init_db()
    cfg = load_config()
    exclude_cfg = cfg.get('exclude', DEFAULT_CONFIG['exclude'])

    print("启动文件监听...")
    print(f"监听 {len(cfg['directories'])} 个目录 (Ctrl+C 停止)")

    class KBHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                self._handle(event.src_path, 'created')
        def on_modified(self, event):
            if not event.is_directory:
                self._handle(event.src_path, 'modified')
        def on_deleted(self, event):
            if not event.is_directory:
                self._handle(event.src_path, 'deleted')
        def on_moved(self, event):
            if not event.is_directory:
                self._handle(event.dest_path, 'moved', old_path=event.src_path)

        def _handle(self, path, action, old_path=None):
            name = Path(path).name
            if name.startswith('.'):
                return
            for pat in exclude_cfg.get('patterns', []):
                if fnmatch.fnmatch(name, pat):
                    return
            print(f"  {'🆕' if action == 'created' else '✏' if action == 'modified' else '🗑' if action == 'deleted' else '↪'} {action}: {path}")

    observer = Observer()
    for d in cfg['directories']:
        p = Path(d['path']).expanduser().resolve()
        if p.exists():
            observer.schedule(KBHandler(), str(p), recursive=True)
            print(f"  监听: {p}")

    observer.start()
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n监听已停止")
    observer.join()


# ── CLI ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="忆时 Knowledge Base - 个人知识库引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="初始化知识库")
    p_init.set_defaults(func=cmd_init)

    # add
    p_add = sub.add_parser("add", help="注册目录")
    p_add.add_argument("path", help="目录路径")
    p_add.add_argument("--label", help="标签")
    p_add.set_defaults(func=cmd_add)

    # remove
    p_remove = sub.add_parser("remove", help="移除注册目录")
    p_remove.add_argument("path", help="目录路径")
    p_remove.set_defaults(func=cmd_remove)

    # index
    p_index = sub.add_parser("index", help="建立/更新索引")
    p_index.add_argument("path", help="目录路径")
    p_index.add_argument("--quick", action="store_true", help="快速 mtime 增量更新")
    p_index.add_argument("--project", action="store_true", help="项目识别模式")
    p_index.set_defaults(func=cmd_index)

    # find
    p_find = sub.add_parser("find", help="搜索文件")
    p_find.add_argument("query", nargs="?", default="", help="搜索关键词")
    p_find.add_argument("--ext", help="扩展名过滤")
    p_find.add_argument("--type", choices=["doc", "image", "video", "audio", "code", "archive", "other"], help="文件类型")
    p_find.add_argument("--mtime", help="修改时间 (today/thisweek/lastmonth/yyyy-mm-dd..yyyy-mm-dd)")
    p_find.add_argument("--size", help="文件大小 (>1mb/<500kb/100kb..10mb)")
    p_find.add_argument("--dir", help="限定目录")
    p_find.add_argument("--limit", type=int, default=50, help="返回数量上限")
    p_find.add_argument("--json", action="store_true", help="JSON 输出")
    p_find.set_defaults(func=cmd_find)

    # open
    p_open = sub.add_parser("open", help="打开文件管理器定位")
    p_open.add_argument("target", help="文件ID 或目录路径")
    p_open.set_defaults(func=cmd_open)

    # annotate
    p_annot = sub.add_parser("annotate", help="AI 标注管理")
    p_annot.add_argument("path", nargs="?", help="目录路径 (列出该目录下待标注文件)")
    p_annot.add_argument("--pending", action="store_true", help="列出所有待标注文件")
    p_annot.add_argument("--file", help="标注指定文件ID")
    p_annot.add_argument("--tags", help="AI 生成的标签")
    p_annot.add_argument("--summary", help="AI 生成的摘要")
    p_annot.add_argument("--limit", type=int, default=20, help="返回数量")
    p_annot.set_defaults(func=cmd_annotate)

    # category
    p_cat = sub.add_parser("category", help="虚拟分类管理")
    p_cat.add_argument("subcmd", choices=["list", "add", "show", "remove"], help="子命令")
    p_cat.add_argument("--name", help="分类名称")
    p_cat.add_argument("--query", help="查询条件 (JSON)")
    p_cat.add_argument("--desc", help="分类描述")
    p_cat.set_defaults(func=cmd_category)

    # relate
    p_rel = sub.add_parser("relate", help="建立文件关联")
    p_rel.add_argument("source", help="源文件ID")
    p_rel.add_argument("target", help="目标文件ID")
    p_rel.add_argument("--type", required=True, choices=["implements", "references", "depends_on", "related", "derived_from"], help="关联类型")
    p_rel.add_argument("--confidence", type=float, default=0.5)
    p_rel.add_argument("--reason", help="关联理由")
    p_rel.set_defaults(func=cmd_relate)

    # related
    p_related = sub.add_parser("related", help="查看文件关联")
    p_related.add_argument("id", help="文件ID")
    p_related.set_defaults(func=cmd_related)

    # search
    p_search = sub.add_parser("search", help="统一搜索 (记忆+文件)")
    p_search.add_argument("query", help="搜索关键词")
    p_search.add_argument("--limit", type=int, default=10, help="返回数量上限")
    p_search.set_defaults(func=cmd_search)

    # status
    p_st = sub.add_parser("status", help="知识库状态")
    p_st.add_argument("path", nargs="?", help="指定目录")
    p_st.set_defaults(func=cmd_status)

    # watch
    p_watch = sub.add_parser("watch", help="实时文件监听 (需 watchdog)")
    p_watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
