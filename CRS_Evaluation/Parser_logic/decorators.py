import functools
import time


def timer(func):
    """
    Print the runtime of the decorated function.
    Source: https://realpython.com/primer-on-python-decorators/
    @param func: the function to be measured
    @return:
    """

    @functools.wraps(func)
    def wrapper_time(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} seconds")
        return value

    return wrapper_time
