#!/usr/bin/env python3
import config
import logging
import argparse
from threading import Event
from smarttwc import Master

parser = argparse.ArgumentParser(description='SmartTWC')
parser.add_argument("--debug", action="store_true", dest="debug",
                    default=False, help="Debug logging")
args = parser.parse_args()

loglevel = logging.WARN
if args.debug:
    loglevel = logging.DEBUG

logger = logging.basicConfig(level=loglevel)

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
