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
- **混合检索**: BM25 关键词 + 向量语义双路 RRF 融合（k=60），人名/专名/代码标识符更准；embedding 失败自动降级关键词
- **去重合并**: 存储时相似>90% 自动合并，85%~90% 警告提示，--force 强存
- **场景分组**: --scene 归组 + 活动时间段（--activity-start/--activity-end）
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
python3 scripts/memory_core.py store "记忆内容" --type context --emotion medium --keywords "标签" --scene "场景名"

# 4. 检索记忆
python3 scripts/memory_core.py recall "查询内容" --limit 5 --expand --no-embed
```

## 模型安装

使用 **bge-base-zh-v1.5**（BAAI 中文语义模型，768 维）——中文记忆检索质量远超英文模型 MiniLM。引擎检测 `~/.local/share/opencode/忆时/models/bge-base-zh-v1.5/`，缺失即报错退出，**无回退**（MiniLM 384 维与 bge 768 维数据不兼容，曾致维度冲突）。

bge 安装：自 hf-mirror 下载 Xenova/bge-base-zh-v1.5 之 `onnx/model.onnx` 与 tokenizer 文件至上述目录（详见 modules/08-setup.md）。

## 目录结构

```
忆时/
├── SKILL.md              # 技能定义
├── yishi-instructions.md # 外挂提示词
├── modules/              # 流程模块
├── scripts/
│   └── memory_core.py    # 核心引擎
├── models/                 # （已弃用——运行时 bge 模型在 LOCAL_BASE）
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
