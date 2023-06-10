import numpy as np
from typing import List

from .GoitaRound import GoitaRound
from .GoitaMatch import GoitaMatch


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
    def save_numpy(round: GoitaRound, game_id: int, kyk_id: int, points: List[int], path=".", targ_player=-1):
        base_dicts = round.to_dict()

        for i, log in enumerate(base_dicts):
            player_num = log["played_player"]
            if 0 <= targ_player <= 3 and targ_player != player_num:
                continue

            path = LogExporter.path_fixer(path)
            prefix = f"{path}/{game_id}.{kyk_id}.{i}.{player_num}"

            self_hand = np.array(log["hands"][player_num])
            np.save(f"{prefix}.hand.npy", self_hand)

            other_hands = []
            j = GoitaRound.incremented_player(player_num)
            while j != player_num:
                other_hands.append(log["hands"][j])
                j = GoitaRound.incremented_player(j)
            np.save(f"{prefix}.other_hands.npy", np.array(other_hands))

            action = log["behavior"]
            np.save(f"{prefix}.action.npy", np.array(action))

            cur_points = [points[0], points[1]]
            if player_num == 1 or player_num == 3:
                cur_points.reverse()
            np.save(f"{prefix}.points.npy", np.array(cur_points))

            if not (0 <= targ_player <= 3):
                np.save(f"{prefix}.board.npy", np.array(log["board"]))
            else:
                rotated_board = [log["board"][targ_player]]
                j = GoitaRound.incremented_player(j)
                while j != targ_player:
                    rotated_board.append(log["board"][j])
                    j = GoitaRound.incremented_player(j)
                np.save(f"{prefix}.board.npy",  np.array(rotated_board))

    @staticmethod
    def log_match_numpy(match: GoitaMatch, match_id: int, path=".", win_path="win", lose_path="lose"):
        path = LogExporter.path_fixer(path)
        win_path = LogExporter.path_fixer(win_path)
        lose_path = LogExporter.path_fixer(lose_path)

        win_prefix = f"{path}/{win_path}/"
        lose_prefix = f"{path}/{lose_path}/"

        winner = [0, 2] if match.winner == 0 else [1, 3]

        for i, (round, point) in enumerate(zip(match.logs, match.point_logs)):
            for pl in range(4):
                side_point = point if pl % 2 == 0 else list(reversed(point))
                LogExporter.save_numpy(
                    round,
                    match_id,
                    i,
                    side_point,
                    path=(win_prefix if pl in winner else lose_prefix),
                    targ_player=pl
                )









