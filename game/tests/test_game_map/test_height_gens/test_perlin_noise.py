import pytest

from game_map.height_gens.perlin_noise import PerlinNoise
from game_map.height_gens.abstract_gen import TileHeightGenerator
from tests.settings import RANDOM_SEED

perlin_noise = PerlinNoise(10,RANDOM_SEED)

#All height values below are checked with RANDOM_SEED == 'test'

def test_initiating():
    assert isinstance(perlin_noise,TileHeightGenerator)
    assert len(perlin_noise._gradients) == 100

def test_node_values():
    assert perlin_noise.get_height(0,0) == 1.390227352830289
    assert perlin_noise.get_height(1,1) == 1.3769552274256966

def test_out_of_map_coords():
    with pytest.raises(KeyError) as excinfo:
        perlin_noise.get_height(10,10)
    assert 'Point(y=90, x=90)' in str(excinfo.value)
    with pytest.raises(KeyError) as excinfo:
        perlin_noise.get_height(-1,-1)
    assert 'Point(y=-9, x=-9)' in str(excinfo.value)

def test_internal_values():
    assert perlin_noise.get_height(0.01,0.01) == 1.1447048249401355 