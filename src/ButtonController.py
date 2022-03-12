import time
import threading, queue
import RPi.GPIO as GPIO

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

class Inputs():
    def __init__(self, GPIO_pin, name):
        self._GPIO_pins = [GPIO_pin]
        self._name = name
        self.state = False  # Start in off state
        self.previous_button_state = None

    def init(self):
        pass

    @property
    def GPIO_pin(self):
        return self._GPIO_pins

    @property
    def name(self):
        return self._name

    def getState(self):
        x = not GPIO.input(self._GPIO_pin)
        if x != self.previous_button_state:
            return x, True
        return x, False

    def printState(self):
        print(f'GPIO: {self._GPIO_pin}, state: {self.state}')


class Button(Inputs):
    def __init__(self, GPIO_pin, name):
        super().__init__(GPIO_pin, name)


class LatchButton(Button):
    def __init(self, GPIO_pin, name):
        super().__init__(GPIO_pin, name)

    def getState(self):
        x = not GPIO.input(self._GPIO_pin)
        if x and not self.previous_button_state:
            self.state = not self.state
            print(f'Latch button is {"ON" if self.state else "OFF"}')
            self.previous_button_state = x
            return self.state, True
        if not x and self.previous_button_state:
            self.previous_button_state = §False
        return self.state, False

class MomentaryButton(Button):
    def __init(self, GPIO_pin, name):
        super().__init__(GPIO_pin, name)

    def getState(self):
        x = not GPIO.input(self._GPIO_pin)
        if x != self.previous_button_state:
            self.state = not self.state
            print(f'Momentary button is {"ON" if self.state else "OFF"}')
            self.previous_button_state = x
            return self.state, True
        return self.state, False


class RadioButtons(Button):
    def __init__(self, GPIO_pins, names, default=None):
        #super().__init__(GPIO_pins)
        self.buttons = []
        self.state = []
        self.pressed = -1
        y = 0
        for p, n in zip(GPIO_pins, names):
            b = Button(p, n)
            b.init()
            self.buttons.append(b)
            if n is not None and n == default:
                self.state.append(True)
                self.pressed = y
            else:
                self.state.append(False)
            y += 1

    def init(self):

        for b in self.buttons:
            GPIO.setup(b.GPIO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getState(self):
        y = 0
        for b in self.buttons:
            state, changed = b.getState()
            if changed and state:
                if y != self.pressed:
                    self.pressed = y
                    print(f"Radiobutton pressed: {self.pressed}")

class Local_GPIO():
    def __init__(self):
        pass

    def init(self):
        GPIO.setmode(GPIO.BCM)  # Use GPIO number not physical pin number


class ESP_Communication():
    def __init__(self):
        pass

    def