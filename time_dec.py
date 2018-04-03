import time
import timeit
import functools


def timefunc(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsed_time * 1000)))
    return newfunc

