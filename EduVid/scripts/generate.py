#!/usr/bin/env python3
"""
教学视频生成技能 - AI动态代码生成器
根据自然语言描述智能生成Manim代码并渲染
"""

import os
import sys
import re
import subprocess
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class NaturalLanguageParser:
    """自然语言解析器 - 将描述转换为代码生成参数"""
    
    # 关键词映射
    KEYWORDS = {
        # 数学
        "函数": "function",
        "抛物线": "parabola",
        "正弦": "sin",
        "余弦": "cos",
        "正切": "tan",
        "指数": "exp",
        "对数": "log",
        "平方": "square",
        "三角形": "triangle",
        "正方形": "square",
        "圆形": "circle",
        "旋转": "rotate",
        "平移": "translate",
        "缩放": "scale",
        "坐标轴": "axes",
        "导数": "derivative",
        "切线": "tangent",
        "积分": "integral",
        
        # 物理
        "运动": "motion",
        "抛体": "projectile",
        "振动": "oscillation",
        "弹簧": "spring",
        "单摆": "pendulum",
        "电路": "circuit",
        "电阻": "resistor",
        "电流": "current",
        "磁场": "magnetic",
        "电场": "electric",
        "波": "wave",
        "干涉": "interference",
        "反射": "reflection",
        "折射": "refraction",
        
        # 化学
        "分子": "molecule",
        "原子": "atom",
        "电子": "electron",
        "轨道": "orbital",
        "化学键": "bond",
        "反应": "reaction",
        "水": "water",
        "甲烷": "methane",
        "二氧化碳": "co2",
        "氧气": "oxygen",
        
        # 编程
        "排序": "sort",
        "冒泡": "bubble",
        "快速": "quick",
        "二叉树": "binary_tree",
        "链表": "linked_list",
        "栈": "stack",
        "队列": "queue",
        "图": "graph",
        "递归": "recursion",
        "遍历": "traversal",
        
        # 属性
        "动画": "animation",
        "旋转": "rotate",
        "三维": "3d",
        "2d": "2d",
        "颜色": "color",
        "红色": "red",
        "蓝色": "blue",
        "绿色": "green",
        "黄色": "yellow",
    }
    
    def parse(self, description: str) -> Dict:
        """解析自然语言描述"""
        desc_lower = description.lower()
        
        result = {
            "type": "general",
            "subject": "math",
            "params": {},
            "scene_name": "GeneratedScene"
        }
        
        # 识别学科
        if any(w in desc_lower for w in ["分子", "原子", "电子", "化学键", "反应", "甲烷", "水", "H2O", "CO2"]):
            result["subject"] = "chemistry"
            result["type"] = "molecule"
        elif any(w in desc_lower for w in ["电路", "电阻", "电流", "磁场", "电场", "运动", "抛体", "振动", "弹簧"]):
            result["subject"] = "physics"
            result["type"] = "motion"
        elif any(w in desc_lower for w in ["排序", "二叉树", "链表", "栈", "队列", "递归", "遍历", "算法"]):
            result["subject"] = "coding"
            result["type"] = "algorithm"
        else:
            result["subject"] = "math"
            # 识别数学类型
            if any(w in desc_lower for w in ["函数", "抛物线", "sin", "cos", "tan"]):
                result["type"] = "function"
            elif any(w in desc_lower for w in ["三角形", "正方形", "圆形", "旋转", "平移"]):
                result["type"] = "geometry"
            elif any(w in desc_lower for w in ["导数", "切线"]):
                result["type"] = "calculus"
        
        # 提取函数表达式
        func_match = re.search(r'[yfx]\s*[=]\s*([\w\s\^\(\)\*\+/-]+)', desc_lower)
        if func_match:
            result["params"]["func"] = func_match.group(1).strip()
        
        # 提取数字参数
        num_match = re.search(r'(\d+(?:\.\d+)?)', description)
        if num_match:
            result["params"]["value"] = float(num_match.group(1))
        
        # 识别动画时长
        duration_match = re.search(r'(\d+)\s*[秒秒]', description)
        if duration_match:
            result["params"]["duration"] = int(duration_match.group(1))
        
        return result


