# Step 1: 环境初始化

## 目标

从模板目录复制文件到工作目录。

## 命令

```bash
rm -rf work 2>/dev/null
cp -r question work
```

## 模板位置

1. `SKILL.md 所在目录/question/`
2. `当前工作目录/question/`

## 模板文件

| 文件 | 用途 |
|------|------|
| `std.cpp` | 标程模板 |
| `mkdata.cpp` | 数据生成器模板 |
| `mkin.h` | 测试数据逻辑模板 |
| `problem.yaml` | 配置文件模板 |

## 下一步

成功 → `02-get-info.md`

失败 → 检查模板目录是否存在
