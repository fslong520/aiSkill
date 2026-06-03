---
name: 搬题姬
version: 2.0.0
description: 从 OJ 平台搬运题目（含AtCoder/Codeforces等），生成标准化题目文件包；也可根据用户提供的题目仅生成测试数据。用户说"搬运""搬题""搬道题""导入题目"均适用
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - BrowserUse

metadata:
  slug: ojimport
  trigger: OJ题目、搬题、算法题搬运、搬运题目、搬道题、搬一下、AtCoder、Codeforces、GESP、题目导入、测试点、生成数据、测试数据
---

## Keywords

OJ题目、搬题、搬运、搬运题目、算法题搬运、搬道题、搬一下、AtCoder、Codeforces、GESP、测试点、测试数据

## Summary

自OJ搬题，生标准化题包（题面+标程+数据）；或依用户所供，仅生测试数据（.in/.out）。

## Strategy

### 参考文档

生成测试数据前，先读 **`references/testdata-design.md`**，按题目类型选取边界清单与 Hack 策略。
所有步骤文件（`07-testdata.md`、`11-testdata-only.md`）中的测试数据细节均引用该文档。

### 单题搬运

1. 读 steps/00-detect-url.md → 辨类型
2. 初始化：`cp -r question work_{PID}_{标题简写}`（详 01-init.md）
3. 取题面：按来源
   - URL：urlgo 访问 → snapshot → 解析（urlgo不可用时用 BrowserUse/WebFetch）
   - 文件：读 steps/09-from-file.md → 自本地文件取题面
   - 文本：读 steps/10-from-text.md → 自用户文本取题面
4. 读 steps/03-gesp.md → 定等级
5. 读 steps/04-problem.md → 生题面
6. 读 steps/05-config.md → 写配置
7. 实现标程 std.cpp
8. 读 steps/07-testdata.md → 生数据（⚠️ 只改 mkin.h，勿动 mkdata.cpp）
9. 打包：`zip -r {PID}_{标题简写}.zip work_{PID}_{标题简写}`

### ⚠️ 比赛搬运（必先创题面汇总文件）

1. 读 steps/contest/01-list.md → 创题面汇总文件 `{contest_id}.md`
2. 读 steps/contest/02-problem.md → **逐题译之，追加写入汇总文件**
3. 读 steps/contest/03-move.md → **自文件读题面**，逐题生完整题包

### 生成测试点

用户已有完整题面，仅需测试数据（.in/.out + config.yaml）。

**触发词**：用户言"生成测试点"、"出测试数据"、"想测试数据"、"写测试数据"等。

**流程：**

1. 读 steps/00-detect-url.md → 辨输入类型
2. 初始化：`cp -r question work_{PID}_{标题简写}`（详 01-init.md）
3. 取题面信息：
   - URL：urlgo/BrowserUse/WebFetch 访问并解析
   - 文件：读 steps/09-from-file.md 取题面（仅内部参考，不生正式 problem_zh.md）
   - 文本：读 steps/10-from-text.md 自文本取题面
4. 读 steps/11-testdata-only.md → **实现标程 + 生测试数据 + 打包 testdata.zip + 交付**
5. **跳过**：题面格式化（04-problem.md）、GESP 定级（03-gesp.md）、配置写入（05-config.md）、全局打包（08-package.md）

## AVOID

- AVOID 不读步骤文档即执行
- AVOID 不按模板格式
- AVOID 测试数据只写样例
- AVOID GESP等级乱判
- AVOID 忘清理工作目录（`work_*`）
- AVOID PID 格式错误（用小写 abc451a）
- ⚠️ **AVOID tag 只写 GESP 等级：必含 1~3 个知识点标签 + 1 个等级标签，禁单标签敷衍**
- ⚠️ **AVOID 自对话上下文记忆题面，必自文件读取**
- ⚠️ **AVOID 生成数据时修改 mkdata.cpp，只许修改 mkin.h**
- ⚠️ **AVOID 测试数据缺少特殊性质和 hack 数据**
- ⚠️ **AVOID 写完 std 不验样例：所有样例输入逐一喂入，输出须与题面完全一致，全过方可进入数据生成**
- ⚠️ **AVOID 修改样例：样例输入/输出必原样复制，禁增删改任何字符**
- ⚠️ **AVOID 删除图片链接：题面中 `![](url)`、`<img>` 标签等所有图片语法必原样保留**
- ⚠️ **AVOID 删除示意图：题面原有示意图、表格、公式必完整保留**
- ⚠️ **生成测试点时 AVOID 生成 problem_zh.md、problem.yaml**
- ⚠️ **生成测试点时 AVOID 全局打包（08-package.md 之整个工作目录 zip），只打包 testdata/ 下文件**
- ⚠️ **生成测试点时 AVOID 跳过 std.cpp：无标程则 .out 不出**
- ⚠️ **生成测试点时 AVOID 只写样例数据：25 组全覆盖（含 Hack）**
- ⚠️ **生成测试点时 AVOID 交付前不验证：必查 .in 格式、.out 与样例一致、文件成对存在**

---

## 入口

读 steps/00-detect-url.md
