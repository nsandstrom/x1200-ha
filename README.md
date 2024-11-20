# X1200 Home Assistant Custom Integration

A Custom Integration for Home Assistant, to integrate with a [Geekworm X1200 UPS shield](https://wiki.geekworm.com/index.php?title=X1200).  
It is very much in preview.

Exposes sensors for:
* Voltage
* Battery capacity
* If charger is connected

No built in actions or automations.  

System needs to have I²C enabled before installation. Use for example [HassOSConfigurator/Pi4EnableI2C](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C).

Tested with a X1200 on Raspberry Pi 5, _might_ work with other Geekworm UPS'es on other platforms.
