from __future__ import annotations

import asyncio
import functools
import inspect
from asyncio import Task
from collections.abc import Callable
from concurrent.futures import Future
from typing import Any

from loguru import logger

from python_boilerplate.configuration.thread_pool_configuration import executor


def done_callback(future: Future[Any] | Task[Any]) -> None:
    """
    The default callback is to be executed for Future once it's done.

    This function must be called after submitting a Future, to prevent the ThreadPoolExecutor swallowing exception in
    other threads.

    https://stackoverflow.com/questions/15359295/python-thread-pool-that-handles-exceptions
    https://stackoverflow.com/a/66993893

    :param future: an asynchronous computation
    """
    logger.debug(f"The worker has done its Future task. Done: {future.done()}, future task: {future}")
    exception = future.exception()
    if exception is not None:
        logger.exception(
            f"The worker has raised an exception while executing Future task: {future}, exception: {exception}"
        )


def async_function[R](func: Callable[..., R]) -> Callable[..., Future[R]]:
    """
    An easy way to implement multi-tread feature with thread pool.

    The decorator to run sync function in thread pool. The return value of decorated function will be
    `concurrent.futures._base.Future`.

    Usage: decorate the function with `@async_function`. For example,

    * a function that accepts one integer argument:
    >>> @async_function
    >>> def an_async_function(a_int: int) -> None:
    >>>     pass

    * a function without argument:
    >>> @async_function
    >>> def an_async_function() -> None:
    >>>   pass

    https://stackoverflow.com/questions/37203950/decorator-for-extra-thread

    :param func: a sync function to run in thread pool
    """

    @functools.wraps(func)
    def wrapper(*arg: Any, **kwarg: Any) -> Future[R]:
        future = executor.submit(func, *arg, **kwarg)
        future.add_done_callback(done_callback)
        module = inspect.getmodule(func)
        logger.debug(f"Submitted future task to run function asynchronously: {future}, {module}.{func.__qualname__}")
        return future

    return wrapper


def async_function_wrapper(func: Callable[..., Any]) -> Callable[..., Task[Any]]:
    """
    The decorator to add `add_done_callback` for async function.

    The return value of decorated function will be `concurrent.futures._base.Future`.

    Usage: decorate the function with `@async_function`. For example,

    * a function that accepts one integer argument:
    >>> @async_function_wrapper
    >>> async def an_async_function(a_int: int) -> None:
    >>>     pass

    * a function without argument:
    >>> @async_function_wrapper
    >>> async def an_async_function() -> None:
    >>>   pass

    :param func: a sync function to run in thread pool
    """

    @functools.wraps(func)
    def wrapper(*arg: Any, **kwarg: Any) -> Task[Any]:
        future = asyncio.ensure_future(func(*arg, **kwarg))
        future.add_done_callback(done_callback)
        return future

    return wrapper
