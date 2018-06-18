from enum import Enum


class Messages(Enum):
    FAKE_TW_CID = b'\x77\x77'
    MASTER_SIGN = b'\x77'
    SLAVE_SIGN = '\x77'
    MESSAGE_MATCH = b'^\xc0\xfd\xe2(..)(.)(..)\x00\x00\x00\x00\x00\x00.+\Z'
