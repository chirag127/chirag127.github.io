"""
Retry utilities with exponential backoff.

Provides decorators and utilities for resilient API calls.
"""

import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


logger = logging.getLogger("Utils.Retry")

T = TypeVar("T")


def retry_with_backoff(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator for retrying functions with exponential backoff.

    Retries up to 5 times with exponential wait (4s to 60s).
    Handles RequestException and general Exceptions.
    """
    return retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        retry=retry_if_exception_type(
            (requests.exceptions.RequestException, Exception)
        ),
        reraise=True,
    )(func)


def retry_with_custom_backoff(
    max_attempts: int = 5,
    initial_wait: float = 1.0,
    max_wait: float = 32.0,
    exponential_base: float = 2.0,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Configurable retry decorator with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        initial_wait: Initial wait time in seconds
        max_wait: Maximum wait time in seconds
        exponential_base: Base for exponential calculation

    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        wait_time = min(
                            initial_wait * (exponential_base ** attempt),
                            max_wait
                        )
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                            f"Retrying in {wait_time:.1f}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}"
                        )

            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected retry failure")

        return wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern for API calls.

    Prevents hammering failed services by tracking failures
    and entering an "open" state after threshold is reached.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 60.0,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failures: dict[str, int] = {}
        self._open_until: dict[str, float] = {}

    def is_open(self, key: str) -> bool:
        """Check if circuit is open (blocking requests)."""
        open_until = self._open_until.get(key, 0)
        if time.time() < open_until:
            return True
        # Reset if recovery time has passed
        if key in self._open_until:
            del self._open_until[key]
            self._failures[key] = 0
        return False

    def record_success(self, key: str) -> None:
        """Record a successful call."""
        self._failures[key] = 0

    def record_failure(self, key: str) -> None:
        """Record a failed call."""
        self._failures[key] = self._failures.get(key, 0) + 1

        if self._failures[key] >= self.failure_threshold:
            self._open_until[key] = time.time() + self.recovery_timeout
            logger.warning(
                f"Circuit breaker opened for '{key}' - "
                f"recovery in {self.recovery_timeout}s"
            )

    def reset(self, key: str) -> None:
        """Manually reset circuit for a key."""
        self._failures.pop(key, None)
        self._open_until.pop(key, None)
