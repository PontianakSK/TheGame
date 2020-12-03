from game_map.area.tiles.tile_builders import (  # type: ignore
    TileBuilder,
    BasicTile,
    tile_layers,
)


def test_tile_builder():

    builder = TileBuilder()

    heights = [threshold for threshold, _ in builder._layer_height_thresholds]
    heights.insert(0, 100)
    heights.append(-100)

    for height in heights:

        tile = builder.build(0, 0, height)

        assert isinstance(tile, BasicTile)

        layers = []

        for threshhold, layer in builder._layer_height_thresholds:

            if threshhold >= height:
                layers.append(layer)

        layers.reverse()
        layers.append(tile_layers.StoneLayer)
        tile_layer = tile.top_layer

        for layer in layers:
            error_message = f'{height=}\n {layers=}\n \n{tile=}'
            assert isinstance(tile_layer, layer), error_message
            tile_layer = tile_layer.lower_layer

    print(height)
