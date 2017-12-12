#!/usr/bin/env python3
import config
from smarttwc import Master

master = Master(config.SERIAL_DEVICE, config.SERIAL_BAUD_RATE, config.MAX_CURRENT)
