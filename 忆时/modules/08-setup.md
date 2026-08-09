# 模块 08 - 模型安装、配置与参考

**何时读**：首次安装/切换 embedding 模型、维度重建、配置 opencode.json 外挂提示词、排查"AI不自动检索"问题时。日常无此场景不读。

## 模型安装

本技能使用 **bge-base-zh-v1.5**（BAAI 中文语义模型，768 维，~400MB）——中文记忆检索质量远超英文模型 MiniLM。引擎检测 `~/.local/share/opencode/忆时/models/bge-base-zh-v1.5/onnx/model.onnx`，缺失即报错退出，**无回退**（MiniLM 384 维与 bge 768 维数据不兼容，曾致维度冲突）。

**bge-base-zh-v1.5 安装**（模型放运行时目录，技能更新不覆盖）：

```bash
mkdir -p ~/.local/share/opencode/忆时/models/bge-base-zh-v1.5/onnx
# 自 hf-mirror 下载（或浏览器下载后放入）
curl -sL -o ~/.local/share/opencode/忆时/models/bge-base-zh-v1.5/onnx/model.onnx \
  https://hf-mirror.com/Xenova/bge-base-zh-v1.5/resolve/main/onnx/model.onnx
cd ~/.local/share/opencode/忆时/models/bge-base-zh-v1.5
for f in config.json tokenizer.json special_tokens_map.json tokenizer_config.json vocab.txt; do
  curl -sL -o "$f" "https://hf-mirror.com/Xenova/bge-base-zh-v1.5/resolve/main/$f"
done
```

> ⚠️ **注意**：运行时模型与数据统一存 `~/.local/share/opencode/忆时/`（LOCAL_BASE），**不写入 `~/.cache/chroma/`**，亦不存技能目录（技能更新会覆盖）。

## 必须配置外挂提示词

本技能依赖 OpenCode 的 `instructions` 配置才能完整生效。
未配置时，AI 不会自动检索记忆或存储记忆。

**配置步骤：**

1. 编辑全局配置文件 `~/.config/opencode/opencode.json`
2. 添加 `instructions` 字段，指向技能目录下的提示词文件：

```json
{
  "instructions": [
    "~/.config/opencode/skills/忆时/yishi-instructions.md"
  ]
}
```

3. 重启 OpenCode 使配置生效

**配置后 AI 将自动：**
- 每次对话前检索记忆系统
- 用户说"记住"时自动存储记忆
- 话题关联时主动涌现历史记忆
- 对话结束时自动归档重点

**未配置则：**
- 技能仍可手动调用命令
- 但不会自动检索/存储记忆
- 不会主动联想和闪回

## 运行环境

- Python: 3.13+
- 依赖: chromadb 1.5.4
- 脚本: `scripts/memory_core.py`
- 数据: `data/` (ChromaDB PersistentClient 自动创建)
