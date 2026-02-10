#!/usr/bin/env python3
"""
教学视频生成技能 - 环境检测脚本
检查系统是否满足Manim运行要求
"""

import subprocess
import sys
import shutil
from typing import Tuple, Dict, List


class EnvironmentChecker:
    def __init__(self):
        self.results = {}
        
    def check_command(self, command: str) -> Tuple[bool, str]:
        """检查命令是否存在"""
        result = shutil.which(command)
        if result:
            return True, result
        return False, ""
    
    def check_python_package(self, package: str) -> Tuple[bool, str]:
        """检查Python包是否已安装"""
        try:
            result = subprocess.run(
                [sys.executable, "-c", f"import {package}; print({package}.__version__)"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, version
        except Exception:
            pass
        return False, ""
    
    def check_manim(self) -> Dict:
        """检查Manim安装状态"""
        status = {}
        
        # 检查Python版本
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        status["python"] = {
            "installed": True,
            "version": py_version,
            "required": ">=3.8",
            "ok": sys.version_info >= (3, 8)
        }
        
        # 检查Manim
        manim_ok, manim_ver = self.check_python_package("manim")
        status["manim"] = {
            "installed": manim_ok,
            "version": manim_ver if manim_ok else None,
            "ok": manim_ok
        }
        
        # 检查manim-physics
        physics_ok, physics_ver = self.check_python_package("manim_physics")
        status["manim_physics"] = {
            "installed": physics_ok,
            "version": physics_ver if physics_ok else None,
            "ok": True,  # optional
            "optional": True
        }
        
        # 检查manim-chemistry
        chem_ok, chem_ver = self.check_python_package("manim_chemistry")
        status["manim_chemistry"] = {
            "installed": chem_ok,
            "version": chem_ver if chem_ok else None,
            "ok": True,  # optional
            "optional": True
        }
        
        return status
    
    def check_system_deps(self) -> Dict:
        """检查系统依赖"""
        status = {}
        
        # 检查Cairo
        cairo_ok, cairo_ver = self.check_command("cairo")
        status["cairo"] = {
            "installed": cairo_ok,
            "version": cairo_ver if cairo_ok else "unknown",
            "required": "Yes"
        }
        
        # 检查FFMPEG
        ffmpeg_ok, ffmpeg_ver = self.check_command("ffmpeg")
        status["ffmpeg"] = {
            "installed": ffmpeg_ok,
            "version": "unknown" if not ffmpeg_ok else "installed",
            "required": "Yes"
        }
        
        # 检查LaTeX
        latex_ok = False
        latex_cmds = ["xelatex", "lualatex", "pdflatex"]
        for cmd in latex_cmds:
            if self.check_command(cmd)[0]:
                latex_ok = True
                break
        status["latex"] = {
            "installed": latex_ok,
            "version": "unknown",
            "required": "Yes"
        }
        
        # 检查Pango
        pango_ok, _ = self.check_command("pango")
        status["pango"] = {
            "installed": pango_ok,
            "required": "Yes"
        }
        
        return status
    
    def check_sox(self) -> Dict:
        """检查SoX（可选，用于音频）"""
        sox_ok, _ = self.check_command("sox")
        return {
            "installed": sox_ok,
            "required": "No (optional)",
            "optional": True
        }
    
    def run_check(self) -> Dict:
        """执行完整的环境检测"""
        results = {
            "python": self.check_manim(),
            "system": self.check_system_deps(),
            "optional": {
                "sox": self.check_sox()
            }
        }
        
        # 计算总体状态
        all_required_ok = True
        for key in ["python"]:
            if not results[key].get("manim", {}).get("ok", False):
                all_required_ok = False
                break
        
        for key in ["system"]:
            for dep_key, dep_status in results[key].items():
                if not dep_status.get("optional", False):
                    if not dep_status.get("installed", False):
                        all_required_ok = False
        
        results["status"] = "READY" if all_required_ok else "NEEDS_INSTALL"
        return results
    
    def print_report(self, results: Dict):
        """打印环境检测报告"""
        print("\n" + "=" * 60)
        print("教学视频生成环境检测")
        print("=" * 60)
        
        # Python环境
        print("\n📦 Python 环境:")
        py_info = results["python"]
        print(f"  Python: {py_info['python']['version']} (required: {py_info['python']['required']})")
        
        manim_info = py_info["manim"]
        icon = "✓" if manim_info["ok"] else "✗"
        print(f"  {icon} Manim: {manim_info['version'] if manim_info['installed'] else 'NOT INSTALLED'}")
        
        for pkg in ["manim_physics", "manim_chemistry"]:
            if pkg in py_info:
                info = py_info[pkg]
                icon = "✓" if info["installed"] else "○"
                print(f"  {icon} {pkg}: {info['version'] if info['installed'] else 'not installed (optional)'}")
        
        # 系统依赖
        print("\n🔧 系统依赖:")
        for dep_name, dep_info in results["system"].items():
            icon = "✓" if dep_info.get("installed", False) else "✗"
            required = dep_info.get("required", "")
            print(f"  {icon} {dep_name}: {'installed' if dep_info.get('installed') else 'NOT INSTALLED'} ({required})")
        
        # 可选依赖
        print("\n📋 可选依赖:")
        for dep_name, dep_info in results["optional"].items():
            icon = "✓" if dep_info.get("installed", False) else "○"
            print(f"  {icon} {dep_name}: {'installed' if dep_info.get('installed') else 'not installed'}")
        
        # 总体状态
        print("\n" + "=" * 60)
        print(f"环境状态: {results['status']}")
        print("=" * 60)
        
        if results["status"] != "READY":
            print("\n💡 建议安装命令:")
            print("  python scripts/install.py --method conda")
            print("  或")
            print("  python scripts/install.py --method pip")
        
        return results


def main():
    checker = EnvironmentChecker()
    results = checker.run_check()
    checker.print_report(results)
    
    # 返回退出码
    return 0 if results["status"] == "READY" else 1


if __name__ == "__main__":
    sys.exit(main())
