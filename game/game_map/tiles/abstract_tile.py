class Tile:

    def __init__(self):
        self.under = None
        self.over = None
        self._is_passable = True
        self._fertility = 1

    @property
    def under(self)->Tile:
        return self._under

    @under.setter
    def under(self, tile: Tile)->None:
        self._under = tile

    @property
    def over(self)->Tile:
        return self._over

    @over.setter
    def over(self, tile: Tile)->None:
        self._over = tile

    @property
    def is_passable(self)->bool:
        return self._is_passable

    @property
    def fertility(self)->float:
        return self._fertility



