"""Day 4 · The flaky server

call_with_retry(fn) calls fn() and, when it fails for a reason that might go away, tries again
after waiting a little longer each time.

Two kinds of errors (already defined for you):
  TransientError  - a timeout or a 503. Worth retrying.
  PermanentError  - a 400 or a 404. Retrying won't fix it, so fail at once.

Run `python quest.py 4` to check the retry wrapper.
"""
import logging
import time
from typing import Callable, TypeVar

T = TypeVar("T")
log = logging.getLogger("rynovi.retry")


class TransientError(Exception):
    pass


class PermanentError(Exception):
    pass


def call_with_retry(
    fn: Callable[[], T],
    attempts: int = 4,
    base_delay: float = 0.5,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Retry transient failures with exponentially increasing delays."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    for attempt in range(1, attempts):
        try:
            return fn()
        except TransientError as error:
            delay = base_delay * 2 ** (attempt - 1)
            log.warning("attempt %d failed: %s; retrying in %.1fs", attempt, error, delay)
            sleep(delay)

    return fn()
