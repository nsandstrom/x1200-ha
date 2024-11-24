"""Platform for sensor integration."""

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .entity import DeviceBase


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    hub = config_entry.runtime_data

    new_devices = []
    new_devices.append(BatterySensor(hub))
    new_devices.append(VoltageSensor(hub))

    if new_devices:
        async_add_entities(new_devices)


class BatterySensor(DeviceBase):
    """Representation of a Battery Sensor."""

    device_class = SensorDeviceClass.BATTERY
    _attr_unit_of_measurement = PERCENTAGE

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)

        self._attr_unique_id = f"{self._hub.hub_id}_battery_capacity"
        self._attr_name = f"{self._hub.name} Battery Capacity"
        self._state = self._hub.battery_level

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._hub.battery_level


class VoltageSensor(DeviceBase):
    """Representation of a Voltage Sensor."""

    device_class = SensorDeviceClass.VOLTAGE
    _attr_unit_of_measurement = "V"
    _attr_icon = "mdi:flash"

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)

        self._attr_unique_id = f"{self._hub.hub_id}_battery_voltage"
        self._attr_name = f"{self._hub.name} Battery Voltage"
        self._state = self._hub.battery_voltage

    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        return self._hub.battery_voltage
