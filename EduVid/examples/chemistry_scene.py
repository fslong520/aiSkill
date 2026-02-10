#!/usr/bin/env python3
"""
化学场景示例 - 分子结构、化学反应、原子结构
注: 需要安装 manim-chemistry 扩展库
"""

from manim import *

# 注意: 完整的化学扩展需要额外的安装
# 以下是使用基本Manim实现的化学可视化


class Molecule(Scene):
    """分子结构场景 - 水分子"""
    def construct(self):
        # 氧原子
        oxygen = Circle(radius=0.5, color=RED, fill_opacity=1)
        oxygen_label = Text("O", font_size=36, color=WHITE)
        oxygen_label.move_to(oxygen.get_center())
        
        # 氢原子
        hydrogen1 = Circle(radius=0.3, color=WHITE, fill_opacity=1)
        hydrogen1.move_to(UP * 0.8 + LEFT * 0.6)
        h1_label = Text("H", font_size=24, color=BLACK)
        h1_label.move_to(hydrogen1.get_center())
        
        hydrogen2 = Circle(radius=0.3, color=WHITE, fill_opacity=1)
        hydrogen2.move_to(UP * 0.8 + RIGHT * 0.6)
        h2_label = Text("H", font_size=24, color=BLACK)
        h2_label.move_to(hydrogen2.get_center())
        
        # 键
        bond1 = Line(
            oxygen.get_center() + DOWN * 0.2,
            hydrogen1.get_center() + DOWN * 0.1,
            color=GRAY,
            stroke_width=4
        )
        
        bond2 = Line(
            oxygen.get_center() + DOWN * 0.2,
            hydrogen2.get_center() + DOWN * 0.1,
            color=GRAY,
            stroke_width=4
        )
        
        # 分子标签
        molecule_label = Text("H₂O", font_size=48).to_corner(UL)
        
        self.play(
            Create(bond1),
            Create(bond2),
            Create(oxygen),
            Write(oxygen_label),
            Create(hydrogen1),
            Write(h1_label),
            Create(hydrogen2),
            Write(h2_label)
        )
        self.play(Write(molecule_label))
        
        # 旋转动画
        self.play(
            Rotate(VGroup(oxygen, hydrogen1, hydrogen2, bond1, bond2), PI/2),
            run_time=2
        )
        self.wait()


class Reaction(Scene):
    """化学反应场景 - 燃烧"""
    def construct(self):
        # 甲烷分子
        carbon = Circle(radius=0.4, color=GRAY, fill_opacity=1)
        c_label = Text("C", font_size=24, color=WHITE)
        c_label.move_to(carbon.get_center())
        
        hydrogens = VGroup()
        for i, angle in enumerate([0, PI/2, PI, 3*PI/2]):
            h = Circle(radius=0.25, color=WHITE, fill_opacity=1)
            h.move_to(0.6 * np.cos(angle), 0.6 * np.sin(angle))
            h_label = Text("H", font_size=18, color=BLACK)
            h_label.move_to(h.get_center())
            hydrogens.add(h)
            hydrogens.add(h_label)
        
        hydrogens.add(carbon)
        hydrogens.add(c_label)
        hydrogens.move_to(LEFT * 3)
        
        # 氧气分子
        o2_label = Text("O₂", font_size=36)
        o2_label.move_to(RIGHT * 3)
        
        # 反应箭头
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color=YELLOW)
        arrow_label = Text("燃烧", font_size=24).next_to(arrow, UP)
        
        # 产物
        co2_label = Text("CO₂ + 2H₂O", font_size=36, color=BLUE)
        co2_label.move_to(DOWN * 2)
        
        self.play(
            Create(hydrogens),
            Write(o2_label)
        )
        
        self.play(
            Create(arrow),
            Write(arrow_label)
        )
        
        self.play(
            FadeOut(hydrogens),
            FadeOut(o2_label),
            FadeOut(arrow),
            FadeOut(arrow_label),
            Write(co2_label)
        )
        
        self.wait()


class AtomicStructure(Scene):
    """原子结构场景"""
    def construct(self):
        # 原子核
        nucleus = VGroup()
        for i in range(6):  # 6个质子/中子
            proton = Circle(radius=0.15, color=RED, fill_opacity=1)
            neutron = Circle(radius=0.15, color=GRAY, fill_opacity=1)
            # 随机位置
            proton.move_to(np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3))
            neutron.move_to(np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3))
            nucleus.add(proton)
            nucleus.add(neutron)
        
        nucleus.move_to(ORIGIN)
        
        # 电子轨道
        orbits = VGroup()
        for i in range(3):
            orbit = Circle(radius=0.8 + i * 0.5, color=BLUE, stroke_width=1)
            orbit.set_fill(BLUE, opacity=0.05)
            orbits.add(orbit)
        
        # 电子
        electrons = VGroup()
        for i in range(6):  # 6个电子
            angle = i * PI / 3
            electron = Circle(radius=0.08, color=YELLOW, fill_opacity=1)
            electron.move_to(
                np.cos(angle) * (0.8 + (i % 3) * 0.5),
                np.sin(angle) * (0.8 + (i % 3) * 0.5)
            )
            electrons.add(electron)
        
        # 标签
        label = Text("碳原子 (C)", font_size=36).to_corner(UL)
        
        self.play(
            Create(nucleus),
            run_time=2
        )
        
        self.play(
            Create(orbits),
            run_time=1
        )
        
        self.play(
            Create(electrons),
            run_time=1
        )
        
        self.play(Write(label))
        
        # 轨道旋转
        self.play(
            Rotate(orbits, PI/2),
            Rotate(electrons, PI/2),
            run_time=2
        )
        self.wait()


