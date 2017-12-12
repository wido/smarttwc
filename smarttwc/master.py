import threading
import serial
import logging
import time
from .fakemaster import FakeMaster


class Master(threading.Thread):
    alive = True
    interval = 0.1

    num_init_msg = 10

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

            if self.num_init_msg > 5:
                logging.info('Sending linkready1')
                fakemaster.send_master_linkready1()
                time.sleep(0.1)
                self.num_init_msg -= 1
            elif self.num_init_msg > 0:
                logging.info('Sending linkready2')
                fakemaster.send_master_linkready2()
                time.sleep(0.1)
                self.num_init_msg -= 1

            self.event.wait(self.interval)

    def join(self, timeout=None):
        self.alive = False
        self.dev.close()
        super(Master, self).join(timeout)
