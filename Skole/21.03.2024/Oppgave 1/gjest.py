class Gjest:
    def __init__(self) -> None: 
        self._underholdningsverdi = 0

    def hentUnderholdningsverdi(self):
        return self._underholdningsverdi

    def underhold(self, helltallsverdi):
        self._underholdningsverdi += helltallsverdi