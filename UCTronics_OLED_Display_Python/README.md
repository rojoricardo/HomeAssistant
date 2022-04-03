# YAHBOOM RGB COOLING HAT OLED Display - Python Version

Enables Yahboom RGB Cooling HAT and OLED display Pi 4 to work with Home Assistant.

### NB, This addon will take some time to initially load as it has to build some python libraries. 

This add-on is based on the project of Gareth Cheyne, https://github.com/garethcheyne/HomeAssistant which allows Home Assistant to use an OLED Display, I just added and addapted code to that project, from the developers of Yahboom RGB Cooling HAT for the Raspberry Pi, in orther to make it work and be able to use the fan and the RGB leds.

Gareth Cheyne, wishes to give special thanks to [DC Walter](https://github.com/dcwalter) for his assistance on this project.

This addon includes a splash screen that will show you the current version of the Core OS, and HA, and will be presented with an astricx if either require an upgrade. You are also able to set the duration of the slide rotation, and what slides you wish to present.
Also it'll give five options to set values for when the fan will turn on, at higher temperature, higher speed, the leds change depending on the temperature of the device too, right now they are at a set color, in the future planning on makeing them available through Home Assistant.


## First Step  - Enable i2c
### Option 1  - Official
[Official Documentation](https://www.home-assistant.io/common-tasks/os#enable-i2c-with-an-sd-card-reader) 

### Options 2 - Best Choise
This addon from Adam Outler, [GitHub adamoutler](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C) to first enable the I2C interface, you will need to reboot twice as per his documentation. After I2C is enabled then you wil be able to use this. 


## Second Step - Enable this Addon.
1. Start the Addon
2. Check the "Log" and see if there are any errors.
3. Your OLED should be displaying and fan and RGB leds reflecting the temperature

## Some Teaser Screenshots.
### Splash Screen
![Splash Screen](https://github.com/garethcheyne/HomeAssistant/raw/main/UCTronics_OLED_Display_Python/python/img/examples/splash.png?raw=true)
### CPU Stats
![CPU Stats](https://github.com/garethcheyne/HomeAssistant/raw/main/UCTronics_OLED_Display_Python/python/img/examples/cpu.png?raw=true)
### RAM Stats
![RAM Stats](https://github.com/garethcheyne/HomeAssistant/raw/main/UCTronics_OLED_Display_Python/python/img/examples/memory.png?raw=true)
### Storage Stats
![Storage Stats](https://github.com/garethcheyne/HomeAssistant/raw/main/UCTronics_OLED_Display_Python/python/img/examples/storage.png?raw=true)
### Network Stats
![Network Stats](https://github.com/garethcheyne/HomeAssistant/raw/main/UCTronics_OLED_Display_Python/python/img/examples/network.png?raw=true)
