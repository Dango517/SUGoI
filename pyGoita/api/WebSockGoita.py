from typing import Optional

import pyGoita as pg


class Player:
    pl_name: str
    sec_key: str

    def __init__(self, pl_name, sec_key):
        self.pl_name = pl_name
        self.sec_key = sec_key


class VoteList:
    is_active: bool

    def __init__(self, players=None):
        if players is None:
            players = []
        self.keys_to_vote = [player.sec_key for player in players]
        self.is_active = False

    def participate(self, player: Player):
        self.keys_to_vote.append(player.sec_key)

    def vote(self, player: Player):
        if not player.sec_key in self.keys_to_vote:
            return
        self.keys_to_vote.remove(player.sec_key)
        if len(self.keys_to_vote) == 0:
            self.is_active = True


class GoitaRoom:
    gm: Optional[pg.GameMaster]

    def __init__(self):
        self.players = {i: None for i in range(4)}
        self.ready_list = VoteList()
        self.reset_vote_list = VoteList()
        self.num_of_players = 0

    def seat(self, i, player):
        if not self.players[i] is None:
            raise ValueError("The seat is already seated")

        self.players[i] = player
        self.reset_vote_list.participate(player)
        self.ready_list.participate(player)
        self.num_of_players += 1

    def unseat(self, i, player):
        if self.players[i] is None:
            raise ValueError("Trying to unseat empty seat")
        if self.players[i].sec_key != player.sec_key:
            raise ValueError("Trying to unseat other's seat")

        self.players[i] = None
        self.vote_reset(player)
        # ready vote should not be called here
        self.ready_list.vote(player)
        self.num_of_players -= 1

    def vote_reset(self, player):
        self.reset_vote_list.vote(player)
        if not self.reset_vote_list.is_active:
            return

        self.gm = None
        self.players = {i: None for i in range(4)}
        self.reset_voting()

    def ready(self, player):
        if not (self.gm is None or self.gm.is_game_ended()):
            raise ValueError("Trying to ready though the game is continuing")

        self.ready_list.vote(player)
        if not self.ready_list.is_active or self.num_of_players < 4:
            return False

        self.gm = pg.GameMaster()
        self.gm.start_game()
        self.reset_voting()

        return True

    def reset_voting(self):
        self.ready_list = VoteList(players=list(self.players.values()))
        self.reset_vote_list = VoteList(players=list(self.players.values()))


