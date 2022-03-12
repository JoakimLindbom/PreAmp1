import websocket
import time
import json
from config import IP_ADRESS

# TODO: Add logger

class equaliser():
    def __init__(self):
        websocket.enableTrace(True)
        self.ws = websocket.create_connection(f"ws://{IP_ADRESS}:80", subprotocols=["beocreate"])

    def __del__(self):
        self.ws.close()

    def compare_on(self, channel='a'):
        #print("Sending on")
        self.ws.send('{"target": "equaliser", "header": "compare", "content": {"channel": "' + channel + '", "on": true}}')
        #print("Receiving...")
        result = self.ws.recv()
        #print("Received '%s'" % result)
        if self.check_compare(result, channel):
            print("Command accepted")

    def compare_off(self, channel='a'):
        #print("Sending off")
        self.ws.send('{"target": "equaliser", "header": "compare", "content": {"channel": "' + channel + '", "on": false}}')
        result = self.ws.recv()
        #print("Received '%s'" % result)
        if not self.check_compare(result, channel):
            print("Command accepted")


    def check_compare(self, result, channel):
        r = json.loads(result)
        #  {"header":"disabledTemporarily","target":"equaliser","content":{"a":true,"b":true,"c":false,"d":false,"l":false,"r":false}}
        if "header" in r:
            if r["header"] == "disabledTemporarily":
                if "content" in r:
                    if channel in r["content"]:
                        return r["content"][channel]

        return False  # TODO: Implement proper error handling


if __name__ == "__main__":
    e = equaliser()

    e.compare_on()

    time.sleep(10)

    e.compare_off()
