"""Sensor platform for City Power outages (minimal scaffold)."""
from __future__ import annotations

import json
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEFAULT_NAME, CONF_AREA, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .coordinator import OutagesCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up sensors for an entry."""
    data = entry.data
    area = data.get(CONF_AREA)
    scan_interval = data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    # Use a dummy local endpoint by default. Replace with real City Power API later.
    endpoint = data.get("endpoint") or "http://localhost:8080/outages"

    coordinator = OutagesCoordinator(hass, endpoint=endpoint, scan_interval=scan_interval)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([CityPowerOutagesSensor(coordinator, area)], True)


class CityPowerOutagesSensor(SensorEntity):
    """Representation of the outages sensor."""

    def __init__(self, coordinator: OutagesCoordinator, area: str | None):
        self.coordinator = coordinator
        self._attr_name = DEFAULT_NAME
        self._attr_unique_id = f"citypower_outages_{area or 'default'}"
        self._area = area

    @property
    def state(self):
        data = self.coordinator.data
        if not data:
            return None
        try:
            # Attempt to mirror the example: pick the outages list and return IDs
            # If data is array-like and contains 'outages' in [0], adapt accordingly.
            if isinstance(data, list) and data:
                first = data[0]
                outages = first.get("outages") or []
                ids = [o.get("id") for o in outages if "id" in o]
                return json.dumps(ids)
            # Fallback: return JSON-dumped data keys
            return json.dumps(data)
        except Exception:  # pragma: no cover - defensive
            _LOGGER.exception("Error computing sensor state")
            return None

    @property
    def extra_state_attributes(self):
        return {"raw": self.coordinator.data}

    async def async_update(self):
        await self.coordinator.async_request_refresh()
