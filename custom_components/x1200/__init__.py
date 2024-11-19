"""The nsalab-test integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .hub import Hub

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

type HubConfigEntry = ConfigEntry[Hub]


async def async_setup_entry(hass: HomeAssistant, entry: HubConfigEntry) -> bool:
    """Set up nsalab-test from a config entry."""

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)

    print("🍅 Is this config entry?", entry.data)

    integer_address = int(entry.data["i2c_address"], 16)

    entry.runtime_data = Hub(
        hass,
        entry.data["i2c_bus"],
        integer_address,
        entry.data["gpoi_chip"],
        entry.data["pld_pin"],
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: HubConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
