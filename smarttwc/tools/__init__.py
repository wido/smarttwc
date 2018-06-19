def hex_str(ba: bytearray):
    return ' '.join('{:02X}'.format(c) for c in ba)


def slave_id_str(slave_id):
    return '{:02X}{:02X}'.format(slave_id[0], slave_id[1])
