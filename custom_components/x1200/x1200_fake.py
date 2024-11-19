"""A mocked implementation of the x1200."""

import datetime
import random

from .x1200 import BaseUpsHat


class X1200(BaseUpsHat):
    """A mocked implementation of the x1200."""

    def __init__(
        self, i2c_bus: int, i2c_address: int, gpoi_chip: int, pld_pin: int
    ) -> None:
        """Create a mocked x1200."""
        super().__init__(i2c_bus, i2c_address, gpoi_chip, pld_pin)

        self._local_pld_state = "on"

        print("Connect fake SMBUS", i2c_bus, self._i2c_address)
        print("Connect fake GPIO", self._gpio_path, self._pld_pin)

    def _read_level(self):
        if self._i2c_address == int("0x66", 16):
            raise MockedSMbusError("Fake sensor always fails on address 0x66") from None
        return random.randint(0, 100)

    def _read_voltage(self) -> float:
        return random.random() * 3 + 10

    def _read_pld(self) -> bool:
        if random.randint(0, 10) > 8:
            self._local_pld_state = not self._local_pld_state
        return self._local_pld_state

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        print("🔋 ask for battery_level", datetime.datetime.now())
        level = self._read_level()
        return round(level, 2)

    @property
    def battery_voltage(self) -> float:
        """Return a random voltage roughly that of a 12v battery."""
        print("🔋 ask for battery_voltage", datetime.datetime.now())
        voltage = self._read_voltage()
        return round(voltage, 2)

    @property
    def external_power_detected(self) -> bool:
        """Return true if external power is connected."""
        print("🔌 ask for external_power_detected", datetime.datetime.now())
        return self._read_pld()


class MockedSMbusError(ConnectionError):
    """Error to indicate we cannot connect."""
