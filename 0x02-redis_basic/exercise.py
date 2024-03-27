#!/usr/bin/env python3
""" This module create a calss cachae and the return the key"""


import redis
import uuid
from typing import Union


class Cache:
    """ This is the class class cache that handles the following methods """
    def __init__(self):
        """ This is the initialization method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ This is the method that return the stored key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
