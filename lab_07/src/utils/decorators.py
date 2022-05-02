from time import time


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        answer = func(*args, **kwargs)
        stop_time = time()

        return answer, stop_time - start_time

    return wrapper
