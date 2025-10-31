import asyncio
import pytest


@pytest.fixture
def event_loop():
    """Create a fresh event loop for tests that require the `event_loop` fixture.

This avoids recursive fixture dependencies when other plugins provide a `loop`
fixture that depends on `event_loop`.
"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
