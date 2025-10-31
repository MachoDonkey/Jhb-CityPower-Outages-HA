import json

import pytest

pytest.importorskip("homeassistant")


@pytest.mark.asyncio
async def test_coordinator_fetch(hass, aioclient_mock):
    """Coordinator should fetch JSON from the endpoint."""
    endpoint = "http://example.com/outages"
    sample = [{"id": 1, "outages": [{"id": 101}, {"id": 102}]}]

    # Mock the HTTP response
    aioclient_mock.get(endpoint, json=sample)

    from custom_components.awesome_assistant.coordinator import OutagesCoordinator

    coord = OutagesCoordinator(hass, endpoint=endpoint, scan_interval=1)
    await coord.async_refresh()

    assert coord.data == sample


@pytest.mark.asyncio
async def test_sensor_state(hass, aioclient_mock):
    """Sensor should be created from a config entry and expose state/attributes."""
    endpoint = "http://example.com/outages"
    sample = [{"id": 1, "outages": [{"id": 101}, {"id": 102}]}]

    aioclient_mock.get(endpoint, json=sample)

    from tests.common import MockConfigEntry
    from custom_components.awesome_assistant.const import DOMAIN

    entry = MockConfigEntry(domain=DOMAIN, data={"area": "Test Area", "endpoint": endpoint, "scan_interval": 1})
    entry.add_to_hass(hass)

    # Forward setup to sensor platform
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.async_block_till_done()

    state = hass.states.get("sensor.jhb_city_power_outages")
    assert state is not None

    # The sensor returns the list of outage ids as JSON in state
    assert state.state == json.dumps([101, 102])
    assert "raw" in state.attributes
    assert state.attributes["raw"] == sample
