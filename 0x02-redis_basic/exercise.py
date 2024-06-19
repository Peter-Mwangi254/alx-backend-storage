#!/usr/bin/env python3
"""
Main file that imports
redis and uuid modules
"""
import redis
from uuid import uuid4
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the
    number of times a method is called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Inner function that increments
        the counter and returns the method
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the
    history of inputs and outputs
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Inner function that stores
        the inputs and outputs
        """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Function that replays the
    history of calls of a method
    """
    key = method.__qualname__
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    inputs = redis.lrange(f"{key}:inputs", 0, -1)
    outputs = redis.lrange(f"{key}:outputs", 0, -1)

    print(f"{key} was called {count} times:")
    for i, o in zip(inputs, outputs):
        print(f"{key}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store method that takes
        data and returns a key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float]:
        """
        Get method that takes a key
        and an optional Callable function
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Get method that takes a key
        and returns a string
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """
        Get method that takes a key
        and returns an integer
        """
        return self.get(key, int)
        
