---
name: 搬题姬
description: 从 OJ 平台搬运题目，生成标准化题目文件包；也可根据用户提供的题目仅生成测试数据
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - BrowserUse

metadata:
  slug: ojimport
  trigger: OJ题目、搬题、算法题搬运、AtCoder、Codeforces、GESP、题目导入、测试点、生成数据、测试数据
---

## Keywords

OJ题目、搬题、算法题搬运、AtCoder、Codeforces、GESP、测试点、测试数据

## Summary

从 OJ 平台搬运题目，生成标准化文件包（题面+标程+数据），或根据用户提供的题目仅生成测试数据（.in/.out）。

## Strategy

### 单题搬运

1. 读取 steps/00-detect-url.md → 检测类型
2. 初始化：`cp -r question work_{PID}_{标题简写}`（详见 01-init.md）
3. 获取题面：按来源类型处理
   - URL：urlgo 访问 → snapshot → 解析（urlgo不可用时用 BrowserUse/WebFetch）
   - 文件：读取 steps/09-from-file.md → 从本地文件提取题面
   - 文本：读取 steps/10-from-text.md → 从用户提供的文本生成题面
4. 读取 steps/03-gesp.md → 判定等级
5. 读取 steps/04-problem.md → 生成题面
6. 读取 steps/05-config.md → 写配置
7. 实现标程 std.cpp
8. 读取 steps/07-testdata.md → 生成数据（⚠️ 只改 mkin.h，别动 mkdata.cpp）
9. 打包：`zip -r {PID}_{标题简写}.zip work_{PID}_{标题简写}`

### ⚠️ 比赛搬运（必须先创建题面汇总文件）

1. 读取 steps/contest/01-list.md → 创建题面汇总文件 `{contest_id}.md`
2. 读取 steps/contest/02-problem.md → **逐题翻译并追加写入汇总文件**
3. 读取 steps/contest/03-move.md → **从文件读取题面**，逐题生成完整题包

### 生成测试点

用户已有完整题面，只需要测试数据（.in/.out + config.yaml）。

**触发词**：用户说"生成测试点"、"出测试数据"、"想测试数据"、"写测试数据"等表示只要测试数据不要题面时。

**流程：**

1. 读取 steps/00-detect-url.md → 检测输入类型
2. 初始化：`cp -r question work_{PID}_{标题简写}`（详见 01-init.md）
3. 获取题面信息：
   - URL：urlgo/BrowserUse/WebFetch 访问并解析
   - 文件：读取 steps/09-from-file.md 提取题面（仅内部参考，不生成正式 problem_zh.md）
   - 文本：读取 steps/10-from-text.md 从文本提取题面
4. 读取 steps/11-testdata-only.md → **实现标程 + 生成测试数据 + 打包 testdata.zip + 交付**
5. **跳过**：题面格式化（04-problem.md）、GESP 定级（03-gesp.md）、配置写入（05-config.md）、全局打包（08-package.md）

## AVOID

- AVOID 不读步骤文档就执行
- AVOID 不按模板格式
- AVOID 测试数据只写样例
- AVOID GESP等级乱判
- AVOID 忘清理工作目录（`work_*`）
- AVOID PID 格式错误（用小写 abc451a）
- ⚠️ **AVOID 从对话上下文记忆题面，必须从文件读取**
- ⚠️ **AVOID 生成数据时修改 mkdata.cpp，只允许修改 mkin.h**
- ⚠️ **AVOID 测试数据缺少特殊性质和 hack 数据**
- ⚠️ **AVOID 修改样例：样例输入/输出必须原样复制，严禁增删改任何字符**
- ⚠️ **AVOID 删除图片链接：题面中的 `![](url)`、`<img>` 标签等所有图片语法必须原样保留**
- ⚠️ **AVOID 删除示意图：题面原有的示意图、表格、公式必须完整保留**
- ⚠️ **生成测试点时 AVOID 生成 problem_zh.md、problem.yaml**
- ⚠️ **生成测试点时 AVOID 全局打包（08-package.md 的整个工作目录 zip），只能打包 testdata/ 下的文件**
- ⚠️ **生成测试点时 AVOID 跳过 std.cpp：没有标程就无法生成 .out**
- ⚠️ **生成测试点时 AVOID 只写样例数据：25 组全覆盖（含 Hack）**
- ⚠️ **生成测试点时 AVOID 交付前不验证：必须检查 .in 格式、.out 与样例一致性、文件成对存在**

---

## 入口

读取 steps/00-detect-url.md
