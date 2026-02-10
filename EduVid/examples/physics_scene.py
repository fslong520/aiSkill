#!/usr/bin/env python3
"""
物理场景示例 - 力学、电磁学、波动、光学
注: 需要安装 manim-physics 扩展库
"""

from manim import *
from manim_physics import *


class Mechanics(Scene):
    """力学场景 - 抛体运动"""
    def construct(self):
        # 抛体运动参数
        velocity = 5
        angle = PI / 4  # 45度
        g = 9.8
        
        # 创建运动物体
        ball = Circle(radius=0.3, color=RED, fill_opacity=1)
        ball.move_to(ORIGIN)
        
        # 轨迹
        trajectory = VGroup()
        
        # 初始速度分量
        vx = velocity * np.cos(angle)
        vy = velocity * np.sin(angle)
        
        # 计算运动
        def update_position(mob, dt):
            nonlocal vy
            vy -= g * dt * 0.1  # 缩放时间
            mob.shift(RIGHT * vx * dt * 0.5 + UP * vy * dt * 0.5)
            
            # 添加轨迹点
            dot = Dot(mob.get_center(), color=YELLOW, radius=0.05)
            trajectory.add(dot)
        
        self.add(ball)
        self.play(
            UpdateFromFunc(ball, update_position),
            run_time=3,
            rate_func=linear
        )


class Electromagnetism(Scene):
    """电磁学场景 - 简单电路"""
    def construct(self):
        # 电池
        battery = Rectangle(
            width=0.3, height=1,
            color=RED, fill_opacity=1
        )
        battery_label = Text("+", font_size=24).move_to(battery.get_top() + UP * 0.3)
        
        # 电阻
        resistor = Rectangle(
            width=2, height=0.5,
            color=BLUE, fill_opacity=1
        )
        resistor_zigzag = VGroup()
        for i in range(5):
            segment = Line(
                resistor.get_left() + RIGHT * (0.3 + i * 0.35) + UP * 0.2,
                resistor.get_left() + RIGHT * (0.3 + i * 0.35) + DOWN * 0.2,
                color=BLUE
            )
            resistor_zigzag.add(segment)
        
        # 电流表
        ammeter = Circle(radius=0.4, color=GREEN, fill_opacity=0.3)
        ammeter_label = Text("A", font_size=24).move_to(ammeter.get_center())
        
        # 导线
        wire = Rectangle(
            width=4, height=0.05,
            color=YELLOW
        )
        
        # 排列
        battery.move_to(UP * 2)
        resistor.move_to(RIGHT * 2)
        ammeter.move_to(DOWN * 2)
        wire.move_to(RIGHT * 2)
        
        self.play(
            Create(battery),
            Write(battery_label),
            Create(resistor),
            Create(resistor_zigzag),
            Create(ammeter),
            Write(ammeter_label),
            Create(wire)
        )
        self.wait()


class Wave(Scene):
    """波动场景 - 简谐波"""
    def construct(self):
        # 创建正弦波
        def wave_func(x, t):
            return np.sin(x - t)
        
        axes = Axes(
            x_range=[0, 2*PI, PI/2],
            y_range=[-2, 2, 1],
            axis_config={"include_tip": False}
        )
        
        # 初始波形
        wave = axes.plot(
            lambda x: np.sin(x),
            color=BLUE,
            x_range=[0, 2*PI]
        )
        
        # 动态更新
        def update_wave(mob, dt):
            t = mob.time if hasattr(mob, 'time') else 0
            mob.time = t + dt
            
            # 更新波形
            new_wave = axes.plot(
                lambda x: np.sin(x - t * 2),
                color=BLUE,
                x_range=[0, 2*PI]
            )
            mob.become(new_wave)
        
        self.play(Create(axes))
        self.play(
            UpdateFromFunc(wave, update_wave),
            run_time=5,
            rate_func=linear
        )


