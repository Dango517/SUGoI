import glob
import pyGoita as pg
import json
import yaml

from utils import convert_hands


def main():
    files = glob.glob("../data/raw_kifu/goita*")

    for file in files:
        with open(file, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for i, log in enumerate(data["log"]):
            round = pg.GoitaRound()
            round.start_game(hands=convert_hands(log["hand"]))

            for play_log in log["game"]:
                round.update_hand(int(play_log[0]), pg.Koma.from_str(play_log[2]), pg.Koma.from_str(play_log[1]))

            log_data = {
                "game": round.to_dict(),
                "score": log["score"]
            }

            file_name = file.split("\\")[-1]

            with open(f"../data/extdata/{file_name}-{i}.json", encoding="utf-8", mode="w") as f2:
                json.dump(log_data, f2, indent=4)


if __name__ == "__main__":
    main()
