import functools
import os
import time
from collections.abc import Callable, Coroutine
from datetime import timedelta
from typing import Any

import psutil
from loguru import logger


def _make_profile_decorator[R](
    get_metric: Callable[[], Any],
    format_message: Callable[[str, Any, Any], str],
    level: str = "INFO",
) -> Callable[..., Callable[..., R]]:
    """
    Generic factory for sync profiling decorators.

    Captures a metric before and after function execution, then logs the formatted result.

    :param get_metric: callable returning the metric value (called before and after execution)
    :param format_message: callable(qualname, before, after) -> log message string
    :param level: logging level
    :return: a decorator that wraps a function with before/after metric capture and logging
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*arg: Any, **kwarg: Any) -> Any:
            before = get_metric()
            try:
                return_value = func(*arg, **kwarg)
            except Exception as e:
                after = get_metric()
                logger.log(level, format_message(func.__qualname__, before, after))
                raise e
            after = get_metric()
            logger.log(level, format_message(func.__qualname__, before, after))
            return return_value

        return wrapper

    return decorator


def elapsed_time[R](level: str = "INFO") -> Callable[..., Callable[..., R]]:
    """
    The decorator to monitor the elapsed time of a function.

    Usage:

    * decorate the function with `@elapsed_time()` to profile the function with INFO log
    >>> @elapsed_time()
    >>> def some_function():
    >>>    pass

    * decorate the function with `@elapsed_time("DEBUG")` to profile the function with DEBUG log
    >>> @elapsed_time("DEBUG")
    >>> def some_function():
    >>>    pass

    https://stackoverflow.com/questions/12295974/python-decorators-just-syntactic-sugar

    :param level: logging level, default is "INFO". Available values: ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]
    """

    def _format(qualname: str, before: Any, after: Any) -> str:
        return f"{qualname}() -> elapsed time: {timedelta(seconds=after - before)}"

    return _make_profile_decorator(get_metric=time.perf_counter, format_message=_format, level=level)


def async_elapsed_time[R](
    level: str = "INFO",
) -> Callable[..., Callable[..., Coroutine[Any, Any, R]]]:
    """
    The decorator to monitor the elapsed time of an async function.

    Usage:

    * decorate the function with `@async_elapsed_time()` to profile the function with INFO log
    >>> @async_elapsed_time()
    >>> async def some_function():
    >>>    pass

    * decorate the function with `@async_elapsed_time("DEBUG")` to profile the function with DEBUG log
    >>> @async_elapsed_time("DEBUG")
    >>> async def some_function():
    >>>    pass

    https://stackoverflow.com/questions/12295974/python-decorators-just-syntactic-sugar

    :param level: logging level, default is "INFO". Available values: ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]
    """

    def decorator(func: Callable[..., Coroutine[Any, Any, R]]) -> Callable[..., Coroutine[Any, Any, R]]:
        @functools.wraps(func)
        async def wrapper(*arg: Any, **kwarg: Any) -> Any:
            start_time = time.perf_counter()
            try:
                return_value = await func(*arg, **kwarg)
            except Exception as e:
                elapsed = time.perf_counter() - start_time
                logger.log(
                    level,
                    f"{func.__qualname__}() -> elapsed time: {timedelta(seconds=elapsed)}",
                )
                raise e
            elapsed = time.perf_counter() - start_time
            logger.log(
                level,
                f"{func.__qualname__}() -> elapsed time: {timedelta(seconds=elapsed)}",
            )
            return return_value

        return wrapper

    return decorator


def get_memory_usage() -> int:
    """
    Gets the usage of memory.

    :return: memory usage in bytes
    """
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def get_cpu_usage() -> float:
    """
    Getting cpu_percent non-blocking (percentage since last call).

    :return: CPU usage
    """
    return psutil.cpu_percent()


def mem_profile[R](level: str = "INFO") -> Callable[..., Callable[..., R]]:
    """
    The decorator to monitor the memory usage of a function.

    Usage:

    * decorate the function with `@mem_profile()` to profile the function with INFO log
    >>> @mem_profile()
    >>> def some_function():
    >>>    pass

    * decorate the function with `@mem_profile("DEBUG")` to profile the function with DEBUG log
    >>> @mem_profile("DEBUG")
    >>> def some_function():
    >>>    pass

    https://stackoverflow.com/questions/12295974/python-decorators-just-syntactic-sugar

    :param level: logging level, default is "INFO". Available values: ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]
    """

    def _format(qualname: str, before: Any, after: Any) -> str:
        return (
            f"{qualname}() -> Mem before: {before}, mem after: {after}. "
            f"Consumed memory: {(after - before) / (1024 * 1024):.2f} MB"
        )

    return _make_profile_decorator(get_metric=get_memory_usage, format_message=_format, level=level)


def cpu_profile[R](level: str = "INFO") -> Callable[..., Callable[..., R]]:
    """
    The decorator to monitor the CPU usage of a function.

    Usage:

    * decorate the function with `@cpu_profile()` to profile the function with INFO log
    >>> @cpu_profile()
    >>> def some_function():
    >>>    pass

    * decorate the function with `@cpu_profile("DEBUG")` to profile the function with DEBUG log
    >>> @cpu_profile("DEBUG")
    >>> def some_function():
    >>>    pass

    https://stackoverflow.com/questions/12295974/python-decorators-just-syntactic-sugar

    :param level: logging level, default is "INFO". Available values: ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]
    """

    def _format(qualname: str, before: Any, after: Any) -> str:
        return f"{qualname}() -> CPU before: {before}, CPU after: {after}, delta: {(after - before):.2f}"

    return _make_profile_decorator(get_metric=get_cpu_usage, format_message=_format, level=level)
