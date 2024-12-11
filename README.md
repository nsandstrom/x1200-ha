# X1200 Home Assistant Custom Integration

A Custom Integration for Home Assistant, to integrate with a [Geekworm X1200 UPS shield](https://wiki.geekworm.com/index.php?title=X1200).  
It is very much in preview.

Exposes sensors for:
* Voltage
* Battery level
* If charger is connected

A battery protection mode can also be enabled, that stops charging when battery is at ~4V.  

Can be installed as a [custom repository](https://www.hacs.xyz/docs/faq/custom_repositories/) in HACS.  
After installation, it can be configured from the UI.  
Add "Geekworm X1200 UPS" under Settings -> Integrations.  

System needs to have I²C enabled before installation. Use for example [HassOSConfigurator/Pi4EnableI2C](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C).

Tested with a X1200 on Raspberry Pi 5, _might_ work with other Geekworm UPS'es on other platforms.
