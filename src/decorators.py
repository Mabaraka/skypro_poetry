# mypy: ignore-errors

from functools import wraps


def log(filename=None):
    """
    Декоратор предназначенный для логирования операций
    может записывать как в файл, так и в консоль
    при ошибке записывает текст ошибки и входные параметры функции
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_msg = f"{func.__name__} ok"
                error = None
            except Exception as e:
                result = None
                log_msg = f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}"
                error = e

            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(log_msg)
            else:
                print(log_msg, end="")

            if error:
                raise error
            return result

        return wrapper

    return decorator
