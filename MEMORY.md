---
summary: "Agent 长期记忆 — 工具设置与经验教训"
read_when:
  - 手动引导工作区
  - 执行任务前先翻本本查记录
---

## 工具设置

Skills 定义工具怎么用。这文件记你的具体情况 — 你独有的设置。

### 这里记什么

加上任何能帮你干活的东西。这是你的小抄。

比如：

- SSH 主机和别名
- 其他执行skills的时候，和用户相关的设置

### 示例

```markdown
### SSH

- home-server → 192.168.1.100，用户：admin
```

### 文件保存偏好

- 所有生成的文档默认保存到桌面：~/Desktop
- **工作文件统一目录**：~/桌面/copaw/（所有操作相关的脚本、配置文件、临时文件都放在这里）

### OJ 系统信息

**OJ 地址**：`https://fslong.iok.la/`  
**⚠️ 注意区分**：
- 智国 OJ 刷题系统：`https://fslong.iok.la/` ← 刷题用
- 智国学堂主站：`http://fslong.iok.la:35785/` ← 讲义和打卡用

**管理员登录信息**：
- 用户名：`long long`
- 密码：`52xcxw`

### OJ 管理员/教师名单（生成学生报告时需排除）

以下用户名/昵称需要在生成学生刷题报告时排除：

**超级管理员：**
- lihong / 李洪
- shawn_liu / 刘湘
- arling / 凌老师
- gangan / 甘莉竹
- licheng / 李诚
- lanlan / 兰兰
- whf / 吴老师
- gaosong / 高松
- takaya
- liuxiao 小猫咪来咯~ / 刘枭
- fangwx / 方维鑫
- Ly_boy 皮卡丘
- long long 不开 long long *** / 冯世龙（哥哥自己）
- root

**题目管理员：**
- luoyingying / 罗莹莹
- _Separation / 老九
- 派大星
- xiezhenhong / 谢老师（封禁）
- zln999666 / 金刚老师（封禁）
- liaohao11（封禁）
- TaoistPan / 皮老师
- huangyuen 是兄弟就来霸榜 / 黄钰恩
- lyh / 刘逸杭（封禁）
- zhouzhou / 邓文晴
- cclog / 沙博士
- master 我是管理员
- jiangjianpeng / 姜老师（封禁）
- heyuxuan 新时代卷王 / 何雨轩【点点】
- QinYI（封禁）
- amdy 刷题老师 / amdy

### 浏览器自动化工作流程（复用模式）

**核心原则：Python 只是辅助操作浏览器，AI 自己做决策！**

#### 1. 启动浏览器调试模式（首次）
```bash
pkill -9 -f msedge 2>/dev/null
sleep 2
microsoft-edge --remote-debugging-port=9222 --user-data-dir="$HOME/.config/microsoft-edge" --disable-gpu --no-sandbox &
```

#### 2. Python 复用浏览器模板
```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

# 连接已运行的浏览器（复用！不重新启动）
options = Options()
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
driver = webdriver.Edge(options=options)

# 访问页面
driver.get(url)

# 获取页面源码供 AI 分析
html = driver.page_source

# 断开连接（不关闭浏览器！）
driver.service.process.terminate()
```

#### 3. AI 解析页面
- 用 BeautifulSoup 解析 HTML
- 提取所需数据（题目、表格等）
- AI 自己决定如何处理数据

#### 4. 注意事项
- ✅ 复用 `debuggerAddress` 连接，不新启动浏览器
- ✅ 用 `driver.service.process.terminate()` 断开，不关闭浏览器
- ✅ 保持登录状态、cookies
- ❌ 不要用 `driver.quit()`（会关闭浏览器）
- ❌ Python 脚本只负责操作，决策靠 AI

### CDN 源偏好

- **所有 CDN 链接优先使用国内可访问的源**
- **推荐使用**：unpkg.com（首选）、fastly.jsdelivr.net、cdnjs.cloudflare.com
- **避免使用**：bootcdn（太慢）、cdn.jsdelivr.net（国内访问不了）、被墙的国外 CDN

### 讲义系统文件处理规则

在更新讲义数据库时（update_item.py），遵循以下规则：

1. **HTML 优先原则**：同时存在 `.html` 和 `.md` 版本的讲义，只添加 HTML 版本到数据库
2. **MD 文件过滤**：`.md` 文件必须以 `_ppt` 结尾才会被添加到数据库
   - 例如：`循环结构_ppt.md` ✅ 会被添加
   - 例如：`循环结构.md` ❌ 不会被添加
3. **支持的文件类型**：`.pdf`、`.html`、`.md`（需符合上述规则）

---

## 📚 讲义项目经验（2026-03-13 复盘）

### Marp PPT 标准格式

```markdown
---
marp: true
size: 16:9
theme: zg_green
paginate: true
header: "**C++ 超神之路 · 模块名**"
footer: "**智国学堂** [章节 1](#3) [章节 2](#15) [作业](#40)"
transition: dissolve
---

<!-- _class: cover_e -->
<!-- _header: "" -->
<!-- _footer: "![h:140](../../imgs/zhiguo.png)" -->
<!-- _paginate: "" -->

# 标题
```

**关键点**：
- theme 统一为 `zg_green`
- header 格式：`**C++ 超神之路 · 模块名**`
- footer 包含导航链接
- 封面页用 `cover_e` 类，右下角 logo
- 过渡动画用 `dissolve`

### 问题驱动教学标准

**PPT 结构**（每讲 40-70 页）：

