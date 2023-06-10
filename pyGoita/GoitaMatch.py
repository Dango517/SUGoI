from typing import List, Dict

from .GoitaRound import GoitaRound
from .Koma import Koma


class GoitaMatch:
    current_round: GoitaRound
    current_points: List[int] = [0, 0]
    match_over = False
    winner: int = -1

    logs: List[GoitaRound] = []
    point_logs: List[List] = []

    def __init__(self, disable_log: bool = False):
        self.disable_log = disable_log
        self.ready_round = False

    def reset_round(self):
        if self.match_over:
            return
        self.current_round = GoitaRound(self.disable_log)
        self.ready_round = True

    def start_round(self, **kwargs):
        if not self.ready_round:
            return
        self.current_round.start_game(**kwargs)
        self.ready_round = False

    def update_hand(self, player: int, atkKoma: Koma, defKoma: Koma, pre_log=True):
        if self.current_round is None or self.current_round.is_game_ended():
            return

        self.current_round.update_hand(
            player,
            atkKoma,
            defKoma,
            pre_log=pre_log
        )

        if self.current_round.is_game_ended():
            self.current_points[self.current_round.winner_side] += self.current_round.achieved_point

            if not self.disable_log:
                self.logs.append(self.current_round)
                self.point_logs.append(self.current_points)

            if self.current_points[self.current_round.winner_side] >= 150:
                self.match_over = True
                self.winner = self.current_round.winner_side





