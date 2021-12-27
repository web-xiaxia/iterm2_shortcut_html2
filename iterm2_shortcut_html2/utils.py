# -*- coding: utf-8 -*-
from functools import wraps


def singleton(f):
    instance = {}

    @wraps(f)
    def get_instance(*args, **kwargs):
        if f not in instance:
            instance[f] = f(*args, **kwargs)
        return instance[f]

    return get_instance
