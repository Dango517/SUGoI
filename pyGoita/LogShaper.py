import numpy as np
from typing import List

from .GameMaster import GameMaster


class LogShaper:
    @staticmethod
    def save_numpy(master: GameMaster, game_id: int, points: List[int], path="./"):
        base_dicts = master.to_dict()

        for i, log in enumerate(base_dicts):
            player_num = log["played_player"]

            if path[-1] != "/":
                path += "/"
            prefix = f"{path}{game_id}.{i}.{player_num}"

            self_hand = np.array(log["hands"][player_num])
            np.save(f"{prefix}.hand.npy", self_hand)

            other_hands = []
            j = GameMaster.incremented_player(player_num)
            print(f"player_num:{player_num}")
            while j != player_num:
                other_hands.append(log["hands"][j])
                print(j)
                j = GameMaster.incremented_player(j)
            np.save(f"{prefix}.other_hands.npy", np.array(other_hands))

            action = log["behavior"]
            np.save(f"{prefix}.action.npy", np.array(action))

            cur_points = [points[0], points[1]]
            if player_num == 1 or player_num == 3:
                cur_points.reverse()
            np.save(f"{prefix}.points.npy", np.array(cur_points))







