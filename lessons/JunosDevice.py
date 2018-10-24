from jnpr.junos import Device

class JunosDevice(object):

    def __init__(self):
        self.device = None

    def connect_device(self,host, user, password):
        self.device = Device(host, user=user, password=password)
        self.device.open()

    def gather_facts(self):
        device_facts = dict(self.device.facts)
        return device_facts

    def close_device(self):
        self.device.close()