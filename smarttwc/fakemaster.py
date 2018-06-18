from smarttwc.serial.messages import Messages
import time
import logging


class FakeMaster:
    def __init__(self, device, twcd_id, max_current=10):
        self.device = device
        self.twc_id = twcd_id
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
        msg = bytearray(b'\xFC\xE1') + Messages.FAKE_TW_CID.value + Messages.MASTER_SIGN.value + bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
        self.device.write(msg)

    def send_master_linkready2(self):
        msg = bytearray(b'\xFB\xE2') + Messages.FAKE_TW_CID.value + Messages.MASTER_SIGN.value + bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
        self.device.write(msg)

    def send_max_current(self, slave):
        logging.debug('Advertising maximum current %d to slave %s',
                      slave.max_current, slave.slave_id)
        return True
