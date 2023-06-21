import numpy as np
from typing import List

from .GoitaRound import GoitaRound
from .GoitaMatch import GoitaMatch


class MatchDataNumpy:
    hands: np.ndarray
    other_hands: np.ndarray
    actions: np.ndarray
    points: np.ndarray
    boards: np.ndarray

    def __init__(self):
        self.hands = np.array([])
        self.other_hands = np.array([])
        self.actions = np.array([])
        self.points = np.array([])
        self.boards = np.array([])

    def append_key(self, key, val):
        self_dict = self.__dict__
        if key not in self_dict.keys():
            return

        if len(self_dict[key]) == 0:
            self_dict[key] = val
            return

        self_dict[key] = np.concatenate([self_dict[key], val])

    def extend(self, target):
        if type(target) != MatchDataNumpy:
            return
        for key, val in target.__dict__.items():
            if len(self.__dict__[key]) == 0:
                self.__dict__[key] = val
                continue
            self.__dict__[key] = np.concatenate([self.__dict__[key], val])

    def export(self, n=None, path="./", prefix="", force=False):
        if not force and n and len(self.hands) < n:
            return False

        if path[-1] != "/":
            path += "/"
        if len(prefix) != 0 and prefix[-1] != ".":
            prefix += "."

        for key in self.__dict__.keys():
            np.save(f"{path}{prefix}{key}.npy", self.__dict__[key][:n])

            self.__dict__[key] = self.__dict__[key][n:] if n else np.array([])

        return True

    @staticmethod
    def from_dict(base_dict):
        data = MatchDataNumpy()
        for key, val in base_dict.items():
            data.__dict__[key] = np.array(val)
        return data


class LogExporter:
    @staticmethod
    def path_fixer(path):
        fixed_path = path
        if fixed_path[0] == "/":
            fixed_path = fixed_path[1:]
        if fixed_path[-1] == "/":
            fixed_path = fixed_path[:-1]
        return fixed_path

    @staticmethod
    def convert_play(log: dict, points: List[int], targ_player=-1):
        player_num = log["played_player"]
        if 0 <= targ_player <= 3 and targ_player != player_num:
            return

        self_hand = np.array(log["hands"][player_num])

        other_hands = []
        j = GoitaRound.incremented_player(player_num)
        while j != player_num:
            other_hands.append(log["hands"][j])
            j = GoitaRound.incremented_player(j)

        action = log["behavior"]

        cur_points = [points[0], points[1]]
        if player_num == 1 or player_num == 3:
            cur_points.reverse()

        if not (0 <= targ_player <= 3):
            board = log["board"]
        else:
            rotated_board = [np.array(log["board"][targ_player])[:, :, 0]]
            j = GoitaRound.incremented_player(j)
            while j != targ_player:
                other_board = np.array(log["board"][j])
                # mask the reverse koma
                other_board[other_board[:, :, 1] == 1, 0] = 9
                rotated_board.append(other_board[:, :, 0])
                j = GoitaRound.incremented_player(j)
            board = rotated_board

        return {
            "hands": self_hand,
            "other_hands": other_hands,
            "actions": action,
            "points": cur_points,
            "boards": board
        }

    @staticmethod
    def convert_round(g_round: GoitaRound, points: List[int], targ_player=-1):
        base_dicts = g_round.to_dict()

        datas = {
            "hands": [],
            "other_hands": [],
            "actions": [],
            "points": [],
            "boards": []
        }
        for i, log in enumerate(base_dicts):
            res = LogExporter.convert_play(log, points, targ_player=targ_player)
            if not res:
                continue
            for key, val in res.items():
                datas[key].append(val)
        return MatchDataNumpy.from_dict(datas)

    @staticmethod
    def convert_match(match: GoitaMatch):

        winner = [0, 2] if match.winner == 0 else [1, 3]

        datas = {
            "win": MatchDataNumpy(),
            "lose": MatchDataNumpy()
        }

        for g_round, point in zip(match.logs, match.point_logs):
            for pl in range(4):
                side_point = point if pl % 2 == 0 else list(reversed(point))
                data = LogExporter.convert_round(
                    g_round,
                    side_point,
                    targ_player=pl
                )
                for key, val in data.__dict__.items():
                    datas[("win" if pl in winner else "lose")].append_key(key, val)

        return datas






