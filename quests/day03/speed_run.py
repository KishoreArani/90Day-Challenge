"""Day 3 · The speed run

20 pages, 0.2 seconds each. One by one that's 4 seconds. Together it's about 0.2.
Use fake_web.fetch(url) for every request.

Run `python quest.py 3` to check the fetchers.
"""
import asyncio

from quests.day03 import fake_web


async def fetch_one(url: str) -> tuple[str, int]:
    """Fetch a page and return its URL and content length."""
    page = await fake_web.fetch(url)
    return url, len(page)


async def fetch_all(urls: list[str]) -> list[tuple[str, int]]:
    """Fetch pages concurrently and return results in input order."""
    return await asyncio.gather(*(fetch_one(url) for url in urls))


async def fetch_all_limited(urls: list[str], limit: int = 3) -> list[tuple[str, int]]:
    """Fetch pages in input order with at most `limit` active requests."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    semaphore = asyncio.Semaphore(limit)

    async def fetch_with_limit(url: str) -> tuple[str, int]:
        async with semaphore:
            return await fetch_one(url)

    return await asyncio.gather(*(fetch_with_limit(url) for url in urls))


async def fetch_all_safe(urls: list[str], timeout: float = 0.5) -> list[tuple[str, int | None]]:
    """Fetch pages concurrently and return `(url, None)` for timeouts."""

    async def fetch_with_timeout(url: str) -> tuple[str, int | None]:
        try:
            return await asyncio.wait_for(fetch_one(url), timeout=timeout)
        except asyncio.TimeoutError:
            return url, None

    return await asyncio.gather(*(fetch_with_timeout(url) for url in urls))
