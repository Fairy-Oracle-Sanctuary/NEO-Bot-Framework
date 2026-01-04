import redis.asyncio as redis
from .config_loader import global_config as config
from .logger import logger

class RedisManager:
    """
    Redis 连接管理器（异步单例）
    """
    _instance = None
    _redis = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self):
        """
        异步初始化 Redis 连接并进行健康检查
        """
        if self._redis is None:
            try:
                host = config.redis['host']
                port = config.redis['port']
                db = config.redis['db']
                password = config.redis.get('password')
                
                logger.info(f"正在尝试连接 Redis: {host}:{port}, DB: {db}")

                self._redis = redis.Redis(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    decode_responses=True
                )
                if await self._redis.ping():
                    logger.success("Redis 连接成功！")
                else:
                    logger.error("Redis 连接失败: PING 命令无响应")
            except redis.exceptions.ConnectionError as e:
                logger.error(f"Redis 连接失败: {e}")
                self._redis = None
            except Exception as e:
                logger.exception(f"Redis 初始化时发生未知错误: {e}")
                self._redis = None

    @property
    def redis(self):
        """
        获取 Redis 连接实例
        """
        if self._redis is None:
            raise ConnectionError("Redis 未初始化或连接失败，请先调用 initialize()")
        return self._redis

# 全局 Redis 管理器实例
redis_manager = RedisManager()
