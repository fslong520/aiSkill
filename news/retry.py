"""
重试机制和异常处理
"""
import time
import functools
from typing import Callable, TypeVar, Optional
from logger import get_logger

T = TypeVar("T")

class MaxRetriesExceededError(Exception):
    """超过最大重试次数"""
    pass

def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
    on_failure: Optional[Callable] = None,
):
    """
    重试装饰器

    Args:
        max_attempts: 最大尝试次数
        delay: 初始延迟（秒）
        backoff_factor: 退避因子
        exceptions: 需要重试的异常类型
        on_failure: 失败时的回调函数
    """
    logger = get_logger()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} 第 {attempt}/{max_attempts} 次尝试失败: {str(e)}"
                    )

                    if attempt < max_attempts:
                        logger.info(f"等待 {current_delay:.1f} 秒后重试...")
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(f"{func.__name__} 达到最大重试次数")

            # 所有尝试都失败
            if on_failure:
                return on_failure(*args, **kwargs)

            raise MaxRetriesExceededError(
                f"{func.__name__} 在 {max_attempts} 次尝试后仍然失败"
            ) from last_exception

        return wrapper
    return decorator


def safe_execute(
    func: Callable[..., T],
    default_value: T = None,
    log_error: bool = True,
    raise_on_error: bool = False,
) -> T:
    """
    安全执行函数，捕获所有异常

    Args:
        func: 要执行的函数
        default_value: 失败时的默认返回值
        log_error: 是否记录错误日志
        raise_on_error: 是否重新抛出异常

    Returns:
        函数执行结果或默认值
    """
    logger = get_logger()

    try:
        return func()
    except Exception as e:
        if log_error:
            logger.error(f"执行失败: {func.__name__}", exc_info=True)
        if raise_on_error:
            raise
        return default_value


class RequestErrorHandler:
    """请求错误处理器"""

    def __init__(self):
        self.logger = get_logger()
        self.error_counts = {}
        self.last_errors = {}

    def record_error(self, source: str, error: Exception):
        """记录错误"""
        source_key = source.lower()
        self.error_counts[source_key] = self.error_counts.get(source_key, 0) + 1
        self.last_errors[source_key] = {
            "error": str(error),
            "type": type(error).__name__,
            "timestamp": time.time()
        }
        self.logger.error(f"{source} 请求错误: {str(error)}")

    def get_error_stats(self, source: str) -> dict:
        """获取错误统计"""
        source_key = source.lower()
        return {
            "count": self.error_counts.get(source_key, 0),
            "last_error": self.last_errors.get(source_key)
        }

    def should_disable_source(self, source: str, threshold: int = 10) -> bool:
        """判断是否应该禁用某个数据源"""
        source_key = source.lower()
        return self.error_counts.get(source_key, 0) >= threshold

    def reset(self, source: Optional[str] = None):
        """重置错误统计"""
        if source:
            source_key = source.lower()
            self.error_counts.pop(source_key, None)
            self.last_errors.pop(source_key, None)
        else:
            self.error_counts.clear()
            self.last_errors.clear()


# 全局错误处理器
error_handler = RequestErrorHandler()
