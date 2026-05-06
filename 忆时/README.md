# 忆时 - 记忆胶囊系统

🎋 模拟人类记忆检索机制的 AI 记忆系统。OpenCode 技能。

## 下载

```bash
# 方式一：git clone
git clone git@github.com:fslong520/aiSkill.git --depth 1
# 然后将 忆时/ 目录复制到 skills/ 下

# 方式二：直接复制本目录到 OpenCode skills 目录
cp -r 忆时 ~/.config/opencode/skills/

# 方式三：仅获取核心文件（模型首次使用自动下载）
cp -r 忆时/{scripts,modules,SKILL.md,yishi-instructions.md} ~/.config/opencode/skills/忆时/
```

## 功能

- **类人检索**: 语义40% + 近因20% + 情绪15% + 频率25%
- **渐进式回忆**: 先抛最相关的1-2条，用户追问再深入
- **情绪锚定**: 高情绪记忆权重更高，不易遗忘
- **记忆涌现**: 话题转换时发现隐藏关联
- **时间胶囊**: 封存记忆，设定解锁日期

## 快速开始

```bash
# 1. 安装依赖
pip install chromadb

# 2. 初始化
python3 scripts/memory_core.py init

# 3. 存储记忆
python3 scripts/memory_core.py store "记忆内容" --type context --emotion medium --keywords "标签"

# 4. 检索记忆
python3 scripts/memory_core.py recall "查询内容" --limit 5 --expand
```

## 模型安装

首次使用 `init` 或 `recall` 时自动安装 embedding 模型:
1. 有离线包 `models/onnx/onnx.tar.gz` → 自动解压
2. 无离线包 → 从 Chroma S3 自动下载

## 目录结构

```
忆时/
├── SKILL.md              # 技能定义
├── yishi-instructions.md # 外挂提示词
├── modules/              # 流程模块
├── scripts/
│   └── memory_core.py    # 核心引擎
├── models/
│   └── onnx/             # embedding 模型 (首次使用自动生成)
├── data/                 # ChromaDB 数据 (运行时生成)
│   └── .gitkeep
├── references/           # API 参考
├── venv/                 # Python 虚拟环境
├── .gitignore
├── .gitattributes
└── README.md
```

## 配置

编辑 `~/.config/opencode/opencode.json`:

```json
{
  "instructions": [
    "~/.config/opencode/skills/忆时/yishi-instructions.md"
  ]
}
```
