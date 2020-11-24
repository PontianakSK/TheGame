from game_map.tiles.abstract_tile_layer import TileLayer

class WaterLayer(TileLayer):
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._is_passable = False
        self._fertility = 0

class SandLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._fertility = 0

class SoilLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._fertility = 0.2

class GrassLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

class StoneLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)
        self._fertility = 0