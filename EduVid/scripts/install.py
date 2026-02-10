#!/usr/bin/env python3
"""
教学视频生成技能 - 依赖安装脚本
自动安装Manim及所有必要依赖
"""

import subprocess
import sys
import os
import argparse
from typing import List, Optional


class ManimInstaller:
    def __init__(self, method: str = "pip"):
        self.method = method
        self.python = sys.executable
        self.pkg_manager = ""
        
    def detect_system(self) -> str:
        """检测操作系统"""
        if sys.platform.startswith("linux"):
            if os.path.exists("/etc/debian_version"):
                return "debian"
            elif os.path.exists("/etc/redhat-release"):
                return "redhat"
            else:
                return "linux"
        elif sys.platform == "darwin":
            return "macos"
        elif sys.platform == "win32":
            return "windows"
        return "unknown"
    
    def run_command(self, cmd: List[str], description: str, check: bool = True) -> bool:
        """运行命令并显示进度"""
        print(f"\n📦 {description}...")
        print(f"   Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True
            )
            if check and result.returncode != 0:
                print(f"   ✗ Failed with exit code {result.returncode}")
                return False
            print(f"   ✓ Completed")
            return True
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return False
    
    def install_python_deps_pip(self, core: bool = False, extensions: bool = False) -> bool:
        """使用pip安装Python依赖（国内源）"""
        deps = ["manim"]
        
        if extensions:
            deps.extend([
                "manim-physics",
                "manim-chemistry",
                "numpy",
                "scipy"
            ])
        
        # 国内源配置
        pip_args = [
            self.python, "-m", "pip", "install", "--upgrade",
            "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
            "--trusted-host", "pypi.tuna.tsinghua.edu.cn"
        ]
        
        cmd = pip_args + deps
        
        if not self.run_command(cmd, "Installing Manim and dependencies (using Tsinghua mirror)"):
            # 备用阿里云源
            print("   ⚠️  清华源失败，尝试阿里云源...")
            cmd = [
                self.python, "-m", "pip", "install", "--upgrade",
                "-i", "https://mirrors.aliyun.com/pypi/simple/",
                "--trusted-host", "mirrors.aliyun.com"
            ] + deps
            
            if not self.run_command(cmd, "Installing Manim and dependencies (using Aliyun mirror)"):
                return False
        
        return True
    
    def install_python_deps_conda(self, core: bool = False, extensions: bool = False) -> bool:
        """使用conda安装Python依赖（国内源）"""
        deps = ["manim"]
        
        if extensions:
            deps.extend(["numpy", "scipy", "matplotlib"])
        
        # 配置清华conda源
        channels = [
            "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main",
            "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r",
            "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2",
            "conda config --set show_channel_urls yes"
        ]
        
        for channel_cmd in channels:
            try:
                subprocess.run(channel_cmd.split(), capture_output=True)
            except:
                pass
        
        cmd = ["conda", "install", "-y"] + deps
        
        if not self.run_command(cmd, "Installing Manim via conda (using Tsinghua mirror)"):
            return False
        
        return True
    
    def install_system_deps_debian(self) -> bool:
        """安装Debian/Ubuntu系统依赖"""
        deps = [
            "libcairo2-dev",
            "libpango1.0-dev",
            "ffmpeg",
            "texlive-latex-extra",
            "texlive-fonts-extra",
            "texlive-xetex",
            "fonts-noto-cjk",
            "sox"
        ]
        
        cmd = ["sudo", "apt", "install", "-y"] + deps
        
        if not self.run_command(cmd, "Installing system dependencies (Debian/Ubuntu)"):
            return False
        
        return True
    
    def install_system_deps_redhat(self) -> bool:
        """安装RedHat/Fedora系统依赖"""
        deps = [
            "cairo-devel",
            "pango-devel",
            "ffmpeg",
            "texlive-scheme-medium",
            "sox"
        ]
        
        cmd = ["sudo", "dnf", "install", "-y"] + deps
        
        if not self.run_command(cmd, "Installing system dependencies (RedHat/Fedora)"):
            return False
        
        return True
    
    def install_system_deps_macos(self) -> bool:
        """安装macOS系统依赖"""
        # 检查Homebrew
        brew_path = subprocess.run(
            ["which", "brew"],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        if not brew_path:
            print("\n📦 Installing Homebrew...")
            cmd = ["/bin/bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"]
            if not self.run_command(cmd, "Installing Homebrew"):
                return False
        
        # 安装依赖
        deps = ["cairo", "pango", "ffmpeg", "texlive", "basictex"]
        
        cmd = ["brew", "install"] + deps
        
        if not self.run_command(cmd, "Installing dependencies via Homebrew"):
            return False
        
        # 添加texlive路径
        print("\n💡 Note: You may need to add /usr/local/texlive/*/bin to PATH")
        
        return True
    
    def install_system_deps_windows(self) -> bool:
        """Windows系统依赖安装说明"""
        print("""
📦 Windows 依赖安装说明：

1. 下载并安装 MiKTeX: https://miktex.org/download
2. 下载并安装 FFMPEG: https://www.gyan.dev/ffmpeg/builds/
3. 下载并安装 Cairo: https://github.com/preshing/cairo/releases

详细步骤请参考: https://docs.manim.org.cn/getting_started/installation/windows.html
""")
        return True
    
    def create_venv(self) -> bool:
        """创建虚拟环境并配置国内源"""
        venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "venv")
        
        if os.path.exists(venv_path):
            print(f"   Virtual environment already exists at {venv_path}")
            return True
        
        print(f"\n📦 Creating virtual environment...")
        cmd = [sys.executable, "-m", "venv", venv_path]
        
        if not self.run_command(cmd, "Creating virtual environment"):
            return False
        
        # 配置pip国内源
        pip_conf_path = os.path.join(venv_path, "pip.conf" if sys.platform != "win32" else "pip.ini")
        pip_conf_content = """[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
"""
        
        try:
            with open(pip_conf_path, "w") as f:
                f.write(pip_conf_content)
            print(f"   ✓ Configured pip mirror in {pip_conf_path}")
        except:
            print(f"   ⚠️  Failed to configure pip mirror")
        
        print(f"\n💡 激活虚拟环境:")
        if sys.platform == "win32":
            print(f"   {venv_path}\\Scripts\\activate")
        else:
            print(f"   source {venv_path}/bin/activate")
        
        return True
    
    def install(self, core: bool = False, extensions: bool = False) -> bool:
        """执行完整安装"""
        print("\n" + "=" * 60)
        print("教学视频生成 - Manim 安装程序")
        print("=" * 60)
        
        system = self.detect_system()
        print(f"\n🖥️  检测到系统: {system}")
        
        # 安装系统依赖
        print("\n" + "-" * 40)
        print("步骤 1: 安装系统依赖")
        print("-" * 40)
        
        sys_deps_ok = False
        if system == "debian":
            sys_deps_ok = self.install_system_deps_debian()
        elif system == "redhat":
            sys_deps_ok = self.install_system_deps_redhat()
        elif system == "macos":
            sys_deps_ok = self.install_system_deps_macos()
        elif system == "windows":
            sys_deps_ok = self.install_system_deps_windows()
        else:
            print(f"   ⚠️  不支持的系统: {system}")
            print("   请参考官方文档手动安装依赖")
            return False
        
        if not sys_deps_ok:
            print("   ⚠️  系统依赖安装可能存在问题，继续下一步...")
        
        # 安装Python依赖
        print("\n" + "-" * 40)
        print("步骤 2: 安装Python依赖")
        print("-" * 40)
        
        py_deps_ok = False
        if self.method == "conda":
            py_deps_ok = self.install_python_deps_conda(core, extensions)
        else:
            py_deps_ok = self.install_python_deps_pip(core, extensions)
        
        if not py_deps_ok:
            print("   ✗ Python依赖安装失败")
            return False
        
        # 创建虚拟环境（可选）
        print("\n" + "-" * 40)
        print("步骤 3: 创建虚拟环境（可选）")
        print("-" * 40)
        self.create_venv()
        
        # 完成
        print("\n" + "=" * 60)
        print("安装完成！")
        print("=" * 60)
        
        print("\n📚 接下来:")
        print("  1. 运行环境检测: python scripts/check_env.py")
        print("  2. 生成第一个视频: python scripts/generate.py --demo")
        
        print("\n📖 文档链接:")
        print("  - Manim官方文档: https://docs.manim.org.cn/")
        print("  - 示例场景: examples/")
        
        return True
    
    def show_troubleshooting(self) -> None:
        """显示常见问题解决方案"""
        print("""
🔧 常见问题解决：

1. LaTeX 错误
   - 确保已安装完整版 LaTeX (xelatex)
   - Ubuntu: sudo apt install texlive-latex-extra texlive-fonts-extra

2. Cairo 错误
   - Ubuntu: sudo apt install libcairo2-dev libpango1.0-dev
   - macOS: brew install cairo pango

3. 渲染慢
   - 减少场景复杂度
   - 使用 --quality low 参数
   - 关闭阴影和特效

4. 内存不足
   - 降低分辨率: --resolution 720p
   - 减少帧数: --fps 15
   - 缩短时长: --duration 5
""")


def main():
    parser = argparse.ArgumentParser(
        description="Install Manim and dependencies for teaching video generation"
    )
    parser.add_argument(
        "--method",
        choices=["pip", "conda"],
        default="pip",
        help="Package manager to use (default: pip)"
    )
    parser.add_argument(
        "--core",
        action="store_true",
        help="Install only core dependencies"
    )
    parser.add_argument(
        "--extensions",
        action="store_true",
        help="Install physics and chemistry extensions"
    )
    parser.add_argument(
        "--troubleshoot",
        action="store_true",
        help="Show troubleshooting guide"
    )
    
    args = parser.parse_args()
    
    if args.troubleshoot:
        ManimInstaller().show_troubleshooting()
        return 0
    
    installer = ManimInstaller(method=args.method)
    success = installer.install(core=args.core, extensions=args.extensions)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
