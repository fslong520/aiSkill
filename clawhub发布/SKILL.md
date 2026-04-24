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
  slug: clawhubpub
  trigger: 发布技能、发布到ClawHub、上传技能、publish、clawhub发布
  source: 基于 clawhub CLI 官方文档
---

# ClawHub 技能发布

> 一键发布技能到 ClawHub 技能市场。

## Summary

检查登录→确认技能目录→检测发布历史→推荐Slug→确认参数→执行发布→验证结果。

## Keywords

发布技能、ClawHub、publish、技能市场、上传、版本管理

## Strategy

1. **检查登录**：`clawhub whoami`，未登录则`clawhub login`
2. **确认目录**：检查SKILL.md存在，读取 frontmatter 获取预设 slug/name
3. **检测历史**：`clawhub inspect <slug>`判断是否已发布
4. **分支处理**：
   - **新技能**：推荐Slug（若SKILL.md未定义）→ 确认参数 → 首次发布
   - **更新技能**：提取历史版本/name/tags → 自动递增版本 → 保持一致性更新
5. **执行发布**：`clawhub publish <path> --slug --name --version --changelog --tags`
6. **验证结果**：检查输出是否成功

## AVOID

- AVOID Slug包含连字符-或下划线_，必须是纯小写字母+数字紧密相连
- AVOID 更新已发布技能时更改tags，必须与历史版本保持tags和name一致
- AVOID tags使用中文，只能用英文逗号分隔
- AVOID 未检测发布历史就发布，必须先`clawhub inspect`判断是否已存在
- AVOID 未等待用户确认Slug就发布，必须提供3个方案让用户选择

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

### Step 2: 确认技能目录 & 检测发布历史

#### 2.1 检查目录
检查技能文件夹是否存在：
```
/home/fslong/.copaw/workspaces/default/active_skills/<技能名>/SKILL.md
```

**必须存在**：
- `SKILL.md` - 技能描述文件

#### 2.2 检测是否已发布（强制！）
在确定参数前，必须检查该技能是否已在 ClawHub 存在：

```bash
clawhub inspect <候选slug>
```
*(若 slug 不确定，可先用 `clawhub list` 模糊查找)*

**结果判断**：
- ✅ **已发布**：输出现有版本详情。
  - **铁律**：更新时必须与历史版本保持 `--tags` 和 `--name` 完全一致！
  - **动作**：从输出中提取原有 `tags`，作为本次发布的 `--tags` 参数。仅更新 `--version` 和 `--changelog`。
- ❌ **未发布**：报错 `Skill not found` 或无输出。
  - **动作**：按新技能流程，自行拟定 slug、name、tags。

**⚠️ 核心警告**：
- **绝不要随意更改已发布技能的 tags！** 这会导致 ClawHub 搜索索引混乱或技能关联丢失。
- 更新发布的唯一变量应是：`version`（递增）和 `changelog`（本次改动）。

---

### Step 3: 确定发布参数

**⚠️ 关键区分：新技能 vs 更新技能**

根据 Step 2.2 的检测结果，走不同流程：

---

#### 3A. 新技能发布流程（Skill not found）

**3A.1 读取 SKILL.md 获取预设参数**
先读取技能目录下的 SKILL.md，检查是否已定义：
- `name` - 技能名称（如有则直接使用）
- `metadata.slug` 或 frontmatter 中的 slug（如有则直接使用，跳过推荐步骤）

**3A.2 Slug 推荐（仅当 SKILL.md 未定义 slug 时）**
向用户展示 3 个不同维度的 Slug 推荐方案，等待用户选择。
**推荐维度示例**：
1.  **全拼音方案**（适合中文技能）：`mochi`, `banti`
2.  **英文意译方案**（适合通用技能）：`inkpot`, `ojimport`
3.  **功能描述方案**（混合或直白）：`problemporter`, `dailyreport`

**⚠️ 推荐铁律**：
- **禁止符号**：推荐的 Slug 中绝对不能包含 `-` 或 `_`。
- **纯小写**：所有字母必须小写。
- **等待确认**：列出方案后，询问用户确认。

**3A.3 确定其他参数**
| 参数 | 来源 | 示例 |
|------|------|------|
| `--slug` | SKILL.md 或用户确认 | `ojimport` |
| `--name` | SKILL.md 或技能目录名 | `搬题姬` |
| `--version` | 首次发布默认 `1.0.0` | `1.0.0` |
| `--changelog` | 询问用户或自动生成 | `首次发布` |
| `--tags` | SKILL.md 或询问用户 | `oj,algorithm` |

---

#### 3B. 更新技能发布流程（已存在）

**⚠️ 铁律：更新时必须保持 slug、name、tags 与历史一致！**

**3B.1 从 SKILL.md 读取 slug**
```bash
# 读取 SKILL.md frontmatter 中的 slug
```

**3B.2 从 clawhub inspect 输出提取历史信息**
- **Latest 版本号**：如 `Latest: 1.7.0` → 新版本应为 `1.7.1` 或更高
- **Tags**：从 Tags 行提取，如 `Tags: algorithm=1.7.0, oj=1.7.0` → tags 为 `algorithm,oj`
- **Name**：从输出第一行提取，如 `ojimport 搬题姬` → name 为 `搬题姬`

**3B.3 自动递增版本号**
- 从 `Latest: x.y.z` 提取版本号
- 默认递增 patch 版本：`x.y.z` → `x.y.(z+1)`
- 询问用户是否需要 major/minor 版本升级

**3B.4 确定参数**
| 参数 | 来源 | 示例 |
|------|------|------|
| `--slug` | SKILL.md（必须与历史一致） | `ojimport` |
| `--name` | clawhub inspect（必须与历史一致） | `搬题姬` |
| `--version` | 历史版本递增 | `1.7.0` → `1.7.1` |
| `--changelog` | 询问用户本次改动 | `修复 WebSocket 问题` |
| `--tags` | clawhub inspect（必须与历史一致） | `oj,algorithm,problem` |

---

**⚠️ Slug 命名铁律（最高优先级）**：
- **❌ 禁止任何符号**：绝对不允许使用连字符 `-`、下划线 `_` 或任何符号！
- **✅ 唯一格式**：全小写字母 + 数字，紧密相连，干净纯粹。
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

**铁律（无符号纯净模式）**：
- **❌ 禁止任何符号**：绝对不要使用连字符 `-`、下划线 `_`！
- **✅ 唯一允许**：仅小写字母 (a-z) 和数字 (0-9)。

**示例**：
- ✅ `inkpot`, `poxiao`, `lessonprep` (紧密相连)
- ❌ `po-xiao` (连字符), `oi-style` (连字符), `墨池` (中文)

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
- [ ] slug **纯净无符号**（全小写，无 `-` `_`）
- [ ] name 可以用中文或英文
- [ ] version 是语义化版本（x.y.z）
- [ ] changelog 简明扼要说明改动
- [ ] tags 只用英文，逗号分隔

---

**作者**: fslong

**创建日期**: 2026-03-29

**来源**: 墨池技能发布实践