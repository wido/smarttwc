# smarttwc
Smart (Tesla) charging with a (EU) Tesla Wall Connector (TWC) using Python 3 code

# How does it work?
SmartTWC is able to run in *Master* mode for a Tesla Wall Connector and by sending it messages over RS-485 it can
adjust the maximum allowed current the TWC will advertise to the car.

# TWCManager
A lot of credits go to [TWCManager](https://github.com/cdragon/TWCManager) for figuring out the protocol of the Tesla HPWC.

# Requirements
This code has been written for Debian Linux running on a Raspberry Pi. It could and should work on all Linux platforms, but
that has not been tested.

The Python code is written for Python >=3.5 and requires a few additional libraries. These can be found in *requirements.txt*
