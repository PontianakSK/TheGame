import random
import perlin_noise

MAP_SIZE = 500

class Tile:
    views = {
        '00000':None,
        '00100':'single',
        '00101':'single_top',
        '00110':'single_left',
        '01100':'single_right',
        '10100':'single_bottom',
        '10101':'single_vertical',
        '01110':'single_horizontal',
        '10110':'left_bottom',
        '11100':'right_bottom',
        '00111':'left_top',
        '01101':'right_top',
        '10111':'left',
        '11101':'right',
        '11110':'bottom',
        '01111':'top',
        '11111':'middle',
    }

    def __init__(self, y: int, x: int, size: int=128):
        # coordinates
        self.x = x
        self.y = y
        self.height = None
        self.size = size
        # neighbours
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None
        # Nonbasic soil if exists on this tile (sand or grass etc.)
        self.soil_modifier = None
        # object under tile
        self.deep = None
        # Depth of water for flooded cells
        self.water_level = None
        # object on the tile
        self.entity = None
        # human made coating (floor)
        self.coating = None
        # Nonlandscape objects on this cell (trees and stones are also nonlandscape objects)
        self.items = []
        # texture view depending on adjacent tiles
        self.view = {
            'soil' : None,
            'water': None,
            'entity': None,
            'coating': None,
        }
        #Ability of tile to grow plants 
        self.fertility = None

    def __str__(self):
        return f'y:{self.y},x:{self.x}\n'\
            f'soil_modifier:{self.soil_modifier}\n'\
            f'entity:{self.entity}\n'\
            f'water_level:{self.water_level}\n'\
            f'coating:{self.coating}\n'\
            f'deep:{self.deep}\n'\
            f'view:{self.view}\n\n'\

    def set_neighbours(self,neighbours: dict) -> None:
        '''
        Set all neighbour-attributes of tile to tiles from neighbours dict
        '''
        self.top = neighbours.get((1,0))
        self.bottom = neighbours.get((-1,0))
        self.left = neighbours.get((0,-1))
        self.right = neighbours.get((0,1))
        self.top_left = neighbours.get((1,-1))
        self.top_right = neighbours.get((1,1))
        self.bottom_left = neighbours.get((-1,-1))
        self.bottom_right = neighbours.get((-1,1))

    def compare_soil_alignment(self, other) -> str:
        '''
        Checks if this tile and other tile have the same material on soil level
        returns '1' is True '0' if False. If this tile have nothing on this level
        returns always '0'
        '''
        if other == None:
            return '0'
        elif self.soil_modifier == None:
            return '0'
        elif other.soil_modifier == None:
            return '0'
        alignment = int(self.soil_modifier == other.soil_modifier)
        return str(alignment)

    def compare_water_alignment(self, other) -> str:
        '''
        Checks if this tile and other tile have the same water level
        returns '1' is True '0' if False. If this tile is not flooded (water_level = None)
        returns always '0'
        '''
        if other == None:
            return '0'
        elif self.water_level == None:
            return '0'
        elif other.water_level == None:
            return '0'
        alignment = int(self.water_level == other.water_level)
        return str(alignment)

    def compare_entity_alignment(self, other) -> str:
        '''
        Checks if this tile and other tile have the same abject on entity level
        returns '1' is True '0' if False. If this tile have nothing on this level
        returns always '0'
        '''
        if other == None:
            return '0'
        elif self.entity == None:
            return '0'
        elif other.entity == None:
            return '0'
        alignment = int(self.entity == other.entity)
        return str(alignment)

    def compare_coating_alignment(self, other) -> str:
        '''
        Checks if this tile and other tile have the same type of coating
        returns '1' is True '0' if False. If this tile have no coating
        returns always '0'
        '''
        if other == None:
            return '0'
        elif self.coating == None:
            return '0'
        elif other.coating == None:
            return '0'
        alignment = int(self.coating == other.coating)
        return str(alignment)

    def calculate_view(self) -> None:
        '''
        Check adjacent tiles and set view (see Tile.views) for future texture assignment
        '''
        soil_view = ''
        water_view = ''
        entity_view = ''
        coating_view = ''
        for neighbour in [self.top, self.left,self,self.right,self.bottom]:
            soil_view+=self.compare_soil_alignment(neighbour)
            water_view+=self.compare_water_alignment(neighbour)
            entity_view+=self.compare_entity_alignment(neighbour)
            coating_view+=self.compare_coating_alignment(neighbour)
        self.view['soil'] = self.views[soil_view]
        self.view['water'] = self.views[water_view]
        self.view['entity'] = self.views[entity_view]
        self.view['coating'] = self.views[coating_view]
    
class BasicSoil(Tile):

    def __init__(self, y, x):
        super().__init__(y,x)

class Sand(BasicSoil):
    def __init__(self,y,x):
        super().__init__(y,x)
        self.soil_modifier = 'sand'

class Grass(BasicSoil):
    def __init__(self,y,x):
        super().__init__(y,x)
        self.soil_modifier = 'grass'
        self.fertility = 1

class Water(Sand):

    def __init__(self, y, x):
        super().__init__(y,x)
        self.water_level = 1

class Rock(BasicSoil):

    def __init__(self, y, x):
        super().__init__(y,x)
        self.entity = 'rock'

class Map:

    #Landcape is a dictionary of parameers used to creates a map
    #It describes type of basic soil and distribution of landscape types by height
    landscapes = {
        'plain' : {
            'tiles': [
                (Rock,  1.25, 2),
                (Grass, 0.55,1.1),
                (Sand, 0.5,0.55),
                (Water, 0,0.5),
            ],
            'base_tile':'soil',
            'forest':{
                'type':'mixed',
                'density': 0.05,
            },
        },
    }
    def __init__(self, seed: str, size: int = MAP_SIZE, tile_size: int = 128, landscape: str = 'plain') -> None:
        '''
        Creates Map object.
        seed - int or str seed to initialize random-generation 
        size - int, size of map side in tiles. Map is a size x size square
        landscape - str. Name of lanscape type from self.landscapes
        tile_size - size of basic tile of map in pixels
        '''
        self.landscape = landscape
        self.seed = seed
        random.seed(self.seed)
        self.size = size
        self.tile_size = tile_size
        self.tiles = []
        self.base_tile = self.landscapes[self.landscape]['base_tile']
        self.tile_distribution = self.landscapes[self.landscape]['tiles']

    def __str__(self):
        return f'seed:{self.seed}\n'\
            f'landscape:{self.landscape}\n'\
            f'size:{self.size}\n'\

    def index(self,y: int,x: int) -> int:
        '''
        Returns index of tile with
        y - int
        x - int
        coordinates in self.tiles list. Or None if tile is outside of map
        '''
        if 0 <= y < self.size and 0 <= x < self.size:
            return y*self.size+x
        else:
            return None
    
    def coordinates(self,index: int) -> tuple:
        '''
        returns (y,x) - coordinates of tile under
        index - int 
        in self.tiles list. Or None if index is out of range.
        Attention: Does not check if such element exists. Only check that index is
        allowable depending on map size
        '''
        if 0 <= index < self.size**2:
            x = index%self.size
            y = int((index-x)/self.size)
            return (y,x)
        else:
            return None

    def create_basic(self) -> None:
        '''
        Creates whole map landscape using Perlin noise generator. Perlin noise generator provides
        height for each tile. Depending on disctribution of tiles per height from self.landscapes
        tiles are created.
        '''
        perlin = perlin_noise.PerlinNoise(10,self.seed)
        for y in range(0,self.size):
            for x in range(0,self.size):
                tile = None
                tile_height = perlin.perlin(y/self.size,x/self.size)
                for each in self.tile_distribution:
                    if each[1] < tile_height <= each[2]:
                        tile = each[0](y,x)
                if tile == None:
                    tile = BasicSoil(y,x)
                tile.height = tile_height
                tile.size = self.tile_size
                self.tiles.append(tile)

    def neighbour_index(self,y:int,x:int) -> dict:
        '''
        Returns a dict of idices of tiles adjacent to tile with coordinates:
        y - int
        x - int
        keys of dict are tuples of biase of neighbours to y and x. For instance (-1,0)
        '''
        result = {}
        for y_del in [-1,0,1]:
            for x_del in [-1,0,1]:
                if y_del == x_del == 0:
                    pass
                else:
                    index = self.index(y+y_del,x+x_del)
                    if index != None:
                        result[y_del,x_del] = index
        return result
    
    def neighbour_index_cross(self,y: int,x: int) -> dict:
        '''
        Returns top, left, bottom and right tiles adjasent to tile with coordinates:
        y - int
        x - int
        keys of dict are tuples of biase of neighbours to y and x. For instance (-1,0)
        '''
        neighbours = self.neighbour_index(y,x)
        result = {neighbour[0]:neighbour[1] for neighbour in neighbours.items() if neighbour[0][0] == 0 or neighbour[0][1] == 0}
        print(result)

    def get_neighbours(self,y: int,x: int) -> dict:
        '''
        Returns a dict of tiles adjacent to tile with coordinates:
        y - int
        x - int
        keys of dict are tuples of biase of neighbours to y and x. For instance (-1,0)
        '''
        index_dict = self.neighbour_index(y,x)
        return {neighbour[0]:self.tiles[neighbour[1]] for neighbour in index_dict.items()}

    def get_tile(self,y: int,x: int) -> Tile:
        '''
        Returns a Tile-object of tile with coordinates:
        y - int
        x - int
        If coordinates are outside of map, returns None
        '''
        index = self.index(y,x)
        if index != None:
            return self.tiles[index]
        else:
            return None

    def chain_tiles(self) -> None:
        '''
        For each tile on map sets its neighbours to adjacent tiles
        '''
        for tile in self.tiles:
            neighbours = self.get_neighbours(tile.y,tile.x)
            tile.set_neighbours(neighbours)

    def set_views(self):
        '''
        Set views for each tile in self.tiles
        '''
        for tile in self.tiles:
            tile.calculate_view()

    def create_map(self) -> None:
        '''
        Generates whole map, set views, neighbours.
        '''
        self.create_basic()
        self.chain_tiles()
        self.set_views()

    def get_tiles(self, bottom_left: tuple, top_right: tuple):
        result = []
        for y in range(bottom_left[0],top_right[0]+1):
            for x in range(bottom_left[1],top_right[1]+1):
                tile = self.get_tile(y,x)
                if tile != None:
                    result.append(tile)
        return result

                







