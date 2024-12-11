"""A simple abstraction hub."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant

from .const import DOMAIN, POLL_TIME
from .x1200 import X1200

SCAN_INTERVAL = timedelta(seconds=POLL_TIME)

BATTERY_CHARGE_ENABLE_THRESHOLD_VOLTAGE = 3.95
BATTERY_CHARGE_DISABLE_THRESHOLD_VOLTAGE = 4.16

class Hub:
    """Abstraction hub."""

    manufacturer = "Geekworm"

    def __init__(
        self,
        hass: HomeAssistant,
        i2c_bus: int,
        i2c_address: int,
        gpoi_chip: int,
        pld_pin: int,
        battery_protection_pin: int,
    ) -> None:
        """Init hub."""
        self._hass = hass
        self.name = "X1200 UPS"
        self._id = DOMAIN

        self.model = "X1200 UPS Shield"

        self.x1200 = X1200(
            i2c_bus, i2c_address, gpoi_chip, pld_pin, battery_protection_pin
        )

        self._battery_protection = None
        self._battery_level = None
        self._battery_voltage = None
        self._external_power_connected = None
        self._battery_charge_enabled = True

        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for hub."""
        return self._id

    @staticmethod
    def test_connection(i2c_bus: int, i2c_address: int) -> bool:
        """Test connectivity to the UPS module."""
        return X1200.test_connection(i2c_bus, i2c_address)

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        self._battery_level = self.x1200.battery_level
        return self._battery_level

    @property
    def battery_voltage(self) -> float:
        """Battery voltage."""
        self._battery_voltage = self.x1200.battery_voltage
        return self._battery_voltage

    @property
    def external_power_connected(self) -> bool:
        """If external power is pluged in."""
        self._external_power_connected = self.x1200.external_power_detected
        return self._external_power_connected

    @property
    def battery_protection(self) -> bool:
        """If battery charge is limited."""
        return self._battery_protection

    @battery_protection.setter
    def battery_protection(self, value: bool) -> None:
        self._battery_protection = value

    @property
    def battery_charging(self) -> int:
        """Determine if battery should be charging or not."""

        charge_state = self._battery_charge_enabled

        if self._battery_protection:
            if self._battery_voltage <= BATTERY_CHARGE_ENABLE_THRESHOLD_VOLTAGE:
                charge_state = True

            elif self._battery_voltage >= BATTERY_CHARGE_DISABLE_THRESHOLD_VOLTAGE:
                charge_state = False

        else:
            charge_state = True

        self._battery_charge_enabled = charge_state

        self.x1200.disable_battery_charge(not charge_state)

        if self._external_power_connected:
            return charge_state
        return False
