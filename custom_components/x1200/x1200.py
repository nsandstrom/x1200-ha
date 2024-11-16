"""Generic UPS hat module."""

from datetime import datetime
import logging
import struct

import gpiod
from gpiod.line import Direction, Value
from smbus import SMBus

_LOGGER = logging.getLogger(__name__)


class BaseUpsHat:
    """Base for UPS hats."""

    def __init__(self, i2c_bus: int, i2c_address: int) -> None:
        """Initialize the sensor."""
        self._i2c_address = i2c_address

    def _read_level(self) -> int:
        pass

    @classmethod
    def test_connection(cls, i2c_bus: int, i2c_address: int) -> bool:
        """Test if we can connect on the i2c bus."""
        x12 = cls(i2c_bus, i2c_address)
        level = x12.battery_level
        if level >= 0 and level < 200:
            return True
        raise UnexpectedConnectivityResult(f"Battery level {level} was not expected")


class X1200(BaseUpsHat):
    """The real UPS hat."""

    def __init__(self, i2c_bus: int, i2c_address: int) -> None:
        """Initialize the sensor."""
        super().__init__(i2c_bus, i2c_address)
        self._i2c = SMBus(i2c_bus)

    def _read_level(self):
        read = self._i2c.read_word_data(self._i2c_address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        return swapped / 256

    def _read_voltage(self):
        read = self._i2c.read_word_data(self._i2c_address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        return swapped * 1.25 / 1000 / 16

    def _read_pld(self):
        PLD_PIN = 6

        with gpiod.request_lines(
            "/dev/gpiochip4",
            consumer="x1200",
            config={
                PLD_PIN: gpiod.LineSettings(
                    direction=Direction.INPUT,
                )
            },
        ) as request:
            pld_state = request.get_value(PLD_PIN)
            _LOGGER.warn(f"pld_state: {pld_state} at {datetime.now()}")

            if pld_state == Value.ACTIVE:
                return True
            if pld_state == Value.INACTIVE:
                return False
        return None

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        level = self._read_level()
        return round(level, 2)

    @property
    def battery_voltage(self) -> float:
        """Battery voltage."""
        voltage = self._read_voltage()
        return round(voltage, 2)


class UnexpectedConnectivityResult(Exception):
    """Connectivity test returned something we did not expect."""
