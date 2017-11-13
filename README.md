# smarthpwc
Smart (Tesla) charging with a EU HPWC in combination with a Dutch Smart Meter.

# How does it work?
SmartHPWC connects to a Dutch Smart Meter (DSMR) and reads the current energy consumption of the grid connection.

Based on this information it tells the HPWC (in slave mode) how much current it's allowed to advertise to the connected car.

# TWCManager
A lot of credits go to [TWCManager](https://github.com/cdragon/TWCManager) for figuring out the protocol of the Tesla HPWC.
