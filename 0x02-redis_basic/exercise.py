#!/usr/bin/env python3
""" This module create a calss cachae and the return the key"""


import redis
import uuid
import functools
from typing import Union, Callable


def replay(fn: Callable):
    """Display the history of calls of a particular function"""
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    try:
        n_calls = n_calls.decode('utf-8')
    except Exception:
        n_calls = 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ""

        print(f'{f_name}(*{i}) -> {o}')


def call_history(method: Callable) -> Callable:
    """ This is a method that reurn tha callable wrapper """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ This method return the _redis output key """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        # Store input parameters
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, output)

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """ This is a method that handle a callable wrapper """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ This function return the method of the key """
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
    @call_history
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
