
import time
import threading, queue

import yaml
from smbus2 import SMBus, i2c_msg
import yaml


class ButtonController():
    def __init__(self):
        self.i2c_slave_addr = 0x01

        self.inputs = []
        self.RadioButtons = []
        self.q = queue.Queue()
        time.sleep(1)
        # threading.Thread(target=self.comms_worker, daemon=True).start()

    def addButton(self, button):
        self.inputs.append(button)

    def comms_worker(self):
        data_size = 64
        while True:
            time.sleep(0.1)

            with SMBus(1) as bus:
                msg = i2c_msg.read(self.i2c_slave_addr, data_size)
                bus.i2c_rdwr(msg)

    def get_config(self, config_file):
        l = 0
        with open(config_file) as c:
            d = yaml.load(c, Loader=yaml.FullLoader)
            print(f"{d}")
            l = 1
        return l

