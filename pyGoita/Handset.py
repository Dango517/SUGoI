from Koma import Koma
import copy


class Handset:
    def __init__(self, **kwargs):
        self.hand = {}
        for koma in Koma:
            self.hand[koma] = 0

        c = 0
        for (key, val) in kwargs:
            rep = Koma.from_str(key)
            if rep == -1 or not Koma.checkKomaNum(**{rep: val}):
                raise ValueError("Invalid argument in each koma")

            self.hand[key] = val
            c += val

        if c != 8:
            raise ValueError("Invalid sum of koma")

    def to_dict(self):
        return copy.deepcopy(self.hand)

    def to_array(self):
        arr = []
        for (key, val) in self.hand:
            arr.extend([key for _ in range(val)])
        return arr

    def updated(self, koma: Koma):
        assert self.hand[koma] > 0, "invalid update"
        new_hand = copy.deepcopy(self.hand)
        new_hand[koma] -= 1
        return Handset(**new_hand)
