"""Util functions to help filter out similar results."""

from collections.abc import Callable
from datetime import datetime, timedelta
import functools
from typing import Any, overload


@overload
def ignore_variance[**_P, _R: (int, int | None)](
    func: Callable[_P, _R], ignored_variance: int
) -> Callable[_P, _R]: ...


@overload
def ignore_variance[**_P, _R: (float, float | None)](
    func: Callable[_P, _R], ignored_variance: float
) -> Callable[_P, _R]: ...


@overload
def ignore_variance[**_P, _R: (datetime, datetime | None)](
    func: Callable[_P, _R], ignored_variance: timedelta
) -> Callable[_P, _R]: ...


def ignore_variance[**_P](
    func: Callable[_P, Any], ignored_variance: Any
) -> Callable[_P, Any]:
    """Wrap a function that returns old result if new result does not vary enough."""
    last_value: Any = None

    @functools.wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> Any:
        nonlocal last_value

        if (value := func(*args, **kwargs)) is None:
            return None

        if last_value is not None and abs(value - last_value) < ignored_variance:
            return last_value

        last_value = value
        return value

    return wrapper
