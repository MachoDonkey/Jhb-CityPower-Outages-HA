import asyncio
import json

import pytest

pytest.importorskip("homeassistant")


def test_dummy():
    """A very small smoke test placeholder.

    This test is intentionally minimal and will be skipped if Home Assistant test
    helpers are not available in the environment running the tests.
    """
    assert True
