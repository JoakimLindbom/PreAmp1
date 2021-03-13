
import logging
from typing import Dict

from usagecollector.client import report_usage

from ac2.plugins.control.controller import Controller


class Buttons(Controller):

    def __init__(self, params: Dict[str, str] = None):
        super().__init__()

        self.clk = 4
        self.dt = 17
        self.sw = 27
        self.step = 5

        self.name = "buttons"

        if params is None:
            params = {}

        if "clk" in params:
            try:
                self.clk = int(params["clk"])
            except:
                logging.error("can't parse %s", params["clk"])

        if "dt" in params:
            try:
                self.dt = int(params["dt"])
            except:
                logging.error("can't parse %s", params["dt"])

        if "sw" in params:
            try:
                self.sw = int(params["sw"])
            except:
                logging.error("can't parse %s", params["sw"])

        if "step" in params:
            try:
                self.step = int(params["step"])
            except:
                logging.error("can't parse %s", params["step"])

        logging.info("initializing buttons controller on GPIOs "
                     " clk=%s, dt=%s, sw=%s, step=%s%%",
                     self.clk, self.dt, self.sw, self.step)

        self.encoder = pyky040.Encoder(CLK=self.clk, DT=self.dt, SW=self.sw)
        self.encoder.setup(scale_min=0,
                           scale_max=100,
                           step=1,
                           inc_callback=self.increase,
                           dec_callback=self.decrease,
                           sw_callback=self.button)

    def increase(self, val):
        if self.volumecontrol is not None:
            self.volumecontrol.change_volume_percent(self.step)
            report_usage("audiocontrol_buttons_button1", 1)
        else:
            logging.info("no volume control, ignoring rotary control")

    def decrease(self, val):
        if self.volumecontrol is not None:
            self.volumecontrol.change_volume_percent(-self.step)
            report_usage("audiocontrol_buttons_button2", 1)
        else:
            logging.info("no volume control, ignoring rotary control")

    def button(self):
        if self.playercontrol is not None:
            self.playercontrol.playpause()
            report_usage("audiocontrol_rotary_button", 1)
        else:
            logging.info("no player control, ignoring press")

    def run(self):
        self.encoder.watch()