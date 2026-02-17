---
name: 教育视频生成
description: EduVid - AI驱动的教学视频生成器，基于Manim实现自然语言到教学动画的一键转换。支持数学、物理、化学、编程等学科的动态可视化内容生成。
---

# EduVid - AI教学视频生成器

## 工作流程

```
用户输入 → AI理解 → 代码生成 → Manim渲染 → 视频输出
```

### 1. 直接对话生成
直接在对话中描述需求：
```
"生成一个二次函数抛物线动画" → 自动生成代码并渲染
"制作一个水分子旋转视频" → 自动生成代码并渲染
"展示冒泡排序过程" → 自动生成代码并渲染
```

### 2. 命令行生成
```bash
python scripts/generate.py --desc "二次函数y=x²的动画"
python scripts/generate.py --desc "弹簧振子简谐运动"
python scripts/generate.py --desc "甲烷CH4分子结构"
```

## 核心功能

### 智能代码生成
根据自然语言描述自动生成Manim代码：

| 输入示例          | 生成内容            |
|-------------------|---------------------|
| "正弦函数从0到2π" | Axes + sin(x) 图像  |
| "正方形旋转90度"  | Square + Rotate动画 |
| "氢原子电子轨道"  | 原子核 + 电子运动   |
| "二叉树遍历"      | 树结构 + 遍历动画   |

### 支持的学科类型

#### 数学
- 函数图像（一次、二次、三角、指数、对数）
- 几何图形（点、线、面、多边形、圆）
- 几何变换（旋转、平移、缩放、对称）
- 微积分（导数切线、定积分、极限）
- 概率统计（分布、柱状图、散点图）

#### 物理
- 力学（抛体、碰撞、振动）
- 电磁学（电路、磁场、电场）
- 波动（正弦波、干涉、衍射）
- 光学（反射、折射、透镜）

#### 化学
- 分子结构（有机/无机分子）
- 化学反应（反应式、过程动画）
- 原子结构（轨道、电子排布）
- 晶体结构（晶格、晶胞）

#### 编程
- 算法可视化（排序、搜索、递归）
- 数据结构（链表、栈、队列、树、图）
- 代码演示（语法高亮、执行流程）

## 使用方式

### 方式一：对话式（推荐）

直接告诉我你想生成的视频内容：
- "生成正弦函数动画，带坐标轴和标签"
- "制作等边三角形旋转动画"
- "展示快速排序的过程"
- "生成水分子H2O的三维旋转"
- "制作弹簧振子简谐运动"

### 方式二：命令行

```bash
# 进入技能目录
cd $(dirname $(realpath ${BASH_SOURCE[0]}))

# 生成视频
python scripts/generate.py --desc "你的描述"

# 带参数生成
python scripts/generate.py --desc "二次函数动画" --quality high --duration 10
```

### 参数选项

| 参数         | 说明                       | 默认值 |
|--------------|----------------------------|--------|
| `--desc`     | 自然语言描述               | 必需   |
| `--quality`  | 质量：low/medium/high/best | medium |
| `--format`   | 格式：mp4/gif/webm         | mp4    |
| `--fps`      | 帧率：15/30/60             | 30     |
| `--duration` | 时长（秒）                 | 5      |
| `--output`   | 输出文件名                 | auto   |

## 高级用法

### 自定义代码模板

如果生成的代码需要微调，可以：

1. 先生成代码：
```bash
python scripts/generate.py --desc "二次函数" --save-code
```

2. 编辑生成的 `generated_scene.py`

3. 手动渲染：
```bash
python scripts/render.py generated_scene.py
```

### 批量生成

创建配置文件 `batch.yaml`：
```yaml
videos:
  - desc: "正弦函数动画"
    output: sine_wave.mp4
    quality: high
    
  - desc: "冒泡排序"
    output: bubble_sort.mp4
    quality: medium
```

执行：
```bash
python scripts/generate.py --batch batch.yaml
```

## 环境检测与安装

### 检测环境
```bash
python scripts/check_env.py
```

### 安装依赖
```bash
# 完整安装
python scripts/install.py

# conda方式（推荐）
python scripts/install.py --method conda
```

### 手动安装
```bash
# Manim
pip install manim

# 系统依赖（Ubuntu/Debian）
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg texlive-latex-extra

# 中文字体
sudo apt install fonts-noto-cjk
```

## 输出示例

### 生成过程
```
🎬 收到请求: "生成二次函数y=x²的动画"

🤖 正在生成Manim代码...
✓ 代码生成完成

📦 正在渲染视频...
✓ 渲染完成: output/quadratic_20260210_120000.mp4

📁 输出文件: $(dirname $(realpath ${BASH_SOURCE[0]}))/output/quadratic_20260210_120000.mp4
```

### 输出目录结构
```
EduVid/
├── output/
│   ├── quadratic_20260210_120000.mp4
│   ├── sine_wave_20260210_120015.gif
│   └── ...
├── generated/
│   ├── scene_001.py
│   ├── scene_002.py
│   └── ...
```

## 常见问题

### Q: 生成的代码有误怎么办？
A: 使用 `--save-code` 参数保存代码，手动编辑后用 `python scripts/render.py` 渲染

### Q: 如何调整动画时长？
A: 在描述中指定或在命令行添加 `--duration 10`

### Q: 生成的视频太慢？
A: 使用 `--quality low` 或 `--fps 15` 降低渲染要求

### Q: 支持中文字符吗？
A: 支持，已预配置中文字体支持

## 技术原理

### 代码生成流程

1. **意图识别**：解析用户描述，确定学科和场景类型
2. **模板选择**：根据场景选择对应的Manim模板
3. **参数提取**：从描述中提取具体参数（函数、形状、时间等）
4. **代码生成**：填充模板生成可执行Python代码
5. **语法验证**：检查生成的代码语法
6. **渲染执行**：调用Manim渲染最终视频

### 错误处理

| 错误类型 | 处理方式                   |
|----------|----------------------------|
| 环境缺失 | 提示安装步骤               |
| 代码错误 | 保存错误信息，提供修复建议 |
| 渲染失败 | 输出详细日志               |

## 资源链接

- [Manim官方文档](https://docs.manim.org/)
- [Manim示例合集](https://github.com/ManimCommunity/manim/tree/main/examples)
- [manim-physics](https://github.com/ManimCommunity/manim-physics)
