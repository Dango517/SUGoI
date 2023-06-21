import glob
import yaml
import pyGoita as pg

from utils import convert_hands
import numpy as np


def main(max_n=None, file_size=100):
    files = glob.glob("../data/raw_kifu/goita*")[:max_n]

    datas = {
        "win": pg.MatchDataNumpy(),
        "lose": pg.MatchDataNumpy()
    }

    win_n = 0
    lose_n = 0

    for i, file in enumerate(files):
        with open(file, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        match = pg.GoitaMatch()

        for log in data["log"]:
            match.reset_round()
            match.start_round(hands=convert_hands(log["hand"]), start_player=log["uchidashi"])

            for play_log in log["game"]:
                match.update_hand(int(play_log[0]), pg.Koma.from_str(play_log[2]), pg.Koma.from_str(play_log[1]))

        data = pg.LogExporter.convert_match(
            match
        )
        datas["win"].extend(data["win"])
        datas["lose"].extend(data["lose"])

        exported = datas["win"].export(file_size, path="../data/result/win/", prefix=f"{win_n}")
        win_n += 1 if exported else 0
        exported = datas["lose"].export(file_size, path="../data/result/lose/", prefix=f"{lose_n}")
        lose_n += 1 if exported else 0


def test():
    file = "../data/raw_kifu/goita_kifu_2023-3-21-21-24-33.yaml"

    with open(file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    match = pg.GoitaMatch()

    for log in data["log"]:
        match.reset_round()
        match.start_round(hands=convert_hands(log["hand"]), start_player=log["uchidashi"])

        for play_log in log["game"]:
            match.update_hand(int(play_log[0]), pg.Koma.from_str(play_log[2]), pg.Koma.from_str(play_log[1]))

    datas = pg.LogExporter.convert_match(
        match
    )

    datas["win"].export(50, path="../extendedData/test/win")
    datas["lose"].export(50, path="../extendedData/test/lose")


if __name__ == "__main__":
    main(max_n=20, file_size=20)
