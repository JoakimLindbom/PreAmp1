import subprocess

class DSP_manipulator():
    def __init__(self):
        pass

    def mute(self):
        self.call("mute")

    def call(self, cmd, params=""):
        subprocess.run("dsptoolkit", cmd + " " + params)

def Startup(name):
    print(f'Starting up DSP manipulation - {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Startup('DSP 1')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
