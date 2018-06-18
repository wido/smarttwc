import time


class SlaveList:
    def __init__(self):
        self.slaves = list()

    def contains(self, slave_id):
        slave = [x for x in self.slaves if x.slave_id == slave_id]

        return slave

    def add_slave(self, slave_id, max_current):
        slave = self.contains(slave_id)

        if not slave:
            slave = Slave(slave_id, max_current)
            self.slaves.append(slave)

    def remove_slave(self, slave_id):
        slave = self.contains(slave_id)
        if slave:
            self.slaves.remove(slave)

    def __iter__(self):
        for slave in self.slaves:
            yield slave

    def __len__(self):
        return len(self.slaves)


class Slave:
    def __init__(self, slave_id, max_current=6):
        self.slave_id = slave_id
        self.max_current = max_current
        self.heartbeat = time.time()

    def ping(self):
        self.heartbeat = time.time()