class BondTypes(Scene):
    """化学键类型"""
    def construct(self):
        # 标题
        title = Text("化学键类型", font_size=48).to_corner(UP)
        
        # 共价键 - 原子靠近
        atom1 = Circle(radius=0.4, color=BLUE, fill_opacity=1)
        atom2 = Circle(radius=0.4, color=RED, fill_opacity=1)
        atom1.move_to(LEFT * 3 + UP)
        atom2.move_to(RIGHT * 3 + UP)
        
        covalent_bond = Line(
            atom1.get_right(),
            atom2.get_left(),
            color=YELLOW,
            stroke_width=6
        )
        
        covalent_label = Text("共价键", font_size=24).next_to(
            VGroup(atom1, atom2, covalent_bond), DOWN
        )
        
        # 离子键 - 电子转移
        na_circle = Circle(radius=0.4, color=BLUE, fill_opacity=1).move_to(LEFT * 3 + DOWN)
        cl_circle = Circle(radius=0.4, color=GREEN, fill_opacity=1).move_to(RIGHT * 3 + DOWN)
        
        electron = Circle(radius=0.1, color=YELLOW, fill_opacity=1)
        electron.move_to(LEFT * 3 + DOWN + RIGHT * 0.2)
        
        ionic_arrow = Arrow(
            electron.get_right(),
            cl_circle.get_left(),
            color=YELLOW
        )
        
        ionic_label = Text("离子键", font_size=24).next_to(
            VGroup(na_circle, cl_circle), DOWN
        )
        
        # 金属键
        metal_atoms = VGroup()
        for i in range(3):
            for j in range(3):
                atom = Circle(
                    radius=0.25,
                    color=GRAY,
                    fill_opacity=1
                ).move_to(
                    LEFT * 1 + i * 0.6 + DOWN * 0.6 + j * 0.6
                )
                metal_atoms.add(atom)
        metal_atoms.move_to(DOWN * 2)
        
        # 自由电子
        free_electrons = VGroup()
        for i in range(8):
            e = Circle(radius=0.05, color=YELLOW, fill_opacity=1)
            e.move_to(
                np.random.uniform(-1, 1),
                np.random.uniform(-0.8, 0.8)
            )
            free_electrons.add(e)
        
        metal_label = Text("金属键", font_size=24).next_to(metal_atoms, DOWN)
        
        self.play(Write(title))
        
        self.play(
            Create(atom1),
            Create(atom2),
            Create(covalent_bond),
            Write(covalent_label)
        )
        
        self.play(
            Create(na_circle),
            Create(cl_circle),
            Create(electron),
            Create(ionic_arrow),
            Write(ionic_label)
        )
        
        self.play(
            Create(metal_atoms),
            Create(free_electrons),
            Write(metal_label)
        )
        
        self.wait()


class PeriodicTable(Scene):
    """元素周期表示意"""
    def construct(self):
        # 创建元素卡片
        elements = [
            ("H", "氢", 1.008),
            ("He", "氦", 4.003),
            ("Li", "锂", 6.941),
            ("Be", "铍", 9.012),
            ("B", "硼", 10.81),
        ]
        
        cards = VGroup()
        for i, (symbol, name, mass) in enumerate(elements):
            card = RoundedRectangle(
                width=1.2,
                height=1.2,
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=0.3
            )
            
            symbol_text = Text(symbol, font_size=36, color=WHITE)
            symbol_text.move_to(card.get_center() + UP * 0.2)
            
            name_text = Text(name, font_size=16)
            name_text.move_to(card.get_center() - UP * 0.3)
            
            card.add(symbol_text)
            card.add(name_text)
            
            card.move_to(LEFT * 4 + i * 1.3)
            cards.add(card)
        
        # 标题
        title = Text("元素周期表示意", font_size=36).to_corner(UP)
        
        self.play(Write(title))
        self.play(Create(cards), run_time=2)
        self.wait()


class CrystalStructure(Scene):
    """晶体结构"""
    def construct(self):
        # 创建晶格点
        def create_lattice_point(x, y, color=BLUE):
            point = Dot(
                [x, y, 0],
                radius=0.15,
                color=color
            )
            return point
        
        # 二维晶格
        lattice = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                point = create_lattice_point(i * 0.8, j * 0.8)
                lattice.add(point)
        
        # 连接线
        bonds = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i < 2:
                    line = Line(
                        [i * 0.8, j * 0.8, 0],
                        [(i + 1) * 0.8, j * 0.8, 0],
                        color=GRAY,
                        stroke_width=1
                    )
                    bonds.add(line)
                if j < 2:
                    line = Line(
                        [i * 0.8, j * 0.8, 0],
                        [i * 0.8, (j + 1) * 0.8, 0],
                        color=GRAY,
                        stroke_width=1
                    )
                    bonds.add(line)
        
        # 标签
        label = Text("晶体结构", font_size=36).to_corner(UL)
        
        self.play(Write(label))
        self.play(Create(bonds), run_time=1)
        self.play(Create(lattice), run_time=1)
        
        # 旋转效果
        self.play(
            Rotate(lattice, PI/4),
            Rotate(bonds, PI/4),
            run_time=2
        )
        self.wait()
