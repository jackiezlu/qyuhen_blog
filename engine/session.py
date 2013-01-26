# coding=utf-8

__all__ = []


from redis import ConnectionPool, Redis


class Session(object):
    #
    # 
    # 
    pool = ConnectionPool(max_connections = settings.REDIS_POOL_MAX, 
        host = settings.REDIS_HOST, port = settings.REDIS_PORT, db = settings.SESSION_DB)


    def __init__(self, uid):
        self._uid = uid
        self._redis = Redis()


    def _refresh(self, pipeline):
        # 
        # 刷新过期时间。
        # 
        pipeline.expire(self._uid, settings.SESSION_EXPIRE)


    def exists(self):
        # 
        # 判断当前用户 Session 是否存在，以便从数据库刷新信息。
        # 
        return self._redis.exists(self._uid)


    def get(self, key):
        # 
        # 获取值
        # 
        pass


    def set(self, key, value):
        # 
        # 设置键值
        # 
        pass


