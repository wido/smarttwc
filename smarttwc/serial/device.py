import serial
import logging
import time
import threading
from smarttwc.tools import hex_str


class Device:
    @staticmethod
    def unescape_msg(msg: bytearray, msgLen):
        msg = msg[0:msgLen]

        i = 0
        while i < len(msg):
            if msg[i] == 0xdb:
                if msg[i + 1] == 0xdc:
                    msg[i:i + 2] = [0xc0]
                elif msg[i + 1] == 0xdd:
                    msg[i:i + 2] = [0xdb]
                else:
                    msg[i:i + 2] = [0xdb]
            i = i + 1

        msg = msg[1:len(msg) - 1]
        return msg

    @staticmethod
    def checksum(data):
        msg = bytearray(data)
        checksum = 0
        for i in range(1, len(msg)):
            checksum += msg[i]

        msg.append(checksum & 0xFF)
        return msg

    @staticmethod
    def calc_checksum(msg):
        expected = msg[len(msg) - 1]
        checksum = 0
        for i in range(1, len(msg) - 1):
            checksum += msg[i]

        if (checksum & 0xFF) != expected:
            return True

        return False

    def __init__(self, device, baud_rate, timeout=0):
        self.msg_rx_start = time.time()
        self.event = threading.Event()
        self.dev = serial.Serial(device, baud_rate, timeout=timeout)

    def write(self, data):
        msg = self.checksum(data)

        i = 0
        while i < len(msg):
            if msg[i] == 0xc0:
                msg[i] = b'\xdb\xdc'
                i = i + 1
            elif msg[i] == 0xdb:
                msg[i] = b'\xdb\xdd'
                i = i + 1
            i = i + 1

        logging.debug('TX: %s', hex_str(msg))
        self.dev.write(msg)

    def read(self, size):
        msg = self.dev.read(size)
        logging.debug('RX: %s', hex_str(msg))
        return msg

    def read_msg(self):
        msg = bytearray()

        while True:
            now = time.time()
            waiting = self.dev.in_waiting
            if waiting == 0:
                if len(msg) == 0:
                    if (now - self.msg_rx_start) >= 2.0:
                        break

                    self.event.wait(0.025)
                    continue
            else:
                data = self.dev.read(1)

            if len(msg) == 0 and data[0] != 0xc0:
                continue
            elif 0 < len(msg) < 15 and data[0] == 0xc0:
                msg = data
                continue

            msg += data

            if len(msg) >= 16 and data[0] == 0xc0:
                logging.debug('RX: %s', hex_str(msg))
                if self.calc_checksum(msg):
                    break
                else:
                    logging.debug('Ignoring message due to failed checksum')
                    msg = bytearray()
                    continue

            if len(msg) > 32:
                self.dev.reset_input_buffer()
                msg = bytearray()
                continue

        return msg

    def close(self):
        self.dev.close()
