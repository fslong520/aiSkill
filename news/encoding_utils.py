"""
编码工具模块
统一处理 Windows 下的 UTF-8 编码输出问题
"""
import sys
import io
from contextlib import contextmanager

# 设置标准输出为 UTF-8 模式（Windows 兼容）
def setup_utf8_output():
    """配置标准输出流为 UTF-8 编码"""
    if sys.platform == 'win32':
        # Windows 系统
        try:
            # 尝试使用 UTF-8 模式
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, TypeError):
            # Python < 3.7 的回退方案
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding='utf-8', errors='replace'
            )
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, encoding='utf-8', errors='replace'
            )


def safe_print(msg, end='\n', file=None):
    """
    安全打印函数，自动处理编码问题

    Args:
        msg: 要输出的消息（str 或 bytes）
        end: 结尾字符
        file: 输出文件对象
    """
    if file is None:
        file = sys.stdout

    if isinstance(msg, str):
        # 尝试直接输出
        try:
            print(msg, end=end, file=file)
            return
        except (UnicodeEncodeError, UnicodeError):
            # 如果失败，使用 buffer 方式
            try:
                file.buffer.write(msg.encode('utf-8'))
                if end:
                    file.buffer.write(end.encode('utf-8'))
                file.buffer.flush()
                return
            except Exception:
                # 最后的回退：移除无法编码的字符
                safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
                print(safe_msg, end=end, file=file)
    else:
        print(msg, end=end, file=file)


def safe_write(data, file=None):
    """
    安全写入函数

    Args:
        data: 要写入的数据（str 或 bytes）
        file: 输出文件对象
    """
    if file is None:
        file = sys.stdout

    if isinstance(data, str):
        try:
            file.write(data)
        except (UnicodeEncodeError, UnicodeError):
            file.buffer.write(data.encode('utf-8'))
    else:
        file.write(data)


# 模块加载时自动配置
setup_utf8_output()
