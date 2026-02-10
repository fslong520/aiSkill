#!/usr/bin/env python3
"""
数学场景示例 - 包含函数图像、几何变换、微积分、统计可视化
"""

from manim import *


class FunctionPlot(Scene):
    """函数图像绘制场景"""
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 25, 5],
            axis_config={
                "include_tip": True,
                "tips": True,
                "color": WHITE
            }
        )
        
        # 二次函数
        parabola = axes.plot(
            lambda x: x**2,
            color=BLUE,
            x_range=[-3, 3]
        )
        
        # 添加标签
        parabola_label = axes.get_graph_label(
            parabola,
            label="f(x) = x^2",
            direction=UP
        )
        
        self.play(Create(axes))
        self.play(Create(parabola))
        self.play(Write(parabola_label))
        self.wait()


class GeometricTransform(Scene):
    """几何变换场景"""
    def construct(self):
        # 创建正方形
        square = Square(side_length=2, color=BLUE)
        
        # 创建旋转中心点
        rotation_center = ORIGIN
        
        self.play(Create(square))
        
        # 旋转动画
        self.play(
            square.animate.rotate(PI/4),
            run_time=2
        )
        
        # 缩放动画
        self.play(
            square.animate.scale(0.5),
            run_time=1
        )
        
        # 平移动画
        self.play(
            square.animate.shift(RIGHT * 2),
            run_time=1
        )
        
        self.wait()


class Calculus(Scene):
    """微积分场景 - 导数与切线"""
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 10, 2],
            axis_config={"include_tip": False}
        )
        
        # 绘制函数
        graph = axes.plot(
            lambda x: x**2,
            color=BLUE,
            x_range=[-3, 3]
        )
        
        # 在 x=1 处创建切线
        tangent_line = axes.get_tangent_line(
            1,
            graph,
            length=4,
            color=RED
        )
        
        # 点
        point = Dot(axes.c2p(1, 1), color=YELLOW)
        point_label = Text("x=1", font_size=24).next_to(point, UP)
        
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(tangent_line))
        self.play(Create(point))
        self.play(Write(point_label))
        self.wait()


class Statistics(Scene):
    """统计可视化 - 正态分布"""
    def construct(self):
        # 正态分布曲线
        def normal(x, mu=0, sigma=1):
            return (1 / (sigma * np.sqrt(2 * PI))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
        
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"include_tip": False}
        )
        
        # 绘制正态分布
        normal_graph = axes.plot(
            normal,
            color=BLUE,
            x_range=[-4, 4]
        )
        
        # 填充区域
        area = axes.get_graph(
            normal,
            color=BLUE,
            x_range=[-1, 1]
        ).set_fill(BLUE, opacity=0.3)
        
        # 标签
        label = Text("正态分布", font_size=36).to_corner(UL)
        
        self.play(Create(axes))
        self.play(Create(normal_graph))
        self.play(FadeIn(area))
        self.play(Write(label))
        self.wait()


class TrigonometricFunctions(Scene):
    """三角函数可视化"""
    def construct(self):
        axes = Axes(
            x_range=[-2*PI, 2*PI, PI/2],
            y_range=[-2, 2, 0.5],
            axis_config={
                "include_tip": False,
                "numbers_to_include": np.arange(-2*PI, 3*PI, PI)
            }
        )
        
        # 正弦函数
        sine = axes.plot(
            lambda x: np.sin(x),
            color=BLUE,
            x_range=[-2*PI, 2*PI]
        )
        
        # 余弦函数
        cosine = axes.plot(
            lambda x: np.cos(x),
            color=RED,
            x_range=[-2*PI, 2*PI]
        )
        
        # 标签
        sine_label = axes.get_graph_label(sine, label="sin(x)")
        cosine_label = axes.get_graph_label(cosine, label="cos(x)", direction=DOWN)
        
        self.play(Create(axes))
        self.play(Create(sine))
        self.play(Create(cosine))
        self.play(Write(sine_label))
        self.play(Write(cosine_label))
        self.wait()


class LinearEquations(Scene):
    """线性方程组可视化"""
    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_tip": False}
        )
        
        # 两条直线
        line1 = axes.plot(
            lambda x: 2*x + 1,
            color=BLUE,
            x_range=[-3, 2]
        )
        
        line2 = axes.plot(
            lambda x: -x + 3,
            color=RED,
            x_range=[-3, 5]
        )
        
        # 交点
        intersection = Dot(axes.c2p(2/3, 7/3), color=YELLOW, radius=0.2)
        intersection_label = Text(
            "x = 2/3\ny = 7/3",
            font_size=24
        ).next_to(intersection, UR)
        
        self.play(Create(axes))
        self.play(Create(line1))
        self.play(Create(line2))
        self.play(Create(intersection))
        self.play(Write(intersection_label))
        self.wait()


class GeometricShapes(Scene):
    """基本几何图形"""
    def construct(self):
        # 创建各种图形
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=1.5, color=RED)
        triangle = Triangle(color=GREEN)
        rectangle = Rectangle(width=2, height=1, color=YELLOW)
        
        # 排列图形
        circle.move_to(LEFT * 3)
        square.move_to(LEFT)
        triangle.move_to(RIGHT)
        rectangle.move_to(RIGHT * 3)
        
        # 标签
        labels = VGroup(
            Text("圆", font_size=24).next_to(circle, DOWN),
            Text("正方形", font_size=24).next_to(square, DOWN),
            Text("三角形", font_size=24).next_to(triangle, DOWN),
            Text("长方形", font_size=24).next_to(rectangle, DOWN)
        )
        
        self.play(
            Create(circle),
            Create(square),
            Create(triangle),
            Create(rectangle)
        )
        self.play(Write(labels))
        self.wait()


class Vectors(Scene):
    """向量可视化"""
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_tip": False}
        )
        
        # 向量
        vector1 = Arrow(
            start=ORIGIN,
            end=UP * 2 + RIGHT * 3,
            color=BLUE,
            buff=0
        )
        
        vector2 = Arrow(
            start=ORIGIN,
            end=UP * 1 + RIGHT * 4,
            color=RED,
            buff=0
        )
        
        # 向量和
        vector_sum = Arrow(
            start=ORIGIN,
            end=vector1.get_end() + vector2.get_end(),
            color=GREEN,
            buff=0
        )
        
        # 标签
        v1_label = Text("v₁", font_size=24, color=BLUE).next_to(vector1.get_end(), UR)
        v2_label = Text("v₂", font_size=24, color=RED).next_to(vector2.get_end(), UR)
        sum_label = Text("v₁ + v₂", font_size=24, color=GREEN).next_to(vector_sum.get_end(), UR)
        
        self.play(Create(axes))
        self.play(Create(vector1))
        self.play(Create(vector2))
        self.play(Create(vector_sum))
        self.play(Write(v1_label))
        self.play(Write(v2_label))
        self.play(Write(sum_label))
        self.wait()
