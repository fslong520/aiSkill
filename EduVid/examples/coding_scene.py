#!/usr/bin/env python3
"""
编程场景示例 - 算法可视化、代码高亮、数据结构
"""

from manim import *


class CodeHighlight(Scene):
    """代码高亮场景"""
    def construct(self):
        # 示例代码
        code_text = '''def fibonacci(n):
    """计算斐波那契数"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)'''
        
        # 创建代码块
        code = Code(
            code=code_text,
            language="python",
            font_size=20,
            line_spacing=1.5
        )
        
        self.play(Write(code))
        self.wait()


class Algorithm(Scene):
    """算法可视化 - 冒泡排序"""
    def construct(self):
        # 创建数据列表
        values = [5, 3, 8, 4, 2, 7, 1, 6]
        
        # 创建柱状图
        bars = VGroup()
        for i, val in enumerate(values):
            bar = Rectangle(
                width=0.6,
                height=val * 0.4,
                color=BLUE,
                fill_opacity=0.8
            )
            bar.move_to(
                LEFT * 3.5 + i * 0.8,
                DOWN * 2 + val * 0.2
            )
            bars.add(bar)
        
        # 标签
        step_label = Text("冒泡排序", font_size=36).to_corner(UP)
        compare_label = Text("", font_size=24).next_to(step_label, DOWN)
        
        self.play(Write(step_label))
        self.play(Create(bars))
        
        # 冒泡排序动画
        arr = values.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # 高亮比较的元素
                bar_j = bars[j]
                bar_j1 = bars[j + 1]
                
                self.play(
                    bar_j.animate.set_color(YELLOW),
                    bar_j1.animate.set_color(YELLOW),
                    run_time=0.3
                )
                
                compare_label.become(
                    Text(f"比较: {arr[j]} > {arr[j+1]}?", font_size=24).next_to(step_label, DOWN)
                )
                
                if arr[j] > arr[j + 1]:
                    # 交换
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    
                    # 动画交换
                    self.play(
                        bar_j.animate.move_to(bar_j1.get_center()),
                        bar_j1.animate.move_to(bar_j.get_center()),
                        run_time=0.5
                    )
                    
                    # 交换VGroup中的位置
                    bars[j], bars[j + 1] = bars[j + 1], bars[j]
                    bar_j, bar_j1 = bar_j1, bar_j
                
                # 恢复颜色
                self.play(
                    bar_j.animate.set_color(BLUE),
                    bar_j1.animate.set_color(BLUE),
                    run_time=0.2
                )
        
        compare_label.become(Text("排序完成!", font_size=24, color=GREEN).next_to(step_label, DOWN))
        self.play(Write(compare_label))
        self.wait()


class DataStructure(Scene):
    """数据结构可视化 - 二叉树"""
    def construct(self):
        # 二叉树节点
        class TreeNode:
            def __init__(self, val):
                self.val = val
                self.left = None
                self.right = None
        
        # 创建二叉树
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.right.left = TreeNode(6)
        root.right.right = TreeNode(7)
        
        # 绘制树
        def draw_tree(node, x, y, level=1):
            if node is None:
                return VGroup()
            
            group = VGroup()
            
            # 节点圆
            circle = Circle(radius=0.3, color=BLUE, fill_opacity=1)
            circle.move_to([x, y, 0])
            
            # 标签
            label = Text(str(node.val), font_size=20, color=WHITE)
            label.move_to(circle.get_center())
            
            group.add(circle)
            group.add(label)
            
            # 子节点
            offset = 3 / (2 ** level)
            
            if node.left:
                left_group = draw_tree(node.left, x - offset, y - 1, level + 1)
                # 连接线
                line = Line(
                    circle.get_bottom(),
                    left_group[0].get_top(),
                    color=GRAY
                )
                group.add(line)
                group.add(left_group)
            
            if node.right:
                right_group = draw_tree(node.right, x + offset, y - 1, level + 1)
                # 连接线
                line = Line(
                    circle.get_bottom(),
                    right_group[0].get_top(),
                    color=GRAY
                )
                group.add(line)
                group.add(right_group)
            
            return group
        
        tree = draw_tree(root, 0, 2)
        
        # 标题
        title = Text("二叉树", font_size=36).to_corner(UP)
        
        self.play(Write(title))
        self.play(Create(tree), run_time=2)
        
        # 遍历动画
        traversal_label = Text("前序遍历: 1 → 2 → 4 → 5 → 3 → 6 → 7", font_size=24)
        traversal_label.move_to(DOWN * 2.5)
        
        self.play(Write(traversal_label))
        self.wait()


class Recursion(Scene):
    """递归可视化 - 阶乘"""
    def construct(self):
        # 标题
        title = Text("递归: 阶乘计算", font_size=36).to_corner(UP)
        
        # 递归调用栈
        stack_frames = VGroup()
        
        frames = [
            ("fact(5)", "调用", "→ fact(4)"),
            ("fact(4)", "调用", "→ fact(3)"),
            ("fact(3)", "调用", "→ fact(2)"),
            ("fact(2)", "调用", "→ fact(1)"),
            ("fact(1)", "返回", "1"),
        ]
        
        for i, (frame, action, result) in enumerate(frames):
            line = Text(f"{frame} {action} {result}", font_size=24)
            line.move_to(LEFT * 2 + UP * 2 - i * 0.5)
            
            if "返回" in action:
                line.set_color(GREEN)
            else:
                line.set_color(BLUE)
            
            stack_frames.add(line)
        
        # 计算过程
        calc_label = Text("计算过程: 5 × 4 × 3 × 2 × 1 = 120", font_size=24, color=ORANGE)
        calc_label.move_to(DOWN * 2)
        
        self.play(Write(title))
        self.play(Create(stack_frames), run_time=2)
        
        # 逐层返回动画
        for i, frame in enumerate(stack_frames):
            if "返回" in frame.submobjects[0].full_text:
                self.play(
                    frame.animate.set_opacity(0.5),
                    run_time=0.3
                )
        
        self.play(Write(calc_label))
        self.wait()


