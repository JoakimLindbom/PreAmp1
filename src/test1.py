import unittest
from Players import Players
from Players import PlayerStatus

playernames = ['mpd', 'spotify', 'snapcast', 'LNOR041559', 'Joakim_s_S10e']

class testPlayer_Len(unittest.TestCase):
    def test_len(self):
        players = Players()
        self.assertEqual(len(players), 0)

        self.assertTrue(players.addPlayers(playernames))
        self.assertEqual(len(players), 5)


class testPlayer_GetItem(unittest.TestCase):
    def setUp(self):
        self.players = Players()
        self.players.addPlayers(playernames)

    def test_getitem(self):
        p = self.players["mpd"]
        self.assertEqual(p._status, PlayerStatus.Unknown)


class testPlayer_Status(unittest.TestCase):
    def setUp(self):
        self.players = Players()
        self.players.addPlayers(playernames)

    def test_SetGetStatus(self):
        p = self.players["mpd"]
        p.status = PlayerStatus.Playing
        self.assertEqual(p.status, PlayerStatus.Playing)
        p.status = PlayerStatus.Unknown
        self.assertEqual(p.status, PlayerStatus.Unknown)


class testPlayer_Playing(unittest.TestCase):
    def setUp(self):
        self.players = Players()
        self.players.addPlayers(playernames)

    def test_GetLiveStatus(self):
        self.players.getStatus()
        p = self.players["mpd"]
        self.assertEqual(p.status, PlayerStatus.Playing)

class testPlayer_PlayPause(unittest.TestCase):
    def setUp(self):
        self.players = Players()
        self.players.addPlayers(playernames)

    def test_Pause(self):
        p = self.players["mpd"]
        self.assertEqual(True, p.pause())
        self.assertEqual(True, p.play())
        self.assertEqual(True, p.next())
        self.assertEqual(True, p.previous())

