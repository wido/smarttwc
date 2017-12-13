#!/usr/bin/env python3
import logging
import argparse
from threading import Event
from smarttwc import Master

parser = argparse.ArgumentParser(description='SmartTWC')
parser.add_argument("--debug", action="store_true", dest="debug",
                    default=False, help="Debug logging")
parser.add_argument("--serial-device", action="store", dest="serial_device",
                    help="Serial device to use")
parser.add_argument("--serial-baud-rate", action="store", type=int,
                    dest="serial_baud_rate", help="Serial baud rate")
parser.add_argument("--max-current", action="store", type=int,
                    dest="max_current", help="Maximum current")
args = parser.parse_args()

loglevel = logging.WARN
if args.debug:
    loglevel = logging.DEBUG

logger = logging.basicConfig(level=loglevel)

if args.serial_device:
    serial_device = args.serial_device
else:
    from config import SERIAL_DEVICE
    serial_device = SERIAL_DEVICE

if args.serial_baud_rate:
    serial_baud_rate = args.serial_baud_rate
else:
    from config import SERIAL_BAUD_RATE
    serial_baud_rate = SERIAL_BAUD_RATE

if args.max_current:
    max_current = args.max_current
else:
    from config import MAX_CURRENT
    max_current = MAX_CURRENT

logging.info('Serial Device: %s Baud Rate: %d Max Current: %d',
            serial_device, serial_baud_rate, max_current)

master = Master(serial_device, serial_baud_rate, max_current)
master.daemon = True
master.start()

event = Event()
while master.is_alive():
    try:
        event.wait(0.1)
    except:
        master.join()
