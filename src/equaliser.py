import websocket
import time
import json
import logging as log
from config import IP_ADRESS

# TODO: Add logger

class equaliser():
    def __init__(self):
        self.presets = []
        self.current_preset = None

        #log.basicConfig(filename='equaliser.log', encoding='utf-8', level=log.DEBUG)
        log.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', encoding='utf-8', level=log.DEBUG)
        log.debug('This message should go to the log file')

        websocket.enableTrace(True)
        self.ws = websocket.create_connection(f"ws://{IP_ADRESS}:80", subprotocols=["beocreate"])

        self.get_presets()

    def __del__(self):
        self.ws.close()

    def compare_on(self, channel='a'):
        #print("Sending on")
        self.ws.send('{"target": "equaliser", "header": "compare", "content": {"channel": "' + channel + '", "on": true}}')
        #print("Receiving...")
        result = self.ws.recv()
        #print("Received '%s'" % result)
        if self.check_compare(result, channel):
            log.info("Command accepted")

    def compare_off(self, channel='a'):
        #print("Sending off")
        self.ws.send('{"target": "equaliser", "header": "compare", "content": {"channel": "' + channel + '", "on": false}}')
        result = self.ws.recv()
        #print("Received '%s'" % result)
        if not self.check_compare(result, channel):
            log.info("compare_off - Command accepted")

    def get_presets(self):
        self.ws.send('{"target": "beosonic", "header": "beosonicSettings"}')
        result = self.ws.recv()
        r = json.loads(result)
        try:
            self.presets = r["content"]["settings"]["presetOrder"]
            #print(f"Presets: {self.presets}")
        except KeyError:
            log.critical("get_presets: Whoops no preset list found")
            self.presets = []

        try:
            self.current_preset = r["content"]["settings"]["selectedPreset"]
            log.info(f"Current preset: {self.current_preset}")
        except KeyError:
            log.critical("get_presets: Whoops no selected preset")
            self.presets = []

        #print("Received '%s'" % result)
        #'{"header":"beosonicSettings","target":"beosonic","content":
        # {"settings":{"loudness":5,
        # "beosonicDistance":29.420926181981333,
        # "beosonicAngle":51,
        # "beosonicAmbience":0,
        # "presetOrder":["optimal","clear","dark","podcast","listentest1"],
        # "selectedPreset":
        # "listentest1", "bassGain":0.5884185236396267,"trebleGain":0.07845580315195022,"bassQ":0.707,"trebleQ":0.707,"bassFc":120,"trebleFc":8000,"bassMaxGain":6,"trebleMaxGain":8},"canDoToneControl":{"ambience":false,"toneControls":14},
        # "presets":{"clear":{"presetName":"Clear","readOnly":true,"adjustments":["beosonic"]},
        # "dark":{"presetName":"Dark","readOnly":true,"adjustments":["beosonic"]},
        # "optimal":{"presetName":"Optimal","readOnly":true,"adjustments":["beosonic"]},
        # "podcast":{"presetName":"Podcast","readOnly":true,"adjustments":["beosonic"]},"listentest1":{"presetName":"LIstenTest1","readOnly":false,"adjustments":["beosonic"]}}}}'

    def next_preset(self):
        i = self.presets.index(self.current_preset) + 1
        if i >= len(self.presets):
            i = 0

        self.current_preset = self.presets[i]
        log.info(f"next: {self.current_preset}")
        self.select_preset(self.current_preset)


    def select_preset(self, presetID):
        self.ws.send('{"target": "beosonic", "header": "applyPreset", "content": {"presetID": "' + presetID + '"}}')
        result = self.ws.recv()
        #print("Received '%s'" % result)

    def get_settings(self):
        print("get:settings")
        self.ws.send('{"target": "equaliser", "header": "getSettings"}')
        result = self.ws.recv()
        #print("Received '%s'" % result)
        # Received '{"header":"settings","target":"equaliser","content":{"uiSettings":{"showAllChannels":true,"dBScale":20,
        # "displayQ":"Q","groupAB":true,"groupCD":false,"groupLR":true},"channels":{
        # "a":[{"type":"peak","frequency":100, "Q":0.7071,"gain":1.9,"bypass":false},{"type":"peak","frequency":20,"Q":1.7,"gain":1.8,"bypass":false},
        # {"type":"peak","frequency":7000,"Q":1.8,"gain":-1.4},{"type":"peak","frequency":9400,"Q":0.7071,"gain":-1.2}],
        # "b":[{"type":"peak","frequency":100,"Q":0.7071,"gain":1.9,"bypass":false},{"type":"peak","frequency":20,"Q":1.7,"gain":1.8,"bypass":false},
        # {"type":"peak","frequency":7000,"Q":1.8,"gain":-1.4},{"type":"peak","frequency":9400,"Q":0.7071,"gain":-1.2}],
        # "c":[],"d":[],
        # "l":[{"a0":1,"a1":0,"a2":0,"b0":1,"b1":0,"b2":0,"samplingRate":48000,"bypass":false}],
        # "r":[{"a0":1,"a1":0,"a2":0,"b0":1,"b1":0,"b2":0,"samplingRate":48000,"bypass":false}]},
        # "canControl":{"a":16,"b":16,"c":16,"d":16,"l":16,"r":16},"Fs":48000,
        # "disabledTemporarily":{"a":false,"b":false,"c":false,"d":false,"l":false,"r":false}}}'

    # '{"header":"settings","target":"equaliser","content":{"uiSettings":{"showAllChannels":true,"dBScale":20,
    # "displayQ":"Q","groupAB":true,"groupCD":false,"groupLR":true},"channels":{
    # "a":[{"type":"peak","frequency":100,"Q":0.7071,"gain":1.9,"bypass":false},{"type":"peak","frequency":20,"Q":1.7,"gain":1.8,"bypass":false},{"type":"peak","frequency":7000,"Q":1.8,"gain":-1.4},{"type":"peak","frequency":9400,"Q":0.7071,"gain":-1.2}],
    # "b":[{"type":"peak","frequency":100,"Q":0.7071,"gain":1.9,"bypass":false},{"type":"peak","frequency":20,"Q":1.7,"gain":1.8,"bypass":false},{"type":"peak","frequency":7000,"Q":1.8,"gain":-1.4},{"type":"peak","frequency":9400,"Q":0.7071,"gain":-1.2}],
    # "c":[],"d":[],
    # "l":[{"a0":1,"a1":0,"a2":0,"b0":1,"b1":0,"b2":0,"samplingRate":48000,"bypass":false},{"type":"peak","frequency":7000,"Q":0.7071,"gain":-1.5},{"type":"highShelf","frequency":180,"Q":1.6,"gain":1.5,"bypass":false}],
    # "r":[{"a0":1,"a1":0,"a2":0,"b0":1,"b1":0,"b2":0,"samplingRate":48000,"bypass":false},{"type":"peak","frequency":7000,"Q":0.7071,"gain":-1.5},{"type":"highShelf","frequency":180,"Q":1.6,"gain":1.5,"bypass":false}]},
    # "canControl":{"a":16,"b":16,"c":16,"d":16,"l":16,"r":16},"Fs":48000,
    # "disabledTemporarily":{"a":false,"b":false,"c":false,"d":false,"l":false,"r":false}}}'

    def check_compare(self, result, channel):
        r = json.loads(result)
        #  {"header":"disabledTemporarily","target":"equaliser","content":{"a":true,"b":true,"c":false,"d":false,"l":false,"r":false}}
        if "header" in r and "target" in r:
            if r["header"] == "disabledTemporarily" and r["target"] == "equaliser":
                if "content" in r:
                    if channel in r["content"]:
                        return r["content"][channel]

        return False  # TODO: Implement proper error handling


if __name__ == "__main__":
    e = equaliser()
    e.get_presets()
    e.select_preset("clear")
    e.next_preset()
    time.sleep(3)
    e.next_preset()
    time.sleep(3)
    e.next_preset()
    time.sleep(3)
    e.next_preset()
    time.sleep(3)
    e.next_preset()
    time.sleep(3)
    e.next_preset()
    time.sleep(3)
    e.next_preset()
    time.sleep(3)
    e.next_preset()
    time.sleep(3)
    #e.get_presets()
    #e.compare_on()
    #time.sleep(10)
    #e.compare_off()
