import random
import itertools
import terraformer_class

class TexturesMap:
    TEXTURES_PATH = 'mappack/PNG/'

    map_tiles = {
        0: 'base_land',
        1: 'desert',
        2: 'grass',
        3: 'rock',
        4: 'snow',
        5: 'soil',
        6: 'water',
    }

    map_digits = {each[1]:each[0] for each in map_tiles.items()}

    def __init__(self, size=50):
        self.map_grid = []
        self.size = size
        self.terrain = 'soil'
        for i in range(0,size):
            row_ = []
            for j in range(0,size):
                row_.append(0)
            self.map_grid.append(row_)

    def __str__(self):
        list_map = []
        for row_ in self.map_grid:
            list_row = []
            for cell_ in row_:
                list_row.append(str(cell_))
            list_map.append(','.join(list_row))
        return '\n'.join(list_map)

    def export_map(self, terraformer):
        terraformer.terrain_map = self.map_grid

    def import_map(self, terraformer):
        self.map_grid = terraformer.terrain_map



    def create_objects(self, type_, count):
        current_map = terraformer_class.Terraformer(50, self.size, self.size)
        self.export_map(current_map)
        objects_map = terraformer_class.Terraformer(50, self.size, self.size)
        objects = objects_map.get_random_areas(type_.length,type_.width,type_.density,count)
        for each in objects:
            print(each)
            each.create_object(type_.pattern)
            each.set_terrain(self.map_digits[type_.texture_type])
            objects_map.apply_terrain_map(each)
        current_map.apply_terrain_map(objects_map)
        self.import_map(current_map)

    def cover_terrain(self, terrain_texture):
        self.terrain = terrain_texture

    def create_map(self, map_type):
        map_= map_type(self.size)
        for object_, count in map_.objects_dict.items():
            self.create_objects(object_(),count)
        self.cover_terrain(map_.cover)
    
    def map_to_text(self):
        text_map = []
        for i in range(self.size):
            row_ = []
            for j in range(self.size):
                row_.append(self.map_tiles[self.map_grid[i][j]])
            text_map.append(row_)
        return text_map

        

class TerrainObject:
    def __init__(self):
        self.pattern = 'hill'
        self.texture_type = None
        self.length = 10
        self.width = 10
        self.density = 50

class Pond(TerrainObject):
    def __init__(self):
        super().__init__()
        self.texture_type = 'water'
        self.length = 10
        self.width = 10
        self.density = 80

class Hill(TerrainObject):
    def __init__(self):
        super().__init__()
        self.texture_type = 'rock'
        self.length = 10
        self.width = 10
        self.density = 70

class BasicMap:
    def __init__(self, size = 50):
        self.size = size
        self.objects_dict = {
            Pond : int(size/50),
            Hill : int(size/25),
        }
        self.cover = 'soil'

"""map_ = TexturesMap(50)
map_.create_map(BasicMap)
#map_.create_objects(Hill(),4)
#map_.cover_terrain('soil')
print(map_.map_to_text())"""
