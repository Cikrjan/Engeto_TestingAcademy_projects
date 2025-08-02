# Jedná se o sdílení svých atributů a mětod mezi svými potomky


class ZmenAuto: #Rodičovská třída
    def __init__(self, auta: list, spz: str):
        self._auta = auta
        self.spz = spz

    def zmen(self):
        for auto in self._auta:
            if auto.spz == self._spz:
                self.zmen_atribut(auto) #Volání metody potomka 

class ZmenZnackuAuta(ZmenAuto):
    def __init__(self, auta: list, spz: str, znacka: str):
        super().__init__(auta, spz)
        self._znacka = znacka

    def zmen_atribut(self, auto):
        auto._znacka = self._znacka