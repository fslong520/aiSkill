# OpenCode 技能仓库

## 此为何物

OpenCode 之技能集，凡五十有余，置于 `~/.config/opencode/skills/`。
各技能均有独立目录，内含 SKILL.md 定义行为，亦可附带脚本、模块、参考文档。
运行时，OpenCode 据此加载上下文，赋予 AI 特定能力。

## 目录结构

```
~/.config/opencode/skills/
├── README.md                # 此文件
├── .gitignore               # 版本忽略规则
├── AI读书/                   # 书籍精华提炼
├── AI剧本杀/                 # 异世界人生模拟
├── GESP作业/                 # GESP考级作业生成
├── oi风格/                   # OI竞赛代码格式化
├── 备课/                     # 信息学奥赛备课框架
├── 忆时/                     # 记忆胶囊系统（自动加载）
├── 命题工坊/                  # 信息学竞赛命题
├── 搬题姬/                   # OJ题目搬运
├── 学生刷题日报/              # 刷题情况日报
├── 智国学堂/                  # Django教学平台开发
├── 撸树人/                    # 鲁迅式公众号推文
├── 公众号写手/                # 多平台文章创作
├── 图片姬/                    # 插图Prompt生成
├── 像素绘/                    # 像素艺术插图
├── 风语绘/                    # 情绪金句卡片
├── 格知/                     # 科普长图
├── 格语/                     # 宫格手绘故事
├── 漫语/                     # 四格哲理漫画
├── 雀影/                     # 视频分镜脚本
├── 雀漫/                     # 动态漫画分镜
├── 墨染天工/                  # 架空历史小说
├── 见自己/                    # 自我探索梳理
├── 破晓/                     # 股市资讯日报
├── 盯盘助手/                  # A股智能分析
├── hold-or-sell/             # 房产持仓决策
├── 穷尽调试/                  # 结构化调试方法
├── 技能诊所/                  # 技能诊断与创建
├── 定时任务/                  # 周期定时任务
├── clawhub发布/              # 技能市场发布
├── docx/                     # Word文档处理
├── xlsx/                     # 电子表格处理
├── pdf/                      # PDF文件处理
├── pptx/                     # 演示文稿处理
├── file_reader/              # 文本文件阅读
├── browser_cdp/              # 浏览器CDP连接
├── browser_visible/          # 浏览器可见模式
├── urlgo/                    # 浏览器控制CLI
├── news/                     # 新闻检索
├── himalaya/                 # 邮件管理CLI
├── cron/                     # 定时任务管理
├── channel_message/          # 渠道消息推送
├── chat_with_agent/          # 多Agent对话
├── multi_agent_collaboration/# Agent协作
├── make_plan/                # 外部规划请求
├── guidance/                 # QwenPaw安装配置
├── QA_source_index/          # 文档路径索引
├── dingtalk_channel/         # 钉钉渠道接入
├── cosprompt/                # AI绘图提示词
├── stocktourch/              # 个股分析报告
├── web-design-guidelines/    # UI设计审查
├── 析题/                     # 题目分析与题解
├── logs/                     # 日志目录（已忽略）
└── ...
```

## 技能三要素

每技能至少含：
- **SKILL.md** —— 核心定义，含名称、描述、触发条件、执行流程
- **元数据** —— opencode.json 中通过 `metadata.slug` 注册
- **资源** —— 脚本、模块、引用文档（视需要而定）

部分技能另附 `yishi-instructions.md`，作为外挂提示词注入 AI 上下文。

## 接入方式

全局配置 `~/.config/opencode/opencode.json` 中，以 `instructions` 字段引入外挂提示词：
```json
{
  "instructions": [
    "~/.config/opencode/skills/忆时/yishi-instructions.md"
  ]
}
```
技能自身通过 `auto_load: true` 或手动 `skill` 工具调用激活。

## 纪律

- 一技能一事，不越界
- 修改一技能，不同时动他者
- 重大变更，先存方案于忆时，再动手

## 版本

Git 管理。提交信息以中文简述变更实质。
