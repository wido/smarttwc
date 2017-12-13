import threading
import serial
import logging
from .fakemaster import FakeMaster
from. slave import Slave


class Master(threading.Thread):
    alive = True
    interval = 0.1
    initialized = False
    slaves = list()

    def __init__(self, serial_device, serial_baud_rate, max_current):
        super(Master, self).__init__()
        self.event = threading.Event()
        self.alive = True
        self.serial_device = serial_device
        self.serial_baud_rate = serial_baud_rate
        self.max_current = max_current
        self.dev = serial.Serial(serial_device, serial_baud_rate, timeout=0)

    def run(self):
        fakemaster = FakeMaster(self.dev, self.max_current)

        logging.info('Master thread starting up')
        while self.alive:
            if not self.initialized:
                logging.info('Master not initialized')
                self.initialized = fakemaster.init_master()

            logging.debug('Reading data from bus')
            data = self.dev.read(16)
            if data and len(data) == 16:
                slave = Slave(slave_id=1, max_current=self.max_current)
                self.slaves.append(slave)

            self.event.wait(self.interval)

    def join(self, timeout=None):
        self.alive = False
        self.dev.close()
        super(Master, self).join(timeout)
