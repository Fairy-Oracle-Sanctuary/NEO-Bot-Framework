"""
NEO Bot 主程序入口

负责启动 WebSocket 连接，初始化插件系统，并提供热重载功能。
"""
import asyncio
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 初始化日志系统，必须在其他 core 模块导入之前执行
from core.logger import logger

from core.admin_manager import admin_manager
from core.ws import WS
from core.plugin_manager import load_all_plugins
from core.redis_manager import redis_manager
from core.executor import run_in_thread_pool


class PluginReloadHandler(FileSystemEventHandler):
    """
    文件变更处理器，用于热重载插件

    继承自 watchdog.events.FileSystemEventHandler，
    监听 base_plugins 目录下的文件变化，并触发插件重载。
    """
    def __init__(self):
        """
        初始化处理器
        
        设置冷却时间，防止短时间内多次触发重载。
        """
        self.last_reload_time = 0
        self.cooldown = 1.0  # 冷却时间，防止短时间内多次重载

    def on_any_event(self, event):
        """
        处理所有文件事件

        :param event: watchdog 事件对象
        """
        if event.is_directory:
            return
        
        # 只监控 py 文件
        if not event.src_path.endswith(".py"):
            return
            
        # 过滤掉一些临时文件
        if "__pycache__" in event.src_path:
            return

        # 简单的防抖动
        current_time = time.time()
        if current_time - self.last_reload_time < self.cooldown:
            return
        
        self.last_reload_time = current_time
        
        logger.info(f"检测到文件变更: {event.src_path}")
        logger.info("正在重载插件...")
        
        try:
            # 重新扫描并加载插件
            run_in_thread_pool(load_all_plugins)
            logger.success("插件重载完成")
        except Exception as e:
            logger.exception(f"重载失败: {e}")


@logger.catch
async def main():
    """
    主函数
    
    1. 启动文件监控（热重载）
    2. 初始化 WebSocket 客户端
    3. 建立连接并保持运行
    """
    # 首次加载插件
    await run_in_thread_pool(load_all_plugins)

    # 初始化 Redis 连接
    await redis_manager.initialize()

    # 初始化管理员管理器
    await admin_manager.initialize()

    # 启动文件监控
    # 监控 plugins 目录
    plugin_path = os.path.join(os.path.dirname(__file__), "plugins")
    
    event_handler = PluginReloadHandler()
    observer = Observer()
    
    if os.path.exists(plugin_path):
        observer.schedule(event_handler, plugin_path, recursive=True)
        observer.start()
        logger.info(f"已启动插件热重载监控: {plugin_path}")
    else:
        logger.warning(f"插件目录不存在 {plugin_path}")

    try:
        bot = WS()
        await bot.connect()
    finally:
        if observer.is_alive():
            observer.stop()
            observer.join()


if __name__ == "__main__":
    asyncio.run(main())
