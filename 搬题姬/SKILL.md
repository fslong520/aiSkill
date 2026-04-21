---
name: ojimport
description: 从 OJ 平台搬运题目，生成标准化的题目文件包
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - BrowserUse
---

Domain keywords: OJ题目, 算法题搬运, 竞赛题目, AtCoder, Codeforces, GESP

Summary: 从 OJ 平台搬运题目，生成标准化的题目文件包（含题面、标程、测试数据）。

Strategy:
1. **读取 `steps/00-detect-url.md`** → 检测输入类型 → 判断单题/多题
2. 初始化工作目录：`cp -r question work`
3. 获取题目信息：urlgo 访问页面 → snapshot → 解析题面
4. **读取 `steps/03-gesp.md`** → **按文档中的判定表确定GESP等级**
5. **读取 `steps/04-problem.md`** → **按文档中的模板格式生成题面**
6. **读取 `steps/05-config.md`** → **按文档中的模板格式写入配置**
7. 实现标程 std.cpp
8. **读取 `steps/07-testdata.md`** → **按文档要求修改 mkin.h 生成25组数据**
9. 打包发布：`zip -r problem.zip work`

AVOID:
- AVOID **不读取步骤文档就直接执行**，必须先读取对应步骤文档再执行
- AVOID **不按步骤文档的模板格式**，文档里规定了格式必须严格遵守
- AVOID **测试数据只写样例**，steps/07-testdata.md 要求修改 mkin.h 生成25组
- AVOID **GESP等级乱判**，必须按 steps/03-gesp.md 的判定表（状态压缩=七级）
- AVOID 忘记清理旧的 work 目录，应该先 `rm -rf work`
- AVOID PID 格式错误（如 ABC451_A），应该用小写 abc451a
- AVOID 删除 testdata/config.yaml，模板里已有

---

## 入口

**👉 第一步：读取 `steps/00-detect-url.md`**

---

## 快速参考

| 文件 | 路径 |
|------|------|
| 模板目录 | `question/` |
| 工作目录 | `work/` |
| 题面文件 | `work/problem_zh.md` |
| 配置文件 | `work/problem.yaml` |
| 标程 | `work/std.cpp` |
| 测试数据逻辑 | `work/mkin.h` |
  