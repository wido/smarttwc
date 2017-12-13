from smarttwc.serial.messages import Messages
import time
import logging


class FakeMaster:
    def __init__(self, device, max_current=10):
        self.device = device
        self.max_current = max_current

    def init_master(self):
        num_init_msg = 10
        while True:
            if num_init_msg > 5:
                logging.debug('Sending linkready1')
                self.send_master_linkready1()
                time.sleep(0.1)
                num_init_msg -= 1
            elif num_init_msg > 0:
                logging.debug('Sending linkready2')
                self.send_master_linkready2()
                time.sleep(0.1)
                num_init_msg -= 1
            else:
                break

        return True

    def send_master_linkready1(self):
        self.device.write(Messages.LINK_READY_1.value.encode())

    def send_master_linkready2(self):
        self.device.write(Messages.LINK_READY_2.value.encode())
