from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

from loguru import logger

R = TypeVar("R")


def debounce(wait: float) -> Callable[..., Callable[..., R | None]]:
    """
    Debounce function decorator.

    :param wait: wait time in seconds
    :return: a decorated function
    """

    def decorator(func: Callable[..., R | None]) -> Callable[..., R | None]:
        last_called: float = 0

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R | None:
            nonlocal last_called
            elapsed = time.monotonic() - last_called
            if elapsed > wait:
                logger.debug("Calling function due to elapsed > wait time")
                result: R | None = func(*args, **kwargs)
                last_called = time.monotonic()
                return result
            logger.debug(f"Refused to call function {func.__qualname__}(args={args}, kwargs={kwargs})")
            return None

        return wrapper

    return decorator


def throttle(limit: float) -> Callable[..., Callable[..., R | None]]:
    """
    Throttle function decorator.

    :param limit: throttle limit in seconds
    :return: a decorated function
    """

    def decorator(func: Callable[..., R | None]) -> Callable[..., R | None]:
        last_called: float = 0
        called = False

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R | None:
            nonlocal last_called, called
            elapsed = time.monotonic() - last_called
            if not called:
                logger.debug("Calling func due to not called")
                called = True
                result = func(*args, **kwargs)
                last_called = time.monotonic()
                return result
            if elapsed > limit:
                logger.debug("Calling func due to elapsed > limit")
                result = func(*args, **kwargs)
                last_called = time.monotonic()
                return result
            logger.debug(f"Refused to call function `{func.__qualname__}`(args={args}, kwargs={kwargs})")
            return None

        return wrapper

    return decorator
