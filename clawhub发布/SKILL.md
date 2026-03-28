---
name: clawhub发布
description: |
  将本地技能发布到 ClawHub 技能市场。自动检查技能目录结构、生成版本号、
  构建 changelog，执行发布命令并验证结果。
  
  **触发场景**：用户说"发布技能"、"发布到 ClawHub"、"上传技能"等。

allowed-tools:
  - Read
  - Write
  - ExecuteShellCommand
  - AskUserQuestion

metadata:
  trigger: 发布技能、发布到ClawHub、上传技能、publish、clawhub发布
  source: 基于 clawhub CLI 官方文档
---

# ClawHub 技能发布

> 一键发布技能到 ClawHub 技能市场。

---

## 触发场景

当用户说：
- "发布 XX 技能到 ClawHub"
- "把 XX 发布上去"
- "上传技能"
- "技能发布"

立即调用本技能。

---

## 发布流程

### Step 1: 检查登录状态

```bash
clawhub whoami
```

**结果**：
- ✅ 显示用户名 → 已登录，继续
- ❌ 未登录 → 执行 `clawhub login`，等待用户浏览器登录

---

### Step 2: 确认技能目录

检查技能文件夹是否存在：
```
/home/fslong/.copaw/workspaces/default/active_skills/<技能名>/SKILL.md
```

**必须存在**：
- `SKILL.md` - 技能描述文件

**可选文件**：
- `*.py` - Python 脚本
- `*.js` - JavaScript 脚本
- `assets/` - 资源文件
- `templates/` - 模板文件

---

### Step 3: 确定发布参数

| 参数 | 来源 | 示例 |
|------|------|------|
| `--slug` | 技能英文名（小写，无空格） | `inkpot` |
| `--name` | 技能显示名 | `InkPot` |
| `--version` | 版本号（询问用户或自动推断） | `2.0.0` |
| `--changelog` | 更新说明（询问用户） | `Switch to KV format` |
| `--tags` | 标签（英文，逗号分隔） | `knowledge,learning` |

**⚠️ 注意**：
- `--tags` 只能用英文，不能用中文！
- `--slug` 必须是小写字母、数字、下划线或连字符
- `--version` 必须是语义化版本（x.y.z）

---

### Step 4: 执行发布命令

```bash
clawhub publish <技能路径> \
  --slug <英文slug> \
  --name <显示名> \
  --version <版本号> \
  --changelog "<更新说明>" \
  --tags "<英文标签>"
```

**示例**：
```bash
clawhub publish /home/fslong/.copaw/workspaces/default/active_skills/墨池 \
  --slug inkpot \
  --name "InkPot" \
  --version "2.0.0" \
  --changelog "Switch from JSON to simple KV text format" \
  --tags "knowledge,learning,chinese"
```

---

### Step 5: 验证发布结果

**成功输出**：
```
✔ OK. Published inkpot@2.0.0 (k97f1c87nkv5tzq1rzkd26b3a983shgy)
```

**失败情况**：
- `Field name 中文 has invalid character` → tags 或 name 包含中文，改用英文
- `Not logged in` → 执行 `clawhub login`
- `Skill not found` → 路径错误，检查技能目录

---

## 版本号规则

| 版本类型 | 何时使用 | 示例 |
|----------|----------|------|
| **Major (x.0.0)** | 大改动、不兼容更新 | `2.0.0` - 从 JSON 改为 KV 格式 |
| **Minor (0.y.0)** | 新功能、向后兼容 | `1.1.0` - 新增搜索功能 |
| **Patch (0.0.z)** | 小修复、bug 修复 | `1.0.1` - 修复解析错误 |

---

## 常见问题

### Q: tags 包含中文导致失败？

**错误**：
```
Field name 中文 has invalid character '中'
```

**解决**：tags 只能用英文，如 `chinese` 而不是 `中文`。

---

### Q: slug 格式错误？

**规则**：
- 只能包含：小写字母、数字、连字符 `-`、下划线 `_`
- 不能包含：中文、空格、大写字母、特殊符号

**示例**：
- ✅ `inkpot`, `oi-style`, `lesson_prep`
- ❌ `墨池`, `OI风格`, `lesson prep`

---

### Q: 如何更新已发布的技能？

**流程**：
1. 修改本地技能代码
2. 更新 SKILL.md 中的版本说明
3. 增加版本号（如 `1.0.0` → `1.1.0`）
4. 写 changelog 说明改动
5. 重新执行 `clawhub publish`

---

## 快速参考

### ClawHub CLI 常用命令

| 命令 | 用途 |
|------|------|
| `clawhub whoami` | 检查登录状态 |
| `clawhub login` | 登录（浏览器认证） |
| `clawhub logout` | 登出 |
| `clawhub publish <path>` | 发布技能 |
| `clawhub search <query>` | 搜索技能 |
| `clawhub install <slug>` | 安装技能 |
| `clawhub list` | 列出已安装技能 |
| `clawhub inspect <slug>` | 查看技能详情 |

---

## 发布清单

发布前检查：

- [ ] 已登录 ClawHub (`clawhub whoami`)
- [ ] SKILL.md 存在且格式正确
- [ ] slug 使用英文、小写、无空格
- [ ] name 可以用中文或英文
- [ ] version 是语义化版本（x.y.z）
- [ ] changelog 简明扼要说明改动
- [ ] tags 只用英文，逗号分隔

---

**作者**: fslong

**创建日期**: 2026-03-29

**来源**: 墨池技能发布实践