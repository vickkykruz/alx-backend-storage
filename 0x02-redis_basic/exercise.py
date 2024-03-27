#!/usr/bin/env python3
""" This module create a calss cachae and the return the key"""


import redis
import uuid
import functools
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ This is the class class cache that handles the following methods """
    def __init__(self):
        """ This is the initialization method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ This is the method that return the stored key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """ This is a method that return the get request of the key """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """ The method return the get request str """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """ This method return the get request int """
        return self.get(key, fn=int)
