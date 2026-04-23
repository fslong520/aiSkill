# 智国学堂 - 项目架构学习笔记

## 一、项目概述

**项目名称**：TeachZero（智国学堂）  
**项目定位**：基于 Django 和 Markdown 的课程服务系统，辅助老师备课和学生管理  
**项目路径**：`~/Documents/blog/blog/`

---

## 二、技术栈

| 层级 | 技术 | 版本/说明 |
|------|------|----------|
| **后端框架** | Django | 3.2 |
| **数据库** | SQLite | db.sqlite (~40MB) |
| **后台UI** | django-simpleui | 定制化管理界面 |
| **编辑器** | django-mdeditor | Markdown编辑器 |
| **Markdown渲染** | markdown + pymdown-extensions | 支持表格、代码高亮、数学公式 |
| **部署** | gunicorn + gevent | 生产环境 |
| **前端** | 原生HTML/JS/CSS + Bootstrap风格 | 无前后端分离 |

---

## 三、目录结构

```
~/Documents/blog/blog/
├── apps/                    # Django应用模块
│   ├── home/               # 用户系统（核心）
│   ├── teach/              # 讲义系统
│   ├── exam/               # 考试系统
│   ├── blog/               # 知识系统/博客
│   ├── service/            # 教务系统
│   ├── scratch/            # Scratch作品系统
│   ├── mindmap/            # 思维导图
│   ├── algorithm/          # 算法可视化
│   ├── mathgame/           # 数学游戏
│   ├── englishgame/        # 英语游戏
│   ├── clouddisk/          # 云盘
│   ├── tool/               # 工具
│   ├── mdeditor/           # Markdown编辑器
│   ├── simpleui/           # 后台UI
│   └── templatetags/       # 自定义模板标签
├── teachzero/              # 项目配置
│   ├── settings.py         # 主配置
│   ├── user_settings.py    # 用户自定义配置
│   └── urls.py             # 主路由
├── static/                 # 静态文件
├── uploads/                # 上传文件（项目外）
├── db.sqlite               # 数据库
├── manage.py               # Django管理脚本
├── start.py                # 启动脚本
├── sync.py                 # 同步脚本
└── requirements.txt        # 依赖
```

---

## 四、核心模块详解

### 4.1 用户系统 (apps/home)

**模型**：
- `MyUser` - 扩展用户模型，关联 Django 自带 User
  - 字段：real_name, score, age, gender, avatar, signature, user_type, teacher, tel, email, note 等
  - 用户类型：`01-student`(学员), `02-teacher`(教师), `03-admin`(教务), `10-user`(普通用户)
- `Subject` - 已购课包
- `CheckIn` - 打卡记录

**核心函数**：
- `user_check(request)` - 用户登录检查，返回上下文
- `render_md(md)` - Markdown渲染
- `get_notes(myuser, n)` - 获取课程预告和课堂记录

### 4.2 讲义系统 (apps/teach)

**模型**：
- `Item` - 讲义/练习
  - 字段：name, url, path, md5, func_type(lesson/training), item_type, lv, show
  - 通过 md5 实现访问映射

**核心逻辑**：
- 讲义内容存储在 `uploads/statics/lesson/` 和 `uploads/statics/training/`
- 通过 md5 映射真实地址，实现访问控制
- 支持权限检查 `checkSubject(type, context)`

**支持的文件类型**：
- `.pdf` - PDF 文档（iframe 展示）
- `.html` - HTML 页面（iframe 展示）
- `.md` - Markdown 文档（前端渲染）
  - 普通 Markdown：使用 marked.js + highlight.js 渲染
  - Marp 格式：使用 @marp-team/marp-core 渲染为幻灯片

### 4.3 考试系统 (apps/exam)

**模型**：
- `ExamTag` - 考试标签
- `ExamPaper` - 试卷（支持PDF试卷）
- `ExamQuestion` - 题目（单选/多选/判断/填空/编程）
- `ExamRecord` - 考试记录

**题型数据结构**：
```python
QUESTION_TYPES = [
    ('single', '单选题'),
    ('multiple', '多选题'),
    ('true_false', '判断题'),
    ('fill_blank', '填空题'),
    ('programming', '编程题'),
]
```

**核心视图**：
- `paper_list` - 试卷列表（支持标签筛选、搜索、分页）
- `take_exam` - 答题页面
- `exam_result` - 考试结果
- `import_paper` - 导入试卷

### 4.4 知识系统 (apps/blog)

**模型**：
- `BlogTag` - 知识标签
- `Blog` - 知识文章（使用 MDTextField）
- `Series` - 知识系列

### 4.5 教务系统 (apps/service)

**模型**：
- `Lesson_type` - 课程类型
- `Payment` - 缴费记录
- `Classes` - 班级
- `Scheduling` - 排课
- `Lesson_note` - 上课记录
- `Consume_note` - 消课记录
- `Meeting_Note` - 会议记录
- `ClassroomScoreRecord` - 课堂表现记录

### 4.6 Scratch系统 (apps/scratch)

**模型**：
- `ScratchProject` - Scratch项目
- `ProjectComment` - 项目评论
- `ProjectLike` - 项目点赞

---

## 五、配置要点

### 5.1 主配置 (teachzero/settings.py)

```python
INSTALLED_APPS = [
    "apps.simpleui",      # 后台UI（必须放第一个）
    "apps.mdeditor",      # Markdown编辑器
    "apps.home",          # 用户系统
    "apps.teach",         # 讲义
    "apps.exam",          # 考试
    # ... 其他应用
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite",
    }
}

STATICFILES_DIRS = [
    'static/',
    '../uploads/statics/',
    '../uploads/static/',
]
```

### 5.2 用户配置 (teachzero/user_settings.py)

重要配置项：
- `TITLE = "智国学堂"` - 网站标题
- `WELCOMING = "欢迎来到学习的世界"` - 欢迎语
- `INVITE_CODE` - 注册邀请码列表
- `SIMPLEUI_CONFIG` - 后台菜单配置
- `EXAM_CONFIG` - 考试系统配置
- `PATH` - 讲义/训练/博客存储路径

---

## 六、数据流

### 6.1 讲义访问流程

```
用户请求 → /item/{md5} 
         → Item.objects.filter(md5=url) 
         → 获取真实地址 
         → 权限检查 
         → 返回内容
```

### 6.2 考试答题流程

```
用户进入试卷 → 创建/获取ExamRecord 
            → 加载题目 
            → 答题(save_answer API) 
            → 提交(submit_exam API) 
            → 计算得分 
            → 显示结果
```

---

## 七、URL路由结构

| 路径 | 功能 |
|------|------|
| `/` | 首页 |
| `/admin/` | 后台管理 |
| `/blog/` | 知识系统 |
| `/teach/` | 讲义系统 |
| `/exam/` | 考试系统 |
| `/service/` | 教务系统 |
| `/scratch/` | Scratch系统 |
| `/mindmap/` | 思维导图 |
| `/mathgame/` | 数学游戏 |
| `/englishgame/` | 英语游戏 |
| `/clouddisk/` | 云盘 |
| `/tool/` | 工具 |
| `/item/{md5}` | 讲义详情 |

---

## 八、开发规范

### 8.1 视图函数模板

```python
from apps.home.views import user_check

def my_view(request):
    context = user_check(request)  # 获取用户上下文
    # ... 业务逻辑
    return render(request, "app/template.html", context)
```

### 8.2 权限检查

```python
if not request.user.is_authenticated:
    return JsonResponse({"error": "用户未登录"}, status=401)

if not request.user.is_active:
    return JsonResponse({"error": "用户已被禁用"}, status=403)
```

### 8.3 Markdown渲染

```python
from teachzero.user_settings import render_md

html = render_md(md_content)  # 支持表格、代码高亮、数学公式
```

---

## 九、待优化项（来自README）

- 一键爬取题目成本地数据
- 编程题老师后台阅卷评分
- 公有/私有/共享题库
- 题目搜索功能
- 积分功能
- 纠错功能

---

## 十、启动命令

```bash
# 开发环境
python manage.py runserver

# 生产环境
gunicorn -k gevent teachzero.wsgi:application
```

---

## 十、脚本说明

### 10.1 sync.py（数据同步）

```bash
bsync  # 别名：python3 ~/Documents/blog/blog/sync.py
```

功能：
1. 同步工程目录 git 仓库
2. 同步 `uploads/statics/` 下的子仓库（blog, lesson/cpp, lesson/py, lesson/sc, tools, training 等）
3. 清理垃圾文件（.cpp/.c 编译产物等）
4. 调用 `update.py` 更新数据库

### 10.2 update.py（数据库更新）

```bash
python update.py
```

功能：调用 `ItemUpdateManager` 解析讲义文件，更新 `Item` 表

### 10.3 start.py（启动服务）

```bash
python start.py
```

功能：使用 gunicorn 启动 Django 服务
- 绑定地址：`0.0.0.0:12345`
- Worker 数：9
- Worker 类：gevent
- 日志：`~/django_log.txt`

---

## 十一、题目数据结构（JSON）

### 11.1 题型枚举

```python
QUESTION_TYPES = [
    ('single', '单选题'),
    ('multiple', '多选题'),
    ('true_false', '判断题'),
    ('fill_blank', '填空题'),
    ('programming', '编程题'),
]
```

### 11.2 选项格式 (Question.options)

```json
{
    "option1": "内容",
    "option2": {
        "content": "内容",
        "image_url": ["图片地址1", "图片地址2"]
    },
    "option3": "",
    "option4": {
        "title": "标题",
        "type": "single",
        "options": {
            "option1": "内容"
        }
    }
}
```

### 11.3 正确答案格式 (Question.correct_answer)

```json
{
    "option1": 1,
    "option2": "答案文本",
    "option3": "**********",
    "option4": {
        "option1": 1
    }
}
```

> 注：`"**********"` 表示需要人工批改

### 11.4 用户答案格式 (currentAnswer)

```json
{
    "023": {
        "option1": 1,
        "option2": "用户答案"
    }
}
```

---

## 十二、开发约束

### ⚠️ 禁止收集静态文件

```bash
# ❌ 不要运行这个命令
python manage.py collectstatic
```

**原因**：静态文件由用户手动配置，存放在 `static/` 和 `uploads/statics/` 目录。

---

*学习完成时间：2024年*