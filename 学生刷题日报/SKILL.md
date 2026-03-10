---
name: 学生刷题日报
description: |
  使用 browser_use 工具自动抓取智国 OJ 学生刷题数据，生成精美的 Markdown 和 HTML 日报。
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  trigger: 智国 OJ 刷题日报生成
  source: 智国 OJ 数据抓取和处理
---


# 学生刷题日报技能

## 功能描述

使用 browser_use 工具自动抓取智国 OJ 学生刷题数据，生成精美的 Markdown 和 HTML 日报。

## 使用方式

### 手动触发
```bash
copaw run 学生刷题日报
```
或直接对 Agent 说："生成今天的学生刷题日报"

### 自动运行
每天晚 10 点自动运行（通过 cron 定时任务触发 Agent）

## 输出文件

- **Markdown 源文件**：`~/Desktop/智国 OJ 刷题日报/智国 OJ 刷题日报_YYYY-MM-DD.md`
- **HTML 渲染文件**：`~/Desktop/智国 OJ 刷题日报/智国 OJ 刷题日报_YYYY-MM-DD.html`

## 配置说明

### 管理员/教师排除名单
在 MEMORY.md 中配置，自动排除管理员和老师的提交记录。常见管理员账号包括：lihong、shawn_liu、arling、long long 等约 30 个。

### OJ 登录信息
- OJ 地址：https://fslong.iok.la
- 用户名：long long
- 密码：已在 MEMORY.md 中安全存储

## 报告内容

### 总榜单
- 🏅 排名（金银铜牌样式）
- 👤 用户名
- ✅ 今日 AC 数

### 个人报告
- ✅ 今天 AC 的题目列表
- 🔍 今天尝试但未 AC 的题目列表（**只有最终没 AC 的才列在这里**）
- 📖 未 AC 题目的简洁题解（可用 mermaid 画图）
- 💡 代码优化建议（仅明显低效时才给）
- 🎯 今日训练重点点评（每个学生一句，说明练习的题目类型）

## 工作流程

### 1. 登录 OJ
```
- 打开浏览器访问 https://fslong.iok.la
- 使用 credentials 登录（从 MEMORY.md 获取）
```

### 2. 抓取 24 小时内提交数据（⚠️ 关键）
```
- 访问评测状态页面 /status
- 从第 1 页开始抓取
- 检查每条记录的提交时间：
  - "X 分钟前"、"X 小时前" → 24 小时内，需要
  - "X 天前" → 超出 24 小时，停止抓取
- 自动翻页（点击下一页按钮），直到遇到"1 天前"的记录
- ⚠️ 不要只抓第 1 页！必须翻页确保抓取所有 24 小时内的数据
```

### 3. 数据处理（⚠️ 关键逻辑）
```
- 过滤掉 MEMORY.md 中的管理员/教师账号
- 按学生分组统计：
  - 每个学生今日 AC 题数（**只显示 AC 数，不显示提交总数和通过率**）
- 判断未 AC 题目：
  - ✅ 正确逻辑：某题目今天有多次提交，但最终没有 Accepted → 需要题解
  - ❌ 错误逻辑：某题目今天有 Wrong Answer 但最终 Accepted 了 → 不需要题解
  - 简单判断：对每个学生，检查每个题目今天的最终状态，不是 Accepted 才列入未 AC
- 识别题目类型（用于生成训练重点点评）：
  - 字符串处理：加密解密、字符串反转、单词分割等
  - 循环嵌套：图形打印、数学计算等
  - 模拟算法：物品管理、过程模拟等
  - 动态规划：最优解、计数问题等
  - 贪心算法：局部最优选择等
  - 搜索算法：DFS、BFS 等
```

