from enum import Enum


class Messages(Enum):
    FAKE_TW_CID = '\x77\x77'
    MASTER_SIGN = '\x77'
    SLAVE_SIGN = '\x77'
    LINK_READY_1 = '\xFC\xE1{0}{1}\x00\x00\x00\x00\x00\x00\x00\x00'.format(FAKE_TW_CID, MASTER_SIGN)
    LINK_READY_2 = '\xFB\xE2{0}{1}\x00\x00\x00\x00\x00\x00\x00\x00'.format(FAKE_TW_CID, MASTER_SIGN)
    SLAVE_LINK_READY = '\xFD\xE2{0}{1}\x1F\x40\x00\x00\x00\x00\x00\x00'.format(FAKE_TW_CID, SLAVE_SIGN)
