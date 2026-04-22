---
name: TeachZero
description: 帮助开发和维护智国学堂（TeachZero）Django教学平台项目
tags: [Django, Python, 教学平台]
icon: https://fslong.iok.la/assets/images/logo.png
author: 智国学堂
url: https://fslong.iok.la:35785

metadata:
  trigger: 智国学堂、TeachZero、Django教学平台、教学平台开发
---

Domain keywords: Django, 智国学堂, TeachZero, 教学平台, 开发维护

Summary: 帮助开发Django教学平台，遵循项目代码风格，提供代码生成、功能扩展、Bug修复能力。

Strategy:
1. 理解需求，定位相关代码
2. 遵循项目规范编写代码
3. 测试验证功能
4. 提交代码（符合commit规范）

AVOID:
- AVOID 不调用user_check获取用户上下文
- AVIEW 权限检查缺失，敏感操作必须验证is_staff/is_authenticated
- AVOID 长文本用TextField，必须用MDTextField
- AVOID 运行collectstatic，静态文件手动配置

---

## 项目配置

| 配置项 | 值 |
|-------|-----|
| 项目路径 | ~/Documents/blog/blog/ |
| 技术栈 | Django 3.2 + SQLite + django-simpleui |
| 虚拟环境 | source venv/bin/activate |

## 项目结构

```
apps/
├── home/      # 用户系统（MyUser, CheckIn）
├── teach/     # 讲义系统（Item）
├── exam/      # 考试系统（ExamPaper, ExamQuestion）
├── blog/      # 知识系统（Blog, Series）
├── service/   # 教务系统（Lesson_type, Classes）
└── scratch/   # Scratch作品

teachzero/
├── settings.py       # 主配置
├── user_settings.py  # 用户配置
└── urls.py           # 主路由
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `python manage.py runserver 0.0.0.0:8000` | 开发服务器 |
| `python manage.py makemigrations && migrate` | 数据库迁移 |
| `python start.py` | 生产环境启动 |
| `bsync` | 同步讲义、博客静态资源 |
| `python update.py` | 更新Item表 |

## 代码模板

### 视图函数
```python
from apps.home.views import user_check

def my_view(request):
    context = user_check(request)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "用户未登录"}, status=401)
    # 业务逻辑
    return render(request, "app/template.html", context)
```

### 模型
```python
from apps.home.models import MyUser
from apps.mdeditor.fields import MDTextField

class MyModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    content = MDTextField(verbose_name="内容", default="")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "模型名称"
        ordering = ['-created_at']
```

### API响应
```python
# 成功
return JsonResponse({"status": 200, "message": "成功", "data": {...}})
# 错误
return JsonResponse({"status": 400, "message": "错误"}, status=400)
```

## Git提交规范

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | 修复bug |
| docs | 文档更新 |
| refactor | 重构代码 |
| perf | 性能优化 |

示例：`git commit -m "feat: 添加错题本导出功能"`

## 测试验证

开发完成后：
1. 启动开发服务器
2. 验证页面访问、功能测试、权限检查
3. 检查控制台无报错
4. 同步数据（bsync）

## 注意事项

- 所有需要用户信息的视图都要调用`user_check(request)`
- 长文本使用`MDTextField`
- 敏感操作必须验证权限
- 模板位置：`apps/{app_name}/templates/{app_name}/`
- 禁止运行`collectstatic`