class LinkedList(Scene):
    """链表可视化"""
    def construct(self):
        # 创建链表节点
        nodes = [1, 2, 3, 4, 5]
        node_group = VGroup()
        
        for i, val in enumerate(nodes):
            # 数据块
            data = RoundedRectangle(
                width=0.8,
                height=0.6,
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=1
            )
            
            data_label = Text(str(val), font_size=24, color=WHITE)
            data_label.move_to(data.get_center())
            
            # 指针
            pointer = Triangle(
                direction=RIGHT,
                color=GREEN,
                fill_opacity=1
            )
            pointer.move_to(data.get_right() + RIGHT * 0.1)
            
            node = VGroup(data, data_label, pointer)
            node.move_to(LEFT * 4 + i * 1.2)
            node_group.add(node)
        
        # 箭头连接
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                node_group[i].get_right() + RIGHT * 0.1,
                node_group[i + 1].get_left() - LEFT * 0.2,
                color=YELLOW
            )
            arrows.add(arrow)
        
        # 最后一个节点的NULL指针
        null_label = Text("NULL", font_size=20, color=GRAY)
        null_label.move_to(node_group[-1].get_right() + RIGHT * 0.8)
        
        # 标题
        title = Text("单向链表", font_size=36).to_corner(UP)
        
        self.play(Write(title))
        self.play(Create(node_group), run_time=1)
        self.play(Create(arrows), run_time=1)
        self.play(Write(null_label))
        
        # 高亮遍历
        self.play(
            node_group[0].animate.set_color(YELLOW),
            run_time=0.3
        )
        self.play(
            node_group[0].animate.set_color(BLUE),
            node_group[1].animate.set_color(YELLOW),
            run_time=0.3
        )
        self.wait()


class StackOperations(Scene):
    """栈操作可视化"""
    def construct(self):
        # 栈容器
        stack_box = Rectangle(
            width=1.5,
            height=4,
            color=GRAY,
            stroke_width=2
        )
        stack_label = Text("栈", font_size=24).next_to(stack_box, UP)
        
        # 栈元素
        elements = [1, 2, 3, 4]
        
        self.play(
            Create(stack_box),
            Write(stack_label)
        )
        
        # 入栈动画
        stack = VGroup()
        for i, val in enumerate(elements):
            element = RoundedRectangle(
                width=1.3,
                height=0.6,
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=1
            )
            
            label = Text(str(val), font_size=20, color=WHITE)
            label.move_to(element.get_center())
            
            element.add(label)
            element.move_to(stack_box.get_bottom() + UP * (0.4 + i * 0.7))
            
            self.play(
                Create(element),
                run_time=0.5
            )
            stack.add(element)
        
        # 出栈动画
        self.play(
            stack[-1].animate.move_to(RIGHT * 3),
            run_time=0.5
        )
        self.play(
            FadeOut(stack[-1]),
            stack.remove(stack[-1])
        )
        
        self.play(
            stack[-1].animate.move_to(RIGHT * 3),
            run_time=0.5
        )
        self.play(
            FadeOut(stack[-1]),
            stack.remove(stack[-1])
        )
        
        self.wait()


class GraphTraversal(Scene):
    """图遍历可视化"""
    def construct(self):
        # 创建图节点
        node_positions = {
            'A': [-2, 1, 0],
            'B': [0, 2, 0],
            'C': [2, 1, 0],
            'D': [-1, -1, 0],
            'E': [1, -1, 0]
        }
        
        edges = [
            ('A', 'B'), ('A', 'D'),
            ('B', 'C'), ('B', 'E'),
            ('C', 'E'),
            ('D', 'E')
        ]
        
        # 绘制边
        edge_group = VGroup()
        for start, end in edges:
            line = Line(
                node_positions[start],
                node_positions[end],
                color=GRAY
            )
            edge_group.add(line)
        
        # 绘制节点
        node_group = VGroup()
        for name, pos in node_positions.items():
            circle = Circle(radius=0.35, color=BLUE, fill_opacity=1)
            circle.move_to(pos)
            
            label = Text(name, font_size=24, color=WHITE)
            label.move_to(circle.get_center())
            
            node = VGroup(circle, label)
            node_group.add(node)
        
        # 标题
        title = Text("图的深度优先搜索 (DFS)", font_size=36).to_corner(UP)
        
        self.play(Write(title))
        self.play(Create(edge_group), run_time=1)
        self.play(Create(node_group), run_time=1)
        
        # DFS遍历顺序
        dfs_order = ['A', 'B', 'C', 'E', 'D']
        
        for name in dfs_order:
            node = node_group[int(ord(name) - ord('A'))]
            self.play(
                node.animate.set_color(YELLOW),
                run_time=0.5
            )
        
        self.wait()
