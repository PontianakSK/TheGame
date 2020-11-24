from game_map.tiles import tile_layers

TILE_LAYERS = [
    tile_layers.GrassLayer,
    tile_layers.SandLayer,
    tile_layers.SoilLayer,
    tile_layers.StoneLayer,
    tile_layers.WaterLayer,
]

def test_layer_constructors():

    previous = None
    
    for layer_class in TILE_LAYERS:
        layer = layer_class(lower_layer=previous)
        previous = layer

    from_bottom = previous
    previous = None
    
    for layer_class in TILE_LAYERS[::-1]:
        layer = layer_class(upper_layer=previous)
        previous = layer
    
    layer = previous
    while layer.upper_layer:
        layer = layer.upper_layer
    from_top = layer
    previous = None

    while from_top.lower_layer or from_bottom.lower_layer:
        assert isinstance(from_top,from_bottom.__class__)
        assert from_top.fertility == from_bottom.fertility
        assert from_top.is_passable == from_bottom.is_passable
        from_top = from_top.lower_layer
        from_bottom = from_bottom.lower_layer

def test_binding():

    layer_1 = TILE_LAYERS[0]()
    layer_2 = TILE_LAYERS[-1]()
    tile_layers.TileLayer.bind_layers(layer_1,layer_2)
    assert layer_1.lower_layer is layer_2
    assert layer_2.upper_layer is layer_1


def test_repr():

    previous = None
    starting = None
    for layer_class in TILE_LAYERS:
        layer = layer_class(lower_layer=previous)
        
        if not starting:
            starting = layer

        previous = layer

    assert len(previous.__repr__()) == len(starting.__repr__())
        

    