### 4. 查看学生代码并生成针对性题解（⚠️ 关键）
```
- 登录管理员账号（long long / 52xcxw）
- 对每个未 AC 的题目：
  1. 找到该学生该题目的最高分提交记录
  2. 访问 submission-detail 页面查看代码：
     - URL 格式：https://fslong.iok.la/submission-detail/{RunID}
     - 例如：https://fslong.iok.la/submission-detail/90204
  3. 分析学生代码：
     - ✅ 先找优点（思路正确、边界处理好等）
     - ❌ 再找问题（TLE、WA、MLE 等）
     - 💡 给出优化建议
  4. 访问题目页面了解题意：
     - URL 格式：https://fslong.iok.la/problem/{ProblemID}
     - 例如：https://fslong.iok.la/problem/P7036
  5. 生成针对性题解：
     - 基于学生的实际代码分析问题
     - 给出具体的优化代码示例
     - 用 mermaid 画图展示算法流程
     - 鼓励为主，先肯定再建议
```

### 5. 生成 Markdown 文档（第一步）
```
- 使用标准 Markdown 格式编写日报内容
- 包含所有数据、题解、点评
- mermaid 流程图用 ```mermaid 代码块包裹
- 代码示例用 ```cpp 代码块包裹（注意：Markdown 中不需要转义 HTML 实体）
- 保存为 ~/Desktop/智国 OJ 刷题日报/智国 OJ 刷题日报_YYYY-MM-DD.md
```

### 6. 生成 HTML 报告（第二步，基于 Markdown 渲染）
```
- 读取 Markdown 文档内容
- 渲染为精美的 HTML 页面：
  - 现代浅色主题（紫色渐变主色调）
  - 卡片式布局，悬停效果
  - 代码高亮（GitHub 浅色主题）
  - mermaid 流程图渲染
- 打印分页优化：
  - 第一页只显示总榜单（.rank-section { page-break-after: always; }）
  - 之后每个学生单独一页（.user-section { page-break-before: always; }）
  - 方便打印后分发给学生
- 保存文件到 ~/Desktop/智国 OJ 刷题日报/智国 OJ 刷题日报_YYYY-MM-DD.html
- 落款格式：Generated with ❤️ by 智国 AI
```

## 质量检查清单

生成报告前请确认：

- [ ] **翻页检查**：是否翻越多页抓取了所有 24 小时内的数据？
- [ ] **时间判断**：是否正确区分"X 小时前"和"X 天前"？
- [ ] **管理员排除**：是否排除了 long long、lihong 等管理员账号？
- [ ] **未 AC 逻辑**：是否只统计最终没 AC 的题目？（多次尝试后 AC 的不算）
- [ ] **榜单简化**：总榜单是否只显示 AC 数？（不显示提交总数和通过率）
- [ ] **查看代码**：是否登录管理员账号查看了学生的实际提交代码？
- [ ] **针对性题解**：题解是否基于学生代码分析？（不是脑补的）
- [ ] **题目类型识别**：是否为每个学生识别了练习的题目类型？
- [ ] **训练重点点评**：是否为每个学生生成了一句训练重点点评？
- [ ] **Markdown 格式**：代码块是否用 ```cpp 包裹？mermaid 是否用 ```mermaid 包裹？
- [ ] **HTML 渲染**：代码高亮是否正常？mermaid 图是否能渲染？
- [ ] **代码转义**：HTML 中代码块的 <、>、& 是否转义为 &lt;、&gt;、&amp;？
- [ ] **打印分页**：第一页是否只有总榜单？每个学生是否单独一页？
- [ ] **文件保存**：是否保存到 ~/Desktop/智国 OJ 刷题日报/？文件名是否包含日期？
- [ ] **落款格式**：是否是"Generated with ❤️ by 智国 AI"？

## 注意事项

### ⚠️ 常见错误及避免方法

1. **只抓第 1 页数据**
   - 错误：只抓取 /status?page=1 就生成报告
   - 正确：必须翻页，直到遇到"1 天前"的记录

2. **未 AC 判断错误**
   - 错误：把今天 AC 过的题目但有 WA 记录的也算未 AC
   - 正确：只统计到今天为止最终状态不是 Accepted 的题目

