import threading
import serial
import logging


class Master(threading.Thread):
    alive = True
    interval = 0.1

    def __init__(self, serial_device, serial_baud_rate, max_current):
        super(Master, self).__init__()
        self.event = threading.Event()
        self.alive = True
        self.serial_device = serial_device
        self.serial_baud_rate = serial_baud_rate
        self.max_current = max_current
        self.dev = serial.Serial(serial_device, serial_baud_rate)

    def run(self):
        logging.info('Master thread starting up')
        while self.alive:
            logging.warning(self.dev.port)
            self.event.wait(self.interval)

    def join(self, timeout=None):
        self.alive = False
        self.dev.close()
        super(Master, self).join(timeout)
