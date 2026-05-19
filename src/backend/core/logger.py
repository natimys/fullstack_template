from loguru import logger
from functools import wraps
import time

def timer_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        process_time = end_time - start_time
        logger.debug(f"{func.__name__} took {process_time:.2f} seconds")
        return result
    return wrapper