from game_map.area.tiles.tile_layers.abstract_tile_layer import (
    TileLayer,
    InteractiveObject,
)


class WaterLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._fertility = 0

    def pass_adventurer(self, adventurer: InteractiveObject):

        return False


class SandLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._fertility = 0


class SoilLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._fertility = 0.2


class StoneLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._fertility = 0
