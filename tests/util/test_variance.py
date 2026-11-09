"""Test variance method."""

from datetime import datetime, timedelta

import pytest

from homeassistant.util.variance import ignore_variance


@pytest.mark.parametrize(
    ("value_1", "value_2", "variance", "expected"),
    [
        (1, 1, 1, 1),
        (1, 2, 2, 1),
        (1, 2, 0, 2),
        (2, 1, 0, 1),
        (
            datetime(2020, 1, 1, 0, 0),
            datetime(2020, 1, 2, 0, 0),
            timedelta(days=2),
            datetime(2020, 1, 1, 0, 0),
        ),
        (
            datetime(2020, 1, 2, 0, 0),
            datetime(2020, 1, 1, 0, 0),
            timedelta(days=2),
            datetime(2020, 1, 2, 0, 0),
        ),
        (
            datetime(2020, 1, 1, 0, 0),
            datetime(2020, 1, 2, 0, 0),
            timedelta(days=1),
            datetime(2020, 1, 2, 0, 0),
        ),
    ],
)
def test_ignore_variance(value_1, value_2, variance, expected) -> None:
    """Test ignore_variance."""
    with_ignore = ignore_variance(lambda x: x, variance)
    assert with_ignore(value_1) == value_1
    assert with_ignore(value_2) == expected


@pytest.mark.parametrize(
    ("values", "variance", "expected"),
    [
        ([1, None, 1], 1, [1, None, 1]),
        ([None, 1, 2], 2, [None, 1, 1]),
        ([1, None, 2], 2, [1, None, 1]),
        ([1, None, 5], 2, [1, None, 5]),
        (
            [datetime(2020, 1, 1, 0, 0), None, datetime(2020, 1, 1, 0, 1)],
            timedelta(minutes=5),
            [datetime(2020, 1, 1, 0, 0), None, datetime(2020, 1, 1, 0, 0)],
        ),
    ],
)
def test_ignore_variance_none(values, variance, expected) -> None:
    """Test ignore_variance passes through None without raising."""
    with_ignore = ignore_variance(lambda x: x, variance)
    assert [with_ignore(value) for value in values] == expected