3. **题解渲染成代码块**
   - 错误：用 ``` 包裹题解内容
   - 正确：Markdown 中题解用正常段落和列表，代码示例才用 ```cpp

4. **打印时所有内容挤在一页**
   - 错误：没有设置 page-break 样式
   - 正确：总榜单后分页，每个学生单独一页

5. **榜单显示复杂**
   - 错误：显示提交总数、通过率等多个指标
   - 正确：只显示 AC 题数，简洁明了

6. **不查看学生代码就写题解**
   - 错误：只看题目名字就脑补题解
   - 正确：登录管理员账号，访问 submission-detail 页面查看学生实际代码，针对性分析

7. **代码块 HTML 实体未转义**
   - 错误：HTML 中代码中的 <、>、& 直接写入
   - 正确：HTML 中转义为 &lt;、&gt;、&amp;（Markdown 中不需要）

8. **缺少训练重点点评**
   - 错误：只列出题目，不说明练习了什么类型
   - 正确：每个学生卡片下添加一句点评，说明今日训练重点

### 📝 题解编写原则

- **简洁第一**：小孩子不愿意看太多文字，1-2 段话讲清楚思路
- **针对性**：基于学生实际代码分析，不是脑补的
- **可视化**：能用 mermaid 画图就用图，直观易懂
- **鼓励为主**：代码优化建议先肯定，再给建议
- **代码转义**：
  - Markdown 中：不需要转义，直接写 <、>、&
  - HTML 中：必须转义为 &lt;、&gt;、&amp;
- **精简内容**：没有代码优化建议就不写"代码优化建议"部分
- **训练点评**：每个学生一句，说明练习的题目类型（字符串、循环、模拟等）

## HTML 模板要点

```html
<!-- 页面宽度 -->
<style>
.container {
    max-width: 1100px;  /* 宽敞的页面宽度 */
}

/* 卡片边框加深 */
.user-section {
    border: 2px solid #cbd5e0;  /* 深灰色边框 */
}

/* 代码块浅色主题 */
.explanation pre {
    background: #f7fafc;  /* 浅灰背景 */
    border: 2px solid #e2e8f0;
}
.explanation pre code {
    color: #2d3748;  /* 深色文字 */
}

/* 打印分页样式 -->
@media print {
    .rank-section { page-break-after: always; }
    .user-section { page-break-before: always; }
    .user-section:first-of-type { page-break-before: avoid; }
}
</style>

<!-- 题解正常渲染 -->
<div class="explanation">
    <div class="explanation-title">💡 思路分析</div>
    <p>这道题需要...</p>
    <ul>
        <li><strong>预处理：</strong>先计算...</li>
        <li><strong>增量更新：</strong>只检查...</li>
    </ul>
    <code>行内代码示例</code>
    <pre><code class="language-cpp">// 转义后的代码
for(int i=0; i&lt;n; i++) {
    if(nx&gt;=0 &amp;&amp; nx&lt;n) { ... }
}</code></pre>
</div>

<!-- mermaid 图 -->
<div class="mermaid">
graph TD
    A[开始] --> B[处理]
    B --> C[结束]
</div>

<!-- 训练重点点评 -->
<div class="coach-comment">
    <p><strong>🎯 今日训练重点：</strong>字符串处理专项训练 —— 加密解密、字符串反转、单词分割，都是字符串操作的核心技能，继续加油！</p>
</div>
```

## 文件结构

```
~/Desktop/智国 OJ 刷题日报/
├── 智国 OJ 刷题日报_2026-03-10.md    # Markdown 源文件
└── 智国 OJ 刷题日报_2026-03-10.html  # HTML 渲染文件
```

## 相关文件

- 技能目录：`/home/fslong/.copaw/active_skills/学生刷题日报/`
- 管理员名单：`MEMORY.md` 中的「管理员/教师排除名单」section
- 输出文件夹：`~/Desktop/智国 OJ 刷题日报/`
- cron 任务：通过 `copaw cron` 管理，每晚 22:00 自动触发