class Optics(Scene):
    """光学场景 - 透镜成像"""
    def construct(self):
        # 透镜
        lens = Line(
            UP * 1.5 + RIGHT * 0.1,
            DOWN * 1.5 + RIGHT * 0.1,
            color=BLUE,
            stroke_width=8
        )
        
        # 主光轴
        axis = Line(
            LEFT * 5,
            RIGHT * 5,
            color=GRAY
        )
        
        # 入射光线
        ray1 = Line(LEFT * 4 + UP * 1, lens.get_top(), color=YELLOW, stroke_width=2)
        ray2 = Line(LEFT * 4, ORIGIN, lens.get_center(), color=YELLOW, stroke_width=2)
        
        # 出射光线
        ray1_out = Line(lens.get_top(), RIGHT * 4 + UP * 2, color=YELLOW, stroke_width=2)
        ray2_out = Line(lens.get_center(), RIGHT * 4, ORIGIN, color=YELLOW, stroke_width=2)
        
        # 焦点
        focus1 = Dot(UP * 1 + RIGHT * 1.5, color=RED, radius=0.1)
        focus2 = Dot(DOWN * 1 + RIGHT * 1.5, color=RED, radius=0.1)
        
        # 标签
        focus_label1 = Text("F", font_size=24).next_to(focus1, UP)
        focus_label2 = Text("F", font_size=24).next_to(focus2, DOWN)
        
        self.play(
            Create(axis),
            Create(lens),
            Create(focus1),
            Create(focus2),
            Write(focus_label1),
            Write(focus_label2)
        )
        
        self.play(
            Create(ray1),
            Create(ray2),
            Create(ray1_out),
            Create(ray2_out),
            run_time=2
        )
        self.wait()


class Springs(Scene):
    """弹簧振子"""
    def construct(self):
        # 弹簧
        spring = VGroup()
        spring_segments = 10
        for i in range(spring_segments):
            if i % 2 == 0:
                point = RIGHT * 0.2
            else:
                point = LEFT * 0.2
            segment = Line(
                UP * (1 - i * 0.2),
                UP * (1 - (i + 1) * 0.2) + point,
                color=BLUE
            )
            spring.add(segment)
        
        spring.move_to(ORIGIN + UP * 3)
        
        # 质量块
        mass = Square(side_length=0.8, color=RED, fill_opacity=1)
        mass.move_to(spring.get_bottom())
        
        # 弹簧振子动画
        def update_mass(mob, dt):
            t = mob.time if hasattr(mob, 'time') else 0
            mob.time = t + dt
            
            # 简谐运动
            amplitude = 1.5
            frequency = 2
            displacement = amplitude * np.sin(frequency * t * 2 * PI)
            
            # 更新位置
            new_y = -2 + displacement
            mob.move_to(RIGHT * 3 + UP * new_y)
            
            # 更新弹簧
            spring.move_to(RIGHT * 3 + UP * (new_y + 0.5))
        
        self.add(spring)
        self.add(mass)
        
        self.play(
            UpdateFromFunc(mass, update_mass),
            run_time=4,
            rate_func=linear
        )


class Pendulum(Scene):
    """单摆"""
    def construct(self):
        # 支点
        pivot = Dot(UP * 2, color=BLACK, radius=0.1)
        
        # 摆线
        line = Line(UP * 2, DOWN * 2, color=BLUE)
        
        # 摆锤
        bob = Circle(radius=0.3, color=RED, fill_opacity=1)
        bob.move_to(DOWN * 2)
        
        # 单摆动画
        def update_pendulum(mob, dt):
            t = mob.time if hasattr(mob, 'time') else 0
            mob.time = t + dt
            
            # 简谐运动近似
            amplitude = PI / 6
            frequency = 2
            angle = amplitude * np.sin(frequency * t * 2 * PI)
            
            # 更新摆锤位置
            new_x = 3 * np.sin(angle)
            new_y = -2 * np.cos(angle)
            bob.move_to(RIGHT * new_x + UP * new_y)
            
            # 更新线
            line.put_start_and_end_on(
                UP * 2,
                bob.get_top()
            )
        
        self.add(pivot)
        self.add(line)
        self.add(bob)
        
        self.play(
            UpdateFromFunc(bob, update_pendulum),
            run_time=4,
            rate_func=linear
        )
