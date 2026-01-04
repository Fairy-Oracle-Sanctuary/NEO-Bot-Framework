"""
日志模块

该模块负责初始化和配置 loguru 日志记录器，为整个应用程序提供统一的日志记录接口。
"""
import sys
from pathlib import Path
from loguru import logger

# 定义日志格式
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 移除 loguru 默认的处理器
logger.remove()

# 添加控制台输出处理器
logger.add(
    sys.stderr,
    level="INFO",
    format=LOG_FORMAT,
    colorize=True,
    enqueue=True  # 异步写入
)

# 定义日志文件路径
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file_path = log_dir / "{time:YYYY-MM-DD}.log"

# 添加文件输出处理器
logger.add(
    log_file_path,
    level="DEBUG",
    format=LOG_FORMAT,
    colorize=False,
    rotation="00:00",  # 每天午夜创建新文件
    retention="7 days",  # 保留最近 7 天的日志
    encoding="utf-8",
    enqueue=True,  # 异步写入
    backtrace=True,  # 记录完整的异常堆栈
    diagnose=True    # 添加异常诊断信息
)

# 导出配置好的 logger
__all__ = ["logger"]
