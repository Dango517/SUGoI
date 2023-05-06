import copy
from pyGoita.Koma import Koma


class Handset:
    def __init__(self, **kwargs):
        self.hand = {}
        for koma in Koma:
            self.hand[koma] = 0

        for (key, val) in kwargs.items():
            rep = Koma.from_str(key)

            assert rep != -1 and Koma.checkKomaNum(**{rep.name: val})

            self.hand[rep] = val

    def to_dict(self):
        return copy.deepcopy({name: num for name, num in self.hand.items()})

    def to_array(self):
        arr = []
        for (key, val) in self.hand:
            arr.extend([key for _ in range(val)])
        return arr

    def updated(self, koma: Koma):
        assert self.hand[koma] > 0, "invalid update"
        new_hand = copy.deepcopy(self.hand)
        new_hand[koma] -= 1

        return Handset(**{key.name: val for (key, val) in new_hand.items()})
