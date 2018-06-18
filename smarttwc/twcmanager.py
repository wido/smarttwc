import threading
import logging
import re
from .fakemaster import FakeMaster
from. slave import SlaveList
from .serial import Device
from .serial.messages import Messages


class TWCManager(threading.Thread):
    def __init__(self, serial_device, serial_baud_rate, max_current):
        super(TWCManager, self).__init__()
        self.event = threading.Event()
        self.interval = 0.1
        self.alive = True
        self.max_current = max_current
        self.initialized = False
        self.slaves = SlaveList()
        self.dev = Device(serial_device, serial_baud_rate)

    def run(self):
        fakemaster = FakeMaster(self.dev, self.max_current)

        logging.info('Master thread starting up')
        while self.alive:
            if not self.initialized:
                logging.info('Master not initialized')
                self.initialized = fakemaster.init_master()

            msg = self.dev.read_msg()
            if msg == 0:
                continue

            logging.debug('len=%d msg=%s ', len(msg), msg)

            if len(msg) > 0:
                match = re.search(Messages.MESSAGE_MATCH.value, msg, re.DOTALL)
                if match:
                    sender_id = match.group(1)
                    max_current = ((match.group(3)[0] << 8) + match.group(3)[1]) / 100
                    logging.debug('slave=%s max_current=%d', sender_id, max_current)
                    self.slaves.add_slave(sender_id, max_current)

            logging.info('We currently have %d slaves', len(self.slaves))
            self.event.wait(self.interval)

    def join(self, timeout=None):
        self.alive = False
        self.dev.close()
        super(TWCManager, self).join(timeout)
