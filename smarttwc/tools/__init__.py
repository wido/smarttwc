def hex_str(ba: bytearray):
    return ' '.join('{:02X}'.format(c) for c in ba)
