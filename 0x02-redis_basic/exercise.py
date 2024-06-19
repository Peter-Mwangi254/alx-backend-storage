#!/usr/bin/env python3
"""
Main file that imports
redis and uuid modules
"""
import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class
    """
    def __init__(self):
         """
        Constructor that initializes
        the redis instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
         """
        Store method that takes
        data and returns a key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
        
