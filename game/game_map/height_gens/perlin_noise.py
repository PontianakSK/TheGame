from collections import namedtuple
from itertools import product
from math import ceil, floor
import random

from game_map.height_gens.abstract_gen import TileHeightGenerator #type: ignore

Point = namedtuple('Point','y x')
Gradient = namedtuple('Gradient', 'y x')
AbsCoordDiff = namedtuple('AbsCoordDiff','diff_y diff_x')

class PerlinNoise(TileHeightGenerator):
    '''
        Generator of Perlin noise for 2d space
        frequency - number of random gradients along axis
        seed - random seed
    '''



    def __init__(self,frequency, seed=None):
    
        if seed != None:
            random.seed(seed)
        self.gradients = {}
        self.frequency = frequency
        self.set_gradients()



    def set_gradients(self):
        '''
            Set initial gradients for grid nodes
        '''

        x_len = range(self.frequency)
        y_len = range(self.frequency)

        for y,x in product(y_len,x_len):
            point = Point(y, x)
            self.gradients[point] = Gradient(random.random(),random.random())
    
    def get_height(self, y_perc: float, x_perc: float)->float:
        '''
            Returns perlin noise for coordinates y_perc, x_perc
            y_perc, x_perc - y, x coordinate from range(0,1),
            assumed that y_perc = (y-y_min)/(y_max-y_min),
            where y_min, y_max - starting, ending points
            of area noise is created for.
        '''

        return self.perlin(y_perc, x_perc)



    @staticmethod
    def abs_diff(coords_1: Point, coords_2: Point)->AbsCoordDiff:
        '''
            Returns difference modulus between coords_1, coords_2 for each coordinate
        '''

        diff = AbsCoordDiff(abs(coords_1.y - coords_2.y), abs(coords_1.x - coords_2.x))

        return diff



    def node_impact(self,coords: Point,node_coords: Point)->float:
        '''
            Calculates impact of node gradient in point
            with coords.
        '''
        diff = self.abs_diff(coords, node_coords)

        if diff.diff_x <=1 and diff.diff_y <= 1:
            grad = self.gradients[node_coords]
            node_impact = (1-diff.diff_y)*grad.y + (1-diff.diff_x)*grad.x
            range_weighted_impact = node_impact*(1-diff.diff_y)*(1-diff.diff_x)
            return range_weighted_impact

        return 0
        


    def perlin(self,y_perc: float,x_perc: float)->float:
        '''
            Returns perlin noise for coordinates y_perc, x_perc
            y_perc, x_perc - y, x coordinate from range(0,1),
            assumed that y_perc = (y-y_min)/(y_max-y_min),
            where y_min, y_max - starting, ending points
            of area noise is created for.
        '''
        target_point = Point(y_perc*(self.frequency-1),x_perc*(self.frequency-1))

        min_x = floor(target_point.x)
        max_x = ceil(target_point.x)
        min_y = floor(target_point.y)
        max_y = ceil(target_point.y)        
        closest_nodes = []

        for y,x in product((min_y,max_y),(min_x,max_x)):
            node = Point(y,x)
            closest_nodes.append(node)

        perlin_noise:float = 0

        for node in closest_nodes:
            perlin_noise += self.node_impact(target_point, node)

        return perlin_noise
