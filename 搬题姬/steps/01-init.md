# Step 1: 环境初始化

## 🎯 目标

从模板目录复制文件到工作目录。

---

## 🔧 命令

```bash
# 清理旧工作目录
rm -rf work 2>/dev/null

# 复制模板
cp -r question work
```

**模板位置**（按顺序查找）：
1. `SKILL.md 所在目录/question/`
2. `当前工作目录/question/`

---

## 📦 模板必须包含

| 文件 | 用途 |
|------|------|
| `std.cpp` | 标程模板 |
| `mkdata.cpp` | 数据生成器模板 |
| `mkin.h` | 测试数据逻辑模板 |
| `problem.yaml` | 配置文件模板 |

---

## 📊 判断结果与下一步跳转

### ✅ 初始化成功

**输出**：`work/` 目录已创建，包含模板文件

**👉 下一步**：读取 `steps/02-get-info.md` 获取题目信息

---

### ❌ 模板不存在

**输出**：`cp: cannot stat 'question': No such file or directory`

**处理**：
1. 检查模板目录是否存在
2. 如果不存在，创建基础模板文件
3. 重新执行初始化