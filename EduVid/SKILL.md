---
name: 教学视频
description: EduVid - AI驱动的教学视频生成器，基于Manim实现自然语言到教学动画的一键转换

metadata:
  slug: eduvid
  trigger: EduVid、教学视频、动画生成、Manim、数学可视化、物理动画、教育视频
---

## Keywords

Manim, 教学视频, 动画生成, 数学可视化, 物理动画, 教育视频, 视频生成, 教学动画

## Summary

自然语言描述→Manim代码生成→视频渲染，支持数学、物理、化学、编程等学科。

## Strategy
1. 理解用户描述，识别学科和场景类型
2. 生成Manim代码
3. 调用Manim渲染视频
4. 输出到output/目录

AVOID:
- AVOID 生成代码不验证语法，必须检查
- AVOID 渲染失败不提供修复建议
- AVOID 中文不配置字体，必须预装fonts-noto-cjk

---

## 工作流程

```
用户输入 → AI理解 → 代码生成 → Manim渲染 → 视频输出
```

## 使用方式

### 方式一：对话式（推荐）
直接描述需求：
- "生成正弦函数动画，带坐标轴和标签"
- "制作等边三角形旋转动画"
- "展示快速排序的过程"
- "生成水分子H2O的三维旋转"

### 方式二：命令行
```bash
cd $(dirname $(realpath ${BASH_SOURCE[0]}))
python scripts/generate.py --desc "你的描述"
```

## 参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--desc` | 自然语言描述 | 必需 |
| `--quality` | 质量：low/medium/high/best | medium |
| `--format` | 格式：mp4/gif/webm | mp4 |
| `--fps` | 帧率：15/30/60 | 30 |
| `--duration` | 时长（秒） | 5 |

## 支持的学科

| 学科 | 示例 |
|------|------|
| 数学 | 函数图像、几何变换、微积分、概率统计 |
| 物理 | 力学、电磁学、波动、光学 |
| 化学 | 分子结构、化学反应、原子结构 |
| 编程 | 算法可视化、数据结构、代码演示 |

## 高级用法

### 保存代码后手动编辑
```bash
python scripts/generate.py --desc "二次函数" --save-code
# 编辑 generated_scene.py
python scripts/render.py generated_scene.py
```

### 批量生成
```yaml
# batch.yaml
videos:
  - desc: "正弦函数动画"
    output: sine_wave.mp4
  - desc: "冒泡排序"
    output: bubble_sort.mp4
```
```bash
python scripts/generate.py --batch batch.yaml
```

## 环境安装

```bash
# 检测环境
python scripts/check_env.py

# 完整安装
pip install manim
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg texlive-latex-extra
sudo apt install fonts-noto-cjk  # 中文字体
```

## 输出目录

```
EduVid/
├── output/          # 视频输出
│   └── xxx_20260210_120000.mp4
└── generated/       # 生成的代码
    └── scene_001.py
```

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 代码有误 | `--save-code`保存后手动编辑 |
| 视频太慢 | `--quality low`或`--fps 15` |
| 中文乱码 | 安装fonts-noto-cjk |
