import time
from smarttwc.tools import slave_id_str


class SlaveList:
    def __init__(self):
        self.slaves = list()

    def contains(self, slave_id):
        slave = [x for x in self.slaves if x.slave_id == slave_id]

        if len(slave) > 0:
            return slave[0]

    def add(self, slave_id, max_current):
        slave = self.contains(slave_id)

        if not slave:
            slave = Slave(slave_id, max_current)
            self.slaves.append(slave)

        return slave

    def remove(self, slave_id):
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

    def __str__(self):
        return 'slave_id={0} max_current={1}'.format(slave_id_str(self.slave_id),
                                                     self.max_current)

