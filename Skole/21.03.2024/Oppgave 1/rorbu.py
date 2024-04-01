import gjest

gjest_class = gjest.Gjest()

class Rorbu:
    def __init__(self):
        self.gjester = []

    def leggTilGjest(self, gjestObjekt):
        gjest_class.underhold(1)
        self.gjester.append(gjestObjekt)

    def fortellVits(self, heltall):
        gjest_class.hentUnderholdningsverdi = heltall

    def hvorMorsomtHarViDet(self):
        if gjest_class.hentUnderholdningsverdi < 200:
            return "Kjedelig kveld"
        elif gjest_class.hentUnderholdningsverdi >= 200 and gjest_class.hentUnderholdningsverdi < 400:
            return "Dette var jo litt gøy"
        elif gjest_class.hentUnderholdningsverdi >= 400 and gjest_class.hentUnderholdningsverdi < 600:
            return "Dette var artig!"
        elif gjest_class.hentUnderholdningsverdi >= 600:
            return "Dra på Lopphavet - bi dæ godtar no så gyt e!"