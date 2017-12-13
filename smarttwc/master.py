import threading
import serial
import logging
from .fakemaster import FakeMaster


class Master(threading.Thread):
    alive = True
    interval = 0.1

    initialized = False

    def __init__(self, serial_device, serial_baud_rate, max_current):
        super(Master, self).__init__()
        self.event = threading.Event()
        self.alive = True
        self.serial_device = serial_device
        self.serial_baud_rate = serial_baud_rate
        self.max_current = max_current
        self.dev = serial.Serial(serial_device, serial_baud_rate)

    def run(self):
        fakemaster = FakeMaster(self.dev, self.max_current)

        logging.info('Master thread starting up')
        while self.alive:
            if not self.initialized:
                self.initialized = fakemaster.init_master()

            logging.debug('Reading data from bus')
            self.dev.read_all()

            self.event.wait(self.interval)

    def join(self, timeout=None):
        self.alive = False
        self.dev.close()
        super(Master, self).join(timeout)
