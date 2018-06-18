import serial
import logging
import time
import threading


class Device:
    @staticmethod
    def hex_str(ba: bytearray):
        return ' '.join('{:02X}'.format(c) for c in ba)

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

        logging.debug('TX: %s', self.hex_str(msg))
        self.dev.write(msg)

    def read(self, size):
        msg = self.dev.read(size)
        logging.debug('RX: %s', self.hex_str(msg))
        return msg

    def in_waiting(self):
        data_len = self.dev.in_waiting
        logging.debug('Waiting: %d', data_len)
        return data_len

    def read_msg(self):
        ignored_data = bytearray()
        msg_len = 0
        msg = bytearray()

        while True:
            logging.debug('Reading data from bus')
            now = time.time()
            data_len = self.in_waiting()
            if data_len == 0:
                if msg_len == 0:
                    break
                else:
                    if (now - self.msg_rx_start) >= 2.0:
                        break

                    self.event.wait(0.025)
                    continue
            else:
                data_len = 1
                data = self.dev.read(data_len)

            if data_len != 1:
                logging.error('No data available')
                break

            if msg_len == 0 and data[0] != 0xc0:
                ignored_data += data
                continue
            elif 0 < msg_len < 15 and data[0] == 0xc0:
                msg = data
                msg_len = 1
                continue

            if msg_len == 0:
                msg = bytearray()

            msg += data
            msg_len += 1

            if msg_len >= 16 and data[0] == 0xc0:
                break

        return msg

    def close(self):
        self.dev.close()
