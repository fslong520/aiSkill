# Step 5: 写入配置文件

## 🎯 目标

写入 `work/problem.yaml` 配置文件。

---

## 📝 pid 命名规则（重要！）

### 规则优先级

```
用户指定 pid > 比赛自动命名 > null
```

### 1. 用户指定 pid

如果用户明确指定了 pid，必须使用用户指定的值。

**示例**：
- 用户说："pid 用 gesp2026q1"
- 配置写：`pid: gesp2026q1`

### 2. 比赛自动命名

如果是比赛题目搬运，自动生成 pid：

**格式**：`{比赛简称}{场次}{题号}`

| 来源 | 格式示例 |
|------|---------|
| AtCoder ABC | `abc453a`, `abc453b`, `abc453c`... |
| AtCoder ARC | `arc123a`, `arc123b`... |
| Codeforces Round | `cf789a`, `cf789b`... |
| LeetCode | `lc1234` |
| Luogu 比赛 | `lgP1001` |

**生成方法**：从 URL 或比赛信息中提取比赛简称+场次+题号

### 3. 无比赛信息

单题搬运且无法确定来源时：`pid: null`

---

## 📝 配置格式

```yaml
# 比赛题目（自动命名）
pid: abc453a
title: "移除前导o(Trimo)"
tag:
  - "GESP一级"
  - "字符串"

# 用户指定 pid
pid: gesp2026q1
title: "帮贡排序(Help Contribution Sort)"
tag:
  - "GESP四级"

# 无比赛信息
pid: null
title: "自定义题目名(Custom Title)"
tag:
  - "原创"
```

---

## 🚨 注意事项

1. **pid**: 按上述规则确定，不是无脑填 null！
2. **title**: 必须使用 **中英文对照格式** `中文标题(英文原标题)`
   - 先翻译英文标题为中文（简洁准确，不超过10个字）
   - 格式：`中文(英文)`
   - 示例：`移除前导o(Trimo)`、`偷瞄(Sneaking Glances)`
3. **tag**: 必须包含 `GESPX级` 标签（知识点等级）

---

## 📊 判断结果与下一步跳转

### ✅ 配置写入完成

**输出**：`work/problem.yaml` 已创建

**👉 下一步**：读取 `steps/06-std.md` 实现标程