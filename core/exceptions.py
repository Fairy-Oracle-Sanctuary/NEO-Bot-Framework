"""
自定义异常模块
"""

class SyncHandlerError(Exception):
    """
    当尝试注册同步函数作为异步事件处理器时抛出此异常。
    """
    pass