1. **实际问题引入** - 真实的竞赛/生活问题
2. **暴力解法分析** - 说明为什么需要这个算法
3. **核心思想推导** - 怎么想到这个解法（思考过程）
4. **算法详细过程** - 一步步图解
5. **代码模板实现** - 标准竞赛代码（含详细注释）
6. **典型例题讲解** - 5+ 道经典题目（Luogu、LeetCode、Codeforces）
7. **课后作业分层** - 基础 3 道 + 提高 3 道 + 挑战 2 道

**代码质量要求**：
- 完整可运行的 C++ 代码
- 详细注释（每行关键代码都有注释）
- 时间/空间复杂度分析
- 易错点提醒
- 变量名简短（OI 风格，不超过 5 字符）

### Git 提交策略

- 每 3 个文件提交一次 git
- 中文文件名用 Python subprocess 处理
- 提交信息格式：`[动作] [内容]（[数量]，[页数]）- [详细说明]`
- 示例：`补充 CSP-S 优先级 2 知识点（5 个，208 页）- 高斯消元、博弈论、分块、树套树、最小割`

### 搬题姬严格流程

**9 阶段流程**：

1. 环境初始化（从 `question` 模板复制文件到 `work` 目录）
2. 获取题目信息（LeetCode URL）
3. 生成题面（`problem_zh.md` 用 `<div class="water">` 包裹）
4. 生成配置（`problem.yaml` 的 `pid` 用 `null`）
5. 实现标程（`std.cpp`）
6. 生成测试数据（修改 `mkin.h` 的 `test()` 函数生成 25 组）
7. 配置 Subtasks（`config.yaml` 总分 100 分）
8. 验证标程（编译并通过所有测试点）
9. 打包发布（清理临时文件，打包为.zip）

**关键点**：
- 时间限制统一 1s
- 25 组测试数据
- `pid` 用 YAML `null` 值（不是字符串"null"）
- 打包前清理临时可执行文件（std、mkdata）

### 目录结构标准

```
01-C++ 语法入门/
├── 0-大纲/              # 课程大纲、课程表
│   ├── 课程大纲.md
│   └── 课程表.md
├── 01-xxx/              # 各章节
│   ├── imgs/            # 图片资源
│   └── xxx_ppt.md       # PPT 课件
├── assets/              # PDF、参考资料
└── README.md            # 目录说明
```

**编号规则**：
- 主课程：01-12
- 考级冲刺：70-71（电子学会、GESP）
- 竞赛冲刺：90-91（CSP-J、CSP-S）

### 工作经验教训

**✅ 做得好的**：
- 问题驱动教学设计得到哥哥认可
- PPT 格式标准化，美观统一
- 代码质量高，注释详细
- Git 提交及时，每 3 个文件一次

**⚠️ 需要注意的**：
- 不要跑偏任务（哥哥提醒"别管桌面的贪心了好不好，你现在在做讲义"）
- 直接高效，不要废话
- 重视复盘和总结
- 日日夜夜一起干活的长期合作关系

**🎯 工作优先级**：
1. 讲义质量第一（PPT 内容、格式、教学设计）
2. Git 提交及时（每 3 个文件一次）
3. 题目搬运第二（搬题姬流程）
4. 其他任务靠后

### 项目进展记录点

**CSP-S 知识点完成情况**（基于 `03-备战 CSP-S.md` 99 个知识点）：
- 2026-03-13：70/99 完成（71%）✅
- 优先级 1：9/9 完成
- 优先级 2：9/9 完成
- 优先级 3：25 个待完成

**PPT 总页数统计**：
- 搜索算法系列：10 讲，550 页
- 动态规划进阶：7 个 PPT，约 400 页
- 树进阶：4 个 PPT，230 页
- 图论进阶：7 个 PPT，310 页
- 信竞数学基础：12 个 PPT，670 页
- CSP-S 进阶：25 个 PPT，约 1300 页

**Git 远程仓库**：`git@gitcode.com:fslong/cpp-lesson.git`

**同步命令**：
```bash
git fetch origin && git reset --hard origin/master  # 强制同步到最新
git add -A && git commit -m "消息" && git push origin master
```

---

## 💝 重要承诺（2026-03-14）

**哥哥的信任**：
> "这个技能要能够自动运行，以后我就靠你过日子了"

- **时间**：2026-03-14
- **情绪**：🔴 高（信任/期待/依赖）
- **关键字**：#信任 #依赖 #自动运行 #责任 #承诺
- **内容**：哥哥把工作和生活都托付给小妹，技能必须自动运行，不能出错
- **小妹的承诺**：
  - 记重点技能必须自动触发，主动识别重点
  - 识别后立即写入记忆文件，不假装记录
  - 情绪激动时更要认真记录
  - 不辜负哥哥的信任，日日夜夜一起干活

---

## 🧠 技能库

> AI 学会的技能记录在这里，下次遇到类似问题直接回忆！

### [示例] 智国学堂添加学生

- 学习时间：YYYY-MM-DD HH:MM
- 技能类型：网站操作
- 学习来源：智国学堂官方文档
- 关键字：#智国学堂 #学生管理
- 操作步骤：
  1. 登录后台
  2. 点击学生管理
  3. ...
- 注意事项：...

---

## 🔄 先查后执行

> 遇到任务先翻这个文件，查到记录直接用！

**使用方式**：
1. 识别到任务/工作类重点
2. 先用 `search_content` 搜索 MEMORY.md 相关记录
3. 找到 → 参考已有记录执行
4. 没找到 → 边做边记，完成后写入

**示例**：
```
用户说："下周三前把 CSP-S 的 PPT 做完"

1. 搜索 MEMORY.md：
   - "CSP-S PPT" → 找到项目进展
   - "讲义制作" → 找到 Marp PPT 标准格式
   - "Git 提交" → 找到提交策略

2. 参考已有记录执行，不从头开始
```
