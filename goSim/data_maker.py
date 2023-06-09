import yaml
import glob
import pyGoita as pg
import json
from collections import Counter
import yaml

from collections import Counter


def convert_hands(dict_hands):
    handsets = []
    for string in dict_hands.values():
        koma_reps = []
        for s in string:
            koma_reps.append(pg.Koma.from_str(s).name)
        komas = dict(Counter(koma_reps))
        handsets.append(pg.Handset(**komas))
    return handsets


files = glob.glob("../data/raw_kifu/goita*")

for file in files:
    with open(file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for i, log in enumerate(data["log"]):
        master = pg.GameMaster()
        master.start_game(hands=convert_hands(log["hand"]))

        for play_log in log["game"]:
            master.update_hand(int(play_log[0]), pg.Koma.from_str(play_log[2]), pg.Koma.from_str(play_log[1]))

        log_data = {
            "game": master.to_dict(),
            "score": log["score"]
        }

        file_name = file.split("\\")[-1]

        with open(f"../data/extdata/{file_name}-{i}.json", encoding="utf-8", mode="w") as f2:
            json.dump(log_data, f2, indent=4)
