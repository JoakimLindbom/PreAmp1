# Notes on pin usage for Hifiberry DAC+, DAC+ ADC, DIGI+ AND AMP+, DAC2 PRO boards
# from https://www.hifiberry.com/docs/hardware/gpio-usage-of-hifiberry-boards/
# Pin 27 and 28 are always reserve
# GPIO2-3 (pins 3 and 5) are used by our products for configuration.(I2C)
# GPIOs 18-21 (pins 12, 35, 38 and 40) are used for the sound interface.
#

import RPi.GPIO as GPIO
 #import gpio4 as GPIO
#import gpio4.constants as const

import time
import threading, queue


class inputController():
    def __init__(self):
        self.inputs = []
        self.RadioButtons = []
        self.q = queue.Queue()
        time.sleep(1)
        threading.Thread(target=self.inputs_worker, daemon=True).start()

    def addButton(self, button):
        self.inputs.append(button)

    def addRadioButton(self, radiobutton):
        self.RadioButtons.append(radiobutton)

    def inputs_worker(self):
        while True:
            time.sleep(0.1)
            y = 0
            for i in self.inputs:
                state, changed = i.getState()
                if changed:
                    #print(f"Change detected new state {state}")
                    #self.inputs[y].state = state
                    msg = {"GPIO": i.GPIO_pin, "state": state}
                    #print(msg)
                    # self.q.put(msg)
                y += 1

            y = 0
            for i in self.RadioButtons:
                for b in i.buttons:
                    state, changed = i.getState()
                    if changed:
                        #print(f"Change detected new state {state}")
                        #self.inputs[y].state = state
                        msg = {"GPIO": i.GPIO_pin, "state": state}
                        #print(msg)
                        # self.q.put(msg)
                    y += 1


class Inputs():
    def __init__(self, GPIO_pin, name):
        self._GPIO_pin = GPIO_pin
        self._name = name
        self.state = False  # Start in off state
        self.previous_button_state = None

    def init(self):
        GPIO.setmode(GPIO.BCM)  # Use GPIO number not physical pin number
        GPIO.setup(self._GPIO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @property
    def GPIO_pin(self):
        return self._GPIO_pin

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
            self.previous_button_state = False
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
        GPIO.setmode(GPIO.BCM)  # Use GPIO number not physical pin number

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


class Relay():
    def __init__(self):
        # N.B. GPIO cannot be use in __init__
        self.q = queue.Queue()

        self.inputs = [4, 5, 6, 7, 8]
        self.input_state = []
        self.outputs = [15, 14, 13]
        self.output_state = []
        for o in self.inputs:
            self.input_state.append(False)  # Off
        for o in self.outputs:
            self.output_state.append(0.0)  # Off
        print("--- Starting RelayController---")

    def init(self):
        GPIO.setmode(GPIO.BCM)  # Use GPIO number not physical pin number

        print(f"Setting up inputs")

        for p in self.inputs:
            print(f"           GPIO{p}")
            GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(f"Setting up outputs")

        for p in self.outputs:
            print(f"           GPIO{p}")
            GPIO.setup(p, GPIO.OUT)
            #GPIO.output(p, GPIO.LOW)

        GPIO.output(self.outputs[0], GPIO.LOW)

        time.sleep(1)
        threading.Thread(target=self.inputs_worker, daemon=True).start()
        threading.Thread(target=self.outputs_worker, daemon=True).start()

    def inputs_worker(self):
        while True:
            time.sleep(0.1)
            y = 0
            for i in self.inputs:
                x = not GPIO.input(i)
                #print(f"x {x} input_state; {self.input_state[y]}")
                if x != self.input_state[y]:
                    print(f"Change detected new state {x}")
                    self.input_state[y] = x
                    msg = {"port": y, "state": x}
                    self.q.put(msg)
                y += 1

    def outputs_worker(self):
        while True:
            time.sleep(0.1)
            item = self.q.get()
            print(f'Working on {item}')
            print(f'Finished {item}')
            self.q.task_done()

    def setOutputs(self):
        a = self.readInputs()
        x = 0
        #for o in self.outputs:
        #    x += 1
        #    self.setOutput(o, self.a[x])
        self.setOutput(0, a[0])

    def readInputs(self):
 #       print("Reading inputs")
        a = []
        for i in self.inputs:
            x = GPIO.input(i)
            a.append(0.0 if x else 1.0)
        return a

    def setOutput(self, OutPin, State):
        # TODO: Add PMW support
        #print(f"Outpin: {OutPin} State: {State} {len(self.outputs)}")
        if OutPin <= 0 and OutPin < len(self.outputs):
            if State == 0.0:
                GPIO.output(self.outputs[OutPin], GPIO.LOW)
            if State == 1.0:
                GPIO.output(self.outputs[OutPin], GPIO.HIGH)
