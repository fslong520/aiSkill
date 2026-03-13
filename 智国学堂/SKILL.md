---
name: 智国学堂开发技能
description: 帮助开发和维护智国学堂（TeachZero）Django 教学平台项目。
tags: [Django, Python, 教学平台]
icon: https://fslong.iok.la/assets/images/logo.png
author: 智国学堂
url: https://fslong.iok.la:35785
---


# 智国学堂开发技能

帮助开发和维护智国学堂（TeachZero）Django 教学平台项目。

## 项目概述

- **项目路径**：`~/Documents/blog/blog/`
- **技术栈**：Django 3.2 + SQLite + django-simpleui + django-mdeditor
- **定位**：课程服务系统，辅助老师备课和学生管理

## 核心能力

### 1. 代码生成
- 创建新的 Django app
- 编写 Model、View、URL、Template
- 遵循项目现有代码风格

### 2. 功能扩展
- 基于现有模块添加新功能
- 保持与项目架构一致性

### 3. Bug 修复
- 分析错误日志
- 定位问题代码
- 提供修复方案

### 4. 数据库操作
- 编写 migration
- 数据迁移脚本

## 开发规范

### 视图函数模板

```python
from apps.home.views import user_check
from django.http import JsonResponse

def my_view(request):
    """视图函数示例"""
    context = user_check(request)
    
    # 权限检查
    if not request.user.is_authenticated:
        return JsonResponse({"error": "用户未登录"}, status=401)
    
    # 业务逻辑
    # ...
    
    return render(request, "app/template.html", context)
```

### 模型模板

```python
from django.db import models
from apps.home.models import MyUser
from apps.mdeditor.fields import MDTextField

class MyModel(models.Model):
    """模型示例"""
    name = models.CharField(max_length=100, verbose_name="名称")
    content = MDTextField(verbose_name="内容", default="")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "模型名称"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

### API 响应格式

```python
# 成功响应
return JsonResponse({
    "status": 200,
    "message": "操作成功",
    "data": {...}
})

# 错误响应
return JsonResponse({
    "status": 400,
    "message": "错误信息"
}, status=400)
```

## 项目结构速查

```
apps/
├── home/          # 用户系统（MyUser, CheckIn）
├── teach/         # 讲义系统（Item）
├── exam/          # 考试系统（ExamPaper, ExamQuestion, ExamRecord）
├── blog/          # 知识系统（Blog, Series）
├── service/       # 教务系统（Lesson_type, Classes, Scheduling）
├── scratch/       # Scratch作品（ScratchProject）
├── mindmap/       # 思维导图
└── ...

teachzero/
├── settings.py    # 主配置
├── user_settings.py  # 用户配置（TITLE, INVITE_CODE, SIMPLEUI_CONFIG等）
└── urls.py        # 主路由
```

## 常用命令

```bash
# 进入项目目录
cd ~/Documents/blog/blog

# 激活虚拟环境
source venv/bin/activate

# 开发服务器
python manage.py runserver 0.0.0.0:8000

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建管理员
python manage.py createsuperuser

# 生产环境启动（使用 start.py）
python start.py
# 等价于: gunicorn teachzero.wsgi:application --bind 0.0.0.0:12345 --workers 9 --worker-class=gevent

# 数据同步（同步讲义、博客等静态资源并更新数据库）
bsync
# 等价于: python3 ~/Documents/blog/blog/sync.py

# 更新数据库（解析讲义文件并更新 Item 表）
python update.py
```

## 版本控制规范

### 1. 提交前检查

```bash
# 查看修改的文件
git status

# 查看具体修改内容
git diff

# 确认测试通过后再提交
```

### 2. 提交信息格式

```bash
git commit -m "类型: 简短描述"

# 类型说明：
# feat:     新功能
# fix:      修复 bug
# docs:     文档更新
# style:    代码格式调整（不影响功能）
# refactor: 重构代码
# perf:     性能优化
# test:     测试相关
# chore:    构建/工具变动
```

**示例**：
```bash
git commit -m "feat: 添加错题本导出功能"
git commit -m "fix: 修复编程题评分逻辑错误"
git commit -m "refactor: 优化试卷列表查询性能"
```

### 3. 提交粒度

- **一次提交只做一件事**：不要把多个不相关的修改混在一起
- **小步提交**：完成一个小功能就提交，不要积累太多改动
- **确保可运行**：每次提交后项目应能正常运行

### 4. 分支管理

```bash
# 主分支：main / master（生产环境代码）

# 开发新功能
git checkout -b feature/功能名称

# 修复 bug
git checkout -b fix/bug描述

# 合并到主分支前先测试
```

### 5. 推送规范

```bash
# 推送前先拉取最新代码
git pull

# 解决冲突后再推送
git push
```

---

## 测试验证流程

开发完成后，必须按以下步骤验证：

### 1. 启动开发服务器

```bash
cd ~/Documents/blog/blog
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### 2. 验证清单

- [ ] **页面访问**：打开浏览器访问对应页面，确认能正常加载
- [ ] **功能测试**：测试核心功能是否正常工作
- [ ] **数据验证**：检查数据库操作是否正确（增删改查）
- [ ] **权限检查**：测试未登录/普通用户/管理员权限是否生效
- [ ] **错误处理**：测试异常情况是否有友好提示
- [ ] **控制台日志**：查看终端是否有报错信息
- [ ] **浏览器控制台**：F12 检查是否有 JS 错误

### 3. 验证通过标准

- 页面无 500 错误
- 功能符合预期
- 无明显性能问题
- 控制台无报错

### 4. 验证完成后

```bash
# 同步数据（如有新增讲义/博客等）
bsync

# 提交代码前确认
git status
git diff
```

---

## 注意事项

1. **用户上下文**：所有需要用户信息的视图都要调用 `user_check(request)`
2. **Markdown字段**：长文本使用 `MDTextField` 而非 `TextField`
3. **权限检查**：敏感操作必须验证 `request.user.is_staff` 或 `request.user.is_authenticated`
4. **静态文件**：放在 `static/` 或 `uploads/statics/` 目录
5. **模板位置**：各 app 的 templates 放在 `apps/{app_name}/templates/{app_name}/`
6. **⚠️ 禁止收集静态文件**：不要运行 `python manage.py collectstatic`，静态文件由用户手动配置
7. **文档同步**：每次更新开发文档（SKILL.md / PROJECT.md）时，需同步到两个位置：
   - 技能目录：`~/.copaw/active_skills/智国学堂/`
   - 项目目录：`~/Documents/blog/blog/docs/`

## 相关文档

详细架构说明请查看 [PROJECT.md](./PROJECT.md)