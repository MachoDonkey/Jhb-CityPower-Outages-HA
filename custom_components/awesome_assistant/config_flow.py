"""Config flow for the integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_AREA, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN


class CityPowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for City Power outages."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input.get(CONF_AREA, "City Power"), data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_AREA): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
