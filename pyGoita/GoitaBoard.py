"""GoitaBoard
Defines Goita board data structure.
"""

import copy
from typing import List

from pyGoita.Koma import Koma


class BoardKoma:
    """BoardKoma
    Represents Goita koma on the board.
    Includes reverse status.
    """

    koma: Koma
    """ The koma variable """

    is_reversed: bool
    """ Which the koma is reversed """

    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: Refer the Koma class
        """
        if "koma" in kwargs.keys():
            self.koma = kwargs["koma"]

            self.is_reversed = False
            if "is_reversed" in kwargs.keys():
                self.is_reversed = kwargs["is_reversed"]
        else:
            self.koma = Koma.NONE
            self.is_reversed = False

    def __str__(self):
        """str cast

        Returns:
            The name (not include reverse information)
        """
        return self.koma.name


class GoitaBoard:
    """GoitaBoard
    The game board class of Goita
    """

    num_of_playing: List[int]
    """ How many times the player actioned, shape 4 """

    board: List[List[List[BoardKoma]]]
    """ Board status, shape 4 * 4 * 2 (player * row * column) """

    game_end: bool
    """ Which the game ended """

    def __init__(self):
        # 4 * 4 * 2
        self.board = [[[BoardKoma(), BoardKoma()] for i in range(4)] for j in range(4)]
        self.num_of_playing = [0 for _ in range(4)]
        self.game_end = False

    def updated(self, player, koma: Koma, is_reversed: bool, col: int, **kwargs):
        """updated
        Returns the updated new board instance

        Args:
            player: Playing player index(0 ~ 3)
            koma: The setting koma
            is_reversed: Which the koma is reversed
            col: The position of koma(0 or 1)
            **kwargs:
                row: Specified row index of setting koma

        Returns:
            The new board that have set the koma

        Raises:
            ValueError: When the given argument is invalid
        """
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
    def to_array(self, tokenize=True):
        """to_array
        Returns the board converted to array

        Args:
            tokenize: If True, parse the koma to int token. If False, it is represented as str. (default True)

        Returns:
            The board koma array
        """
        if not tokenize:
            res_board = [[[[Koma.NONE.name, False] for t in range(2)] for i in range(4)] for j in range(4)]
            for player in range(4):
                for row in range(4):
                    for col in range(2):
                        koma = self.board[player][row][col]
                        res_board[player][row][col][0] = koma.koma.name
                        res_board[player][row][col][1] = koma.is_reversed
        else:
            res_board = [[[[Koma.NONE.value, False] for t in range(2)] for i in range(4)] for j in range(4)]
            for player in range(4):
                for row in range(4):
                    for col in range(2):
                        koma = self.board[player][row][col]
                        res_board[player][row][col][0] = koma.koma.value
                        res_board[player][row][col][1] = 1 if koma.is_reversed else 0

        return res_board

    def to_raw_array(self):
        """to_raw_array
        Returns raw board list.
        The koma represented as BoardKoma instance.

        Returns:
            Deep copy of the baord list, each element's type is BoardKoma
        """
        return copy.deepcopy(self.board)
