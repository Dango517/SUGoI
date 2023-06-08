import copy
from typing import List
from collections import Counter
import random

from .GoitaBoard import GoitaBoard, BoardKoma
from .Handset import Handset
from .Koma import Koma


def gen_random_hands():
    koma_set = []
    for koma in Koma:
        num_koma = 4
        if koma == Koma.SHI:
            num_koma = 10
        if koma == Koma.GYK or koma == Koma.HSY or koma == Koma.KAK:
            num_koma = 2
        koma_set.extend([koma.name for _ in range(num_koma)])

    random.shuffle(koma_set)
    player_komas = [koma_set[i*4:i*4+4] for i in range(4)]
    player_hands = [Handset(**dict(Counter(player_komas[i]))) for i in range(4)]

    return player_hands


class GameLog:
    hands: List[Handset]
    board: GoitaBoard
    played: int
    behavior: List[int]

    def __init__(self, hands: List[Handset], board: GoitaBoard, played: int = -1, **kwargs):
        self.hands = hands
        self.board = board

        if "koma" in kwargs.keys() and kwargs["koma"] != -1:
            if not isinstance(kwargs["atkKoma"], Koma) or not isinstance(kwargs["defKoma"], Koma):
                raise TypeError("Invalid type of Koma")
            self.behavior = [kwargs["defKoma"].value, kwargs["atkKoma"].value]
        else:
            self.behavior = [0, 0]

        self.played = played

    def to_dict(self, tokenize=True):
        return {
            "played_player": self.played,
            "behavior": self.behavior,
            "hands": [(hand.to_dict() if not tokenize else hand.to_array()) for hand in self.hands],
            "board": self.board.to_array()
        }


class GameMaster:
    currentHands: List[Handset]
    currentBoard: GoitaBoard
    currentAtk: BoardKoma
    currentPlayer: int
    logs: List[GameLog]
    achieved_point: int = -1

    def __init__(self, disable_log=False):
        self.disable_log = disable_log

    def start_game(self, **kwargs):
        if "hands" in kwargs.keys():
            self.currentHands = kwargs["hands"]
        else:
            self.currentHands = gen_random_hands()

        self.currentAtk = BoardKoma()
        self.currentBoard = GoitaBoard()

        if not self.disable_log:
            self.logs = [GameLog(self.currentHands, self.currentBoard)]
        self.currentPlayer = -1

    @staticmethod
    def incremented_player(player):
        return 0 if player == 3 else player + 1

    def update_hand(self, player: int, atkKoma: Koma, defKoma: Koma, pre_log=True):
        if self.currentBoard.game_end:
            raise ValueError("Invalid update trying of board")

        is_starting = self.currentPlayer == -1 or player == self.currentPlayer

        if not (is_starting or defKoma == self.currentAtk.koma):
            raise ValueError("Invalid koma")

        if pre_log:
            self.log_now(atkKoma=atkKoma, defKoma=defKoma)

        # logging pass
        if not self.currentPlayer == -1:
            while player != self.incremented_player(self.currentPlayer):
                self.currentPlayer = self.incremented_player(self.currentPlayer)
                self.log_now()
        self.currentPlayer = player

        self.currentBoard = self.currentBoard.updated(player, defKoma, is_starting, 0)
        self.currentBoard = self.currentBoard.updated(player, atkKoma, False, 1)
        if self.currentBoard.game_end:
            self.achieved_point = self.currentBoard.board[player][3][1].koma.get_point()

        if not pre_log:
            self.log_now(atkKoma=atkKoma, defKoma=defKoma)

        self.currentHands[player] = self.currentHands[player].updated(defKoma).updated(atkKoma)

        assert self.currentBoard != -1 and self.currentHands[player] != -1

        self.currentAtk = BoardKoma(koma=atkKoma)

    def log_now(self, **kwargs):
        if self.disable_log:
            return
        self.logs.append(GameLog(copy.copy(self.currentHands), self.currentBoard, self.currentPlayer, **kwargs))

    def to_dict(self):
        return [log.to_dict() for log in self.logs]

    def is_game_ended(self):
        return self.currentBoard.game_end

    def get_point(self):
        if not self.is_game_ended():
            return -1

        return self.achieved_point

