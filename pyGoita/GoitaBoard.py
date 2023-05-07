import copy
from typing import List

from pyGoita.Koma import Koma


class BoardKoma:
    koma: Koma
    is_reversed: bool

    def __init__(self, **kwargs):
        if "koma" in kwargs.keys():
            self.koma = kwargs["koma"]

            self.is_reversed = False
            if "is_reversed" in kwargs.keys():
                self.is_reversed = kwargs["is_reversed"]
        else:
            self.koma = Koma.NONE
            self.is_reversed = False

    def __str__(self):
        return self.koma.name


class GoitaBoard:
    num_of_playing: List[int]
    board: List[List[List[BoardKoma]]]
    game_end: bool

    def __init__(self, **kwargs):
        # 4 * 4 * 2
        self.board = [[[BoardKoma(), BoardKoma()] for i in range(4)] for j in range(4)]
        self.num_of_playing = [0 for _ in range(4)]
        self.game_end = False

    def updated(self, player, koma: Koma, is_reversed: bool, col: int, **kwargs):
        row = 0
        if "row" in kwargs.keys():
            row = kwargs["row"]
        else:
            while not self.board[player][row][col].koma == Koma.NONE:
                row += 1
                if row >= len(self.board[player]):
                    raise ValueError("Cannot enter new koma")

        if is_reversed and col == 1:
            raise ValueError("Cannot update position, if you want to update, please recreate instance")
        if self.board[player][row][col].koma != Koma.NONE:
            raise ValueError("Invalid row definition")

        new_board = copy.deepcopy(self)
        new_board.board[player][row][col] = BoardKoma(koma=koma, is_reversed=is_reversed)
        new_board.num_of_playing[player] = row + 1
        new_board.game_end = new_board.num_of_playing[player] >= 4

        return new_board

    # [Koma or -1 , is_reversed] が 4 * 4 * 2で格納
    def to_array(self):
        res_board = [[[[Koma.NONE.name, False] for t in range(2)] for i in range(4)] for j in range(4)]
        for player in range(4):
            for row in range(4):
                for col in range(2):
                    koma = self.board[player][row][col]
                    res_board[player][row][col][0] = koma.koma.name
                    res_board[player][row][col][1] = koma.is_reversed

        return res_board

    def to_raw_array(self):
        return copy.deepcopy(self.board)
