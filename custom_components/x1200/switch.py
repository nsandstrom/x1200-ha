"""Support for Netatmo/BTicino/Legrande switches."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from . import HubConfigEntry
from .entity import DeviceBase

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    hub = config_entry.runtime_data

    new_devices = []
    new_devices.append(BatteryProtection(hub))

    if new_devices:
        async_add_entities(new_devices)


class BatteryProtection(SwitchEntity, RestoreEntity, DeviceBase):
    """A switch for enabling battery protection."""

    def __init__(self, hub) -> None:
        """Initialize the device."""
        super().__init__(hub)

        self._attr_unique_id = f"{self._hub.hub_id}_battery_protection"
        self._attr_name = f"{self._hub.name} Battery Protection"

    def _publish_state_update(self) -> None:
        self._hub.battery_protection = self._attr_is_on
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Run when switch is added to Home Assistant."""
        if state := await self.async_get_last_state():
            self._attr_is_on = state.state == STATE_ON
        else:
            self._attr_is_on = True
        self._publish_state_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the zone on."""
        self._attr_is_on = True
        self._publish_state_update()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the zone off."""
        self._attr_is_on = False
        self._publish_state_update()
