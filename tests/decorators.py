from functools import wraps
import time  # Dodato za merenje vremena

def measure_time(func):
    # Decorator for measuring the execution time of a test method.
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = time.time() - start_time
            print(f"{func.__name__} took {elapsed_time:.3f} seconds")
    return wrapper