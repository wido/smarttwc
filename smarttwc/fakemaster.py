from smarttwc.serial.messages import Messages


class FakeMaster:
    def __init__(self, device, max_current=10):
        self.device = device
        self.max_current = max_current

    def send_master_linkready1(self):
        self.device.write(Messages.LINK_READY_1.value.encode())

    def send_master_linkready2(self):
        self.device.write(Messages.LINK_READY_2.value.encode())
