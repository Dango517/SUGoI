
import pyGoita as pg
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

