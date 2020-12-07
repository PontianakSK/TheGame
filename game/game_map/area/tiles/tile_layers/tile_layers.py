from game_map.area.tiles.tile_layers.abstract_tile_layer import (
    TileLayer,
    InteractiveObject,
)

# Different tile layers. Specific tile layer
# affects tile texture, ability of other
# objects to walk through and grow on this
# tile.


class WaterLayer(TileLayer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._fertility = 0

    # Nobody can walk through water.
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
