"""Shared base class for all entitys."""

from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import DOMAIN


class DeviceBase(Entity):
    """Base representation of a device on X1200 hub."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        self._hub = hub

    @property
    def device_info(self) -> DeviceInfo:
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._hub.hub_id)},
            "name": self._hub.name,
            "model": self._hub.model,
            "manufacturer": self._hub.manufacturer,
        }

    @property
    def available(self) -> bool:
        """Return True if ups is online."""
        return self._hub.online
