import asyncio

import pytest

from py_simple_package.src.py_simple.easy_async import (
    EasyAsyncError,
    run_at_the_same_time_no_params,
    run_at_the_same_time_with_params,
    run_with_timeout,
    run_concurrent_map,
    run_after_delay,
    run_with_retry,
    run_periodically,
)


def test_run_at_the_same_time_no_params_error():
    def failing_function():
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_at_the_same_time_no_params([failing_function]))


def test_run_at_the_same_time_no_params():
    def add():
        return 2 + 2

    def multiply():
        return 3 * 3

    result = asyncio.run(run_at_the_same_time_no_params([add, multiply]))

    assert result == [
        ("add", 4),
        ("multiply", 9),
    ]


def test_run_at_the_same_time_with_params():
    def add(a, b):
        return a + b

    def subtract(a, b):
        return a - b

    result = asyncio.run(
        run_at_the_same_time_with_params(
            [
                (add, 5, 3),
                (subtract, 5, 3),
            ]
        )
    )

    assert result == [
        ("add", 8),
        ("subtract", 2),
    ]


def test_run_at_the_same_time_with_params_error():
    def failing_function(value):
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_at_the_same_time_with_params([(failing_function, 10)]))


def test_run_with_timeout_success():
    """It should execute the function with arguments and return its name and result."""

    def sample_func(x):
        return x * 2

    name, result = asyncio.run(run_with_timeout(sample_func, 2.0, 5))
    assert name == "sample_func"
    assert result == 10


def test_run_with_timeout_failure():
    """It should raise EasyAsyncError if execution times out or fails."""
    import time

    def slow_func():
        time.sleep(0.4)
        return True

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_with_timeout(slow_func, 0.1))


def test_run_concurrent_map_success():
    def double(x):
        return x * 2

    inputs = [1, 2, 3, 4, 5]
    results = asyncio.run(run_concurrent_map(double, inputs))
    assert results == [2, 4, 6, 8, 10]


def test_run_concurrent_map_error():
    def divide_hundred_by(x):
        return 100 // x

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_concurrent_map(divide_hundred_by, [10, 5, 0, 2]))


def test_run_after_delay_success(monkeypatch):
    async def instant_sleep(delay):
        assert delay == 0.5

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def add(a, b):
        return a + b

    result = asyncio.run(run_after_delay(add, 0.5, 2, 3))

    assert result == ("add", 5)


def test_run_after_delay_wraps_function_error(monkeypatch):
    async def instant_sleep(delay):
        assert delay == 0.1

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def fail():
        raise ValueError("broken")

    with pytest.raises(EasyAsyncError, match="broken"):
        asyncio.run(run_after_delay(fail, 0.1))


def test_run_with_retry_success():
    def num(n1, n2):
        return n1 + n2

    result = asyncio.run(run_with_retry(num, 4, 2.0, 2, 3))
    assert result == ("num", 5)


def test_run_with_retry_fail():
    def num():
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_with_retry(num, 3, 0.01))


def test_run_periodically_success(monkeypatch):
    slept = []

    async def fake_sleep(delay):
        slept.append(delay)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    def add():
        return 2 + 2

    result = asyncio.run(run_periodically(add, 0.5, 3))

    assert result == [4, 4, 4]
    assert slept == [0.5, 0.5, 0.5]


def test_run_periodically_passes_args_every_run(monkeypatch):
    async def instant_sleep(delay):
        pass

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def add(a, b):
        return a + b

    result = asyncio.run(run_periodically(add, 0.1, 2, 3, 4))

    assert result == [7, 7]


def test_run_periodically_single_run(monkeypatch):
    async def instant_sleep(delay):
        pass

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def greet():
        return "hi"

    result = asyncio.run(run_periodically(greet, 0.1, 1))

    assert result == ["hi"]


def test_run_periodically_error(monkeypatch):
    async def instant_sleep(delay):
        pass

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def fail():
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_periodically(fail, 0.1, 3))


def test_run_periodically_invalid_interval():
    def add():
        return 2 + 2

    with pytest.raises(EasyAsyncError, match="interval"):
        asyncio.run(run_periodically(add, 0, 3))

    with pytest.raises(EasyAsyncError, match="interval"):
        asyncio.run(run_periodically(add, -1.0, 3))


def test_run_periodically_invalid_times():
    def add():
        return 2 + 2

    with pytest.raises(EasyAsyncError, match="times"):
        asyncio.run(run_periodically(add, 0.5, 0))

    with pytest.raises(EasyAsyncError, match="times"):
        asyncio.run(run_periodically(add, 0.5, -2))
