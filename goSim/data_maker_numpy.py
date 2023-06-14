import glob
import yaml
import pyGoita as pg

from utils import convert_hands


def main():
    files = glob.glob("../data/raw_kifu/goita*")

    for i, file in enumerate(files):
        with open(file, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        match = pg.GoitaMatch()

        for log in data["log"]:
            match.reset_round()
            match.start_round(hands=convert_hands(log["hand"]), start_player=log["uchidashi"])

            for play_log in log["game"]:
                match.update_hand(int(play_log[0]), pg.Koma.from_str(play_log[2]), pg.Koma.from_str(play_log[1]))

        pg.LogExporter.log_match_numpy(
            match,
            i,
            path="../extendedData/test/2"
        )


if __name__ == "__main__":
    main()
