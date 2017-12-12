#!/usr/bin/env python3
import config
import logging
from threading import Event
from smarttwc import Master

logger = logging.basicConfig(level=logging.INFO)

master = Master(config.SERIAL_DEVICE,
                config.SERIAL_BAUD_RATE,
                config.MAX_CURRENT)
master.daemon = True
master.start()

event = Event()
while master.is_alive():
    try:
        event.wait(0.1)
    except:
        master.join()
