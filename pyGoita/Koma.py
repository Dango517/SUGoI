from enum import Enum


class Koma(Enum):
    # nothing or pass
    NONE = 0
    SHI = 1
    GON = 2
    UMA = 3
    KIN = 4
    GIN = 5
    KAK = 6
    HSY = 7
    GYK = 8

    @staticmethod
    def from_str(s: str):
        s = s.lower()

        if s == "shi" or s == "し":
            return Koma.SHI
        if s == "gon" or s == "香":
            return Koma.GON
        if s == "uma" or s == "bakko" or s == "馬":
            return Koma.UMA
        if s == "kin" or s == "金":
            return Koma.KIN
        if s == "gin" or s == "銀":
            return Koma.GIN
        if s == "kak" or s == "kaku" or s == "角":
            return Koma.KAK
        if s == "hisya" or s == "hsy" or s == "hisha" or s == "飛":
            return Koma.HSY
        if s == "gyk" or s == "ou" or s == "gyoku" or s == "王" or s == "玉":
            return Koma.GYK

        return Koma.NONE

    @staticmethod
    def checkKomaNum(**kwargs):
        for (key, val) in kwargs.items():
            rep = key
            if type(rep) == str:
                rep = Koma.from_str(rep)
            if type(rep) != Koma:
                return False

            if rep == Koma.NONE:
                return True

            lim = 4
            if rep == Koma.SHI:
                lim = 10
            if rep == Koma.GYK or rep == Koma.HSY or rep == Koma.KAK:
                lim = 2

            return 0 <= val <= lim
