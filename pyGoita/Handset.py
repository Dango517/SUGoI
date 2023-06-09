import copy
from pyGoita.Koma import Koma


class Handset:
    hand: dict

    def __init__(self, **kwargs):
        self.hand = {}
        for koma in Koma:
            if koma == Koma.NONE:
                continue
            self.hand[koma] = 0

        for (key, val) in kwargs.items():
            rep = Koma.from_str(key)

            if rep == Koma.NONE:
                raise ValueError("Invalid kwargs")
            ignore_num = "ignore_num" in kwargs.keys() and kwargs["ignore_num"]
            if not ignore_num and not Koma.checkKomaNum(**{rep.name: val}):
                raise ValueError("Exceeding Num of Koma; if want to ignore, pass 'ignore_num' argument.")

            self.hand[rep] = val

    def to_dict(self):
        return copy.deepcopy({koma.name: num for koma, num in self.hand.items()})

    def to_array(self, fill_none=True):
        arr = []
        for (key, val) in self.hand.items():
            arr.extend([key.value for _ in range(val)])
        while (not fill_none) or len(arr) < 8:
            arr.append(Koma.NONE.value)
        return arr

    def updated(self, koma: Koma):
        if self.hand[koma] <= 0:
            raise ValueError("Invalid update")

        new_hand = copy.deepcopy(self)
        new_hand.hand[koma] -= 1

        return new_hand