class ManimCodeGenerator:
    """Manim代码生成器"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """加载代码模板"""
        return {
            # 函数图像模板
            "function": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # 坐标轴
        axes = Axes(
            x_range=[{x_range}],
            y_range=[{y_range}],
            axis_config={{
                "include_tip": True,
                "tips": True
            }}
        )
        
        # 函数图像
        graph = axes.plot(
            lambda x: {func_expr},
            color={color},
            x_range={x_range}
        )
        
        # 标签
        graph_label = axes.get_graph_label(
            graph,
            label="{label}",
            direction={direction}
        )
        
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Write(graph_label))
        self.wait()
''',
            # 几何变换模板
            "geometry": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # 创建几何图形
        shape = {shape_type}({shape_params})
        
        # 动画1: 旋转
        self.play(
            shape.animate.rotate({rotate_angle}),
            run_time=2
        )
        
        # 动画2: 缩放
        self.play(
            shape.animate.scale({scale_factor}),
            run_time=1
        )
        
        # 动画3: 平移
        self.play(
            shape.animate.shift({shift_vector}),
            run_time=1
        )
        
        self.wait()
''',
            # 微积分模板
            "calculus": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # 坐标轴
        axes = Axes(
            x_range={x_range},
            y_range={y_range},
            axis_config={{"include_tip": False}}
        )
        
        # 函数图像
        graph = axes.plot(
            lambda x: {func_expr},
            color=BLUE,
            x_range={x_range}
        )
        
        # 切线
        tangent = axes.get_tangent_line(
            {point_x},
            graph,
            length={length},
            color=RED
        )
        
        # 切点
        point = Dot(axes.c2p({point_x}, {point_y}), color=YELLOW)
        
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(tangent))
        self.play(Create(point))
        self.wait()
''',
            # 物理运动模板
            "motion": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # 创建运动物体
        ball = Circle(radius=0.3, color=RED, fill_opacity=1)
        ball.move_to(ORIGIN)
        
        # 运动参数
        velocity = {velocity}
        angle = {angle}  # 弧度
        g = 9.8
        
        def update_position(mob, dt):
            t = mob.time if hasattr(mob, 'time') else 0
            mob.time = t + dt
            
            # 抛体运动
            vx = velocity * np.cos(angle)
            vy = velocity * np.sin(angle) - g * t * 0.05
            mob.shift(RIGHT * vx * dt + UP * vy * dt)
        
        self.add(ball)
        self.play(
            UpdateFromFunc(ball, update_position),
            run_time={duration},
            rate_func=linear
        )
''',
            # 简谐振动模板
            "oscillation": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # 创建振子
        mass = Square(side_length=0.8, color=RED, fill_opacity=1)
        mass.move_to(RIGHT * 3 + UP * 2)
        
        # 弹簧
        spring = VGroup()
        for i in range(8):
            zigzag = Line(
                UP * (2 - i * 0.3) + LEFT * 0.1,
                UP * (2 - (i + 1) * 0.3) + RIGHT * 0.1,
                color=BLUE
            )
            spring.add(zigzag)
        spring.move_to(RIGHT * 3)
        
        # 简谐运动参数
        amplitude = {amplitude}
        frequency = {frequency}
        
        def update_oscillation(mob, dt):
            t = mob.time if hasattr(mob, 'time') else 0
            mob.time = t + dt
            
            displacement = amplitude * np.sin(frequency * t * 2 * PI)
            mob.move_to(RIGHT * 3 + UP * (displacement + 2))
            
            # 更新弹簧
            spring.renew()  # Simplified
        
        self.add(spring)
        self.add(mass)
        
        self.play(
            UpdateFromFunc(mass, update_oscillation),
            run_time={duration},
            rate_func=linear
        )
''',
            # 分子结构模板
            "molecule": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # {molecule_name} 分子
        atoms = {atoms_config}
        bonds = {bonds_config}
        
        molecule = VGroup(atoms, bonds)
        molecule.move_to(ORIGIN)
        
        # 标签
        label = Text("{molecule_formula}", font_size=36)
        label.to_corner(UL)
        
        self.play(Create(molecule))
        self.play(Write(label))
        
        # 旋转动画
        self.play(
            Rotate(molecule, angle=2*PI),
            run_time={duration}
        )
        
        self.wait()
''',
            # 排序算法模板
            "algorithm": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # {algorithm_name} 排序可视化
        values = {array}
        bars = VGroup()
        
        # 创建柱状图
        for i, val in enumerate(values):
            bar = Rectangle(
                width=0.8,
                height=val * 0.4,
                color=BLUE,
                fill_opacity=0.8
            )
            bar.move_to(
                LEFT * 4 + i * 0.9 + DOWN * 2 + UP * val * 0.2
            )
            bars.add(bar)
        
        self.play(Create(bars))
        
        # {algorithm_name} 排序
        arr = values.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                bar_j, bar_j1 = bars[j], bars[j + 1]
                
                self.play(
                    bar_j.animate.set_color(YELLOW),
                    bar_j1.animate.set_color(YELLOW),
                    run_time=0.3
                )
                
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    
                    # 交换动画
                    self.play(
                        bar_j.animate.move_to(bar_j1.get_center()),
                        bar_j1.animate.move_to(bar_j.get_center()),
                        run_time=0.5
                    )
                    bars[j], bars[j + 1] = bars[j + 1], bars[j]
                
                self.play(
                    bar_j.animate.set_color(BLUE),
                    bar_j1.animate.set_color(BLUE),
                    run_time=0.2
                )
        
        self.play(
            bars.animate.set_color(GREEN),
            run_time=0.5
        )
        
        self.wait()
''',
            # 通用场景
            "general": '''from manim import *

class {scene_name}(Scene):
    def construct(self):
        # {description}
        self.play(Create(Square()))
        self.wait()
''',
        }
    
    def generate(self, parsed: Dict) -> str:
        """根据解析结果生成代码"""
        scene_type = parsed.get("type", "general")
        params = parsed.get("params", {})
        
        if scene_type not in self.templates:
            scene_type = "general"
        
        template = self.templates[scene_type]
        code = template.format(
            scene_name=parsed.get("scene_name", "GeneratedScene"),
            description=parsed.get("description", ""),
            **params
        )
        
        return code


class VideoGenerator:
    """视频生成器"""
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "output"
        self.generated_dir = Path(__file__).parent.parent / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        
        self.parser = NaturalLanguageParser()
        self.generator = ManimCodeGenerator()
    
    def generate(self, description: str, quality: str = "medium",
                 duration: int = 5, format: str = "mp4",
                 fps: int = 30, save_code: bool = False) -> Tuple[bool, str]:
        """
        根据描述生成视频
        
        Args:
            description: 自然语言描述
            quality: 视频质量
            duration: 时长
            format: 输出格式
            fps: 帧率
            save_code: 是否保存代码
            
        Returns:
            (是否成功, 输出路径/错误信息)
        """
        print(f"\n🎬 收到请求: \"{description}\"")
        
        # 1. 解析描述
        print("🔍 正在解析描述...")
        parsed = self.parser.parse(description)
        parsed["params"]["duration"] = duration
        print(f"   类型: {parsed['type']}")
        print(f"   学科: {parsed['subject']}")
        
        # 2. 生成代码
        print("🤖 正在生成Manim代码...")
        code = self.generator.generate(parsed)
        
        # 保存代码（可选）
        if save_code:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            code_file = self.generated_dir / f"scene_{timestamp}.py"
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"   代码已保存: {code_file}")
        
        # 3. 执行Manim渲染
        print("📦 正在渲染视频...")
        success = self._render_code(code, description, quality, format, fps, duration)
        
        if success:
            return True, f"视频生成成功"
        else:
            return False, "渲染失败"
    
    def _render_code(self, code: str, description: str, quality: str,
                     format: str, fps: int, duration: int) -> bool:
        """渲染生成的代码"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py",
                                          delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # 生成时间戳文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{timestamp}_{format}"
            output_path = self.output_dir / output_name
            
            # 构建Manim命令
            cmd = [
                "manim",
                "-ql" if quality == "low" else "-qm" if quality == "medium" else "-qh",
                "-f", format,
                "-o", str(output_path),
                temp_file
            ]
            
            print(f"   执行命令: {' '.join(cmd)}")
            
            # 执行渲染
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                print(f"   ✅ 渲染完成: {output_path}")
                return True
            else:
                print(f"   ❌ 渲染失败:")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("   ❌ 渲染超时（超过5分钟）")
            return False
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return False
        finally:
            # 清理临时文件
            try:
                os.unlink(temp_file)
            except:
                pass


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="根据自然语言描述生成教学视频"
    )
    parser.add_argument(
        "--desc", "-d",
        required=True,
        help="自然语言描述"
    )
    parser.add_argument(
        "--quality", "-q",
        choices=["low", "medium", "high", "best"],
        default="medium",
        help="视频质量"
    )
    parser.add_argument(
        "--duration", "-t",
        type=int,
        default=5,
        help="动画时长（秒）"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["mp4", "gif", "webm"],
        default="mp4",
        help="输出格式"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="帧率"
    )
    parser.add_argument(
        "--save-code", "-s",
        action="store_true",
        help="保存生成的代码"
    )
    
    args = parser.parse_args()
    
    generator = VideoGenerator()
    success, message = generator.generate(
        args.desc,
        quality=args.quality,
        duration=args.duration,
        format=args.format,
        fps=args.fps,
        save_code=args.save_code
    )
    
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
