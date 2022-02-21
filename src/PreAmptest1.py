import time
from datetime import datetime
from Players import Players, Player
import platform
import relay_controller as rc
from relay_controller import LatchButton, MomentaryButton, RadioButtons, inputController


def is_raspberry_pi() -> bool:
    return platform.machine() in ('armv7l', 'armv6l')

if is_raspberry_pi():
    import relay_controller

if __name__ == "__main__":
    print("Parsing JSON")
    players = Players()
    players.addPlayers(['mpd', 'spotify', 'snapcast', 'LNOR041559', 'Joakim_s_S10e'])
    players.getStatus()

    pl = players.playing()  # Get the currently playing player
    if pl is not None:
        pl.pause()
        pl.play()

    if is_raspberry_pi() and False:
        r = rc.Relay()
        r.init()
        r.readInputs()

    if is_raspberry_pi():
        b1 = LatchButton(GPIO_pin=4, name='Test')
        b1.init()
        ic = inputController()
        ic.addButton(b1)

        r1 = RadioButtons(GPIO_pins=[5, 6, 7], names=['mpd', 'Spotify', 'Bluetooth'])
        r1.init()

    now = datetime.now().strftime("%H:%M:%S")

    try:
        while True:
            #players.getStatus()
            #players.printStatus()
            if is_raspberry_pi() and False:
                i = r.readInputs()
                print(f"{now} {i}")
                r.setOutputs()
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    print("Ending")
