import json
from enum import Enum
from enum import auto
from HifiberryAPI import HifiberryosApi


class PlayerStatus(Enum):
    Playing = auto()
    Stopped = auto()
    Paused = auto()
    Undefined = auto()
    Unknown = auto() # E.g. when status cannot be retrieved via the API
    def __str__(self):
        return self.name


class PlayersIterator:
    """ Iterator class """
    def __init__(self, players):
        self._players = players
        self._index = 0

    def __next__(self):
        """Returns the next player from list """
        if self._index < (len(self._players)):
            player = (self._players._players[self._index])
            self._index += 1
            return player
        raise StopIteration


class Players:
    def __init__(self):
        self._players = list()
        self.API = HifiberryosApi()

    def __len__(self):
        return len(self._players)

    def addPlayers(self, _players):
        for pl in _players:
            p = Player(pl)
            self._players += p
        res = self.API.getPlayers()
        return len(res) > 2

    def __iter__(self):
        """Returns iterable object"""
        return PlayersIterator(self)

    def __getitem__(self, item):
        for x in self._players:
            if x._name == item:
                return x
        # If none found:
        return None  # Raise exception?

    def getStatus(self):
        resp = self.API.getPlayers()
        if resp != '{}':
            j = json.loads(resp)
            for pl in j['players']:
                for p2 in self._players:
                    if pl['name'] == p2._name:
                        p2.setStatus(pl["state"].lower())
            return True
        else:
            return False

    def playing(self):
        for x in self._players:
            if x.status == PlayerStatus.Playing:
                return x
        return None

    def printStatus(self):
        a = ''
        for p in self._players:
            a += f'{p} \t'
        print(f'Players: {a} ')


class PlayerIterator:
    ''' Iterator class '''

    def __init__(self, player):
        # player object reference
        self._player = player
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        """Returns the next player from list """
        if self._index < (len(self._player)):
            p = self._player
            self._index += 1
            return p
        raise StopIteration


class Player:
    def __init__(self, name):
        self._name = name
        self.setStatus(PlayerStatus.Unknown)
        self.API = HifiberryosApi()

    def __iter__(self):
        """Returns iterable object"""
        return PlayerIterator(self)

    def __len__(self):
        return 1

    def __str__(self):
        return f'{self._name} {self._status}'

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self.setStatus(new_status)

    def pause(self):
        return self.API.pause()

    def play(self):
        return self.API.play()

    def next(self):
        return self.API.next()

    def previous(self):
        return self.API.previous()

    def setStatus(self, new_status):
        if isinstance(new_status, str):
            if new_status == "playing":
                self._status = PlayerStatus.Playing
            elif new_status == "stopped":
                self._status = PlayerStatus.Stopped
            elif new_status == "paused":
               self._status = PlayerStatus.Paused
            elif new_status == "unknown":
                self._status = PlayerStatus.Unknown
            elif new_status == "undefined":
                self._status = PlayerStatus.Undefined
            else:
               raise ValueError
        elif isinstance(new_status, PlayerStatus):
            if new_status in PlayerStatus:
                self._status = new_status
            else:
                raise ValueError

    def getName(self):
        return self._name

    def getStatus(self):
        return self._status
