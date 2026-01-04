"""
线程池执行器

提供一个全局的线程池和异步接口，用于在事件循环中安全地运行同步函数。
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any, Callable

# 创建一个全局的线程池，可以根据需要调整 max_workers
executor = ThreadPoolExecutor(max_workers=10)

async def run_in_thread_pool(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """
    在线程池中异步运行同步函数

    :param func: 要运行的同步函数
    :param args: 函数的位置参数
    :param kwargs: 函数的关键字参数
    :return: 函数的返回值
    """
    loop = asyncio.get_running_loop()
    # 使用 functools.partial 绑定函数和参数，以便传递给 run_in_executor
    func_to_run = partial(func, *args, **kwargs)
    # loop.run_in_executor 会返回一个 awaitable 对象
    return await loop.run_in_executor(executor, func_to_run)
