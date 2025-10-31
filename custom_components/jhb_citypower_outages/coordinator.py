"""Coordinator to fetch outage data from an endpoint."""
from __future__ import annotations

from datetime import timedelta
import asyncio
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


class OutagesCoordinator(DataUpdateCoordinator):
    """Coordinator that polls the outages API."""

    def __init__(self, hass: HomeAssistant, endpoint: str, scan_interval: int = 300):
        super().__init__(
            hass,
            _LOGGER,
            name="citypower_outages",
            update_interval=timedelta(seconds=scan_interval),
        )
        self._endpoint = endpoint

    async def _async_update_data(self):
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self._endpoint, timeout=30) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except asyncio.CancelledError:
            raise
        except Exception as err:
            raise UpdateFailed(f"Error fetching outages: {err}") from err
