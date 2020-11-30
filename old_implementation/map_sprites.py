import arcade
import tiles
import static_objects
import random
import os.path
from pyglet.gl import GL_NEAREST
from pyglet.gl import GL_LINEAR

SPRITE_SCALING = 1
TILE_SIZE = 32
BASE_MAP_TILE_SIZE = 64
SCALED_TILE_SIZE = TILE_SIZE * SPRITE_SCALING
TEXTURES_PATH = 'textures/'

import plants

class PlantSprite(arcade.Sprite):
    def __init__(self, filename: str, tile: tiles.Tile, scale: float=SPRITE_SCALING):
        super().__init__(filename,SPRITE_SCALING)
        self.tile = tile
        self.sprite_position = None
        self.alignment = None

class TileSprite(arcade.Sprite):

    def __init__(self, filename: str, tile: tiles.Tile, scale: float=SPRITE_SCALING):
        super().__init__(filename,SPRITE_SCALING)
        self.tile = tile
        self.sprite_position = None
        self.alignment = None



class SpriteMap(tiles.Map):

    sprite_alignment = {
        'single':('top_left','top_right','bottom_left','bottom_right'),
        'single_top':('top_left','top_right','left','right'),
        'single_left':('top_left','top','bottom_left','bottom'),
        'single_right':('top','top_right','bottom','bottom_right'),
        'single_bottom':('left','right','bottom_left','bottom_right'),
        'single_vertical':('left','right','left','right'),
        'single_horizontal':('top','top','bottom','bottom'),
        'left_bottom':('left','base','bottom_left','bottom'),
        'right_bottom':('base','right','bottom','bottom_right'),
        'left_top':('top_left','top','left','base'),
        'right_top':('top','top_right','base','right'),
        'left':('left','base','left','base'),
        'right':('base','right','base','right'),
        'bottom':('base','base','bottom','bottom'),
        'top':('top','top','base','base'),
        'middle':('base','base','base','base'),
    }

    def __init__(self, seed: str, size: int = tiles.MAP_SIZE,landscape: str = 'plain'):
        '''
        creates SpriteMap object.
        seed - int or str seed to initialize random-generation 
        size - int, size of map side in tiles. Map is a size x size square
        landscape - str. Name of lanscape type from tiles.Map.landscapes
        '''
        super().__init__(seed,size,BASE_MAP_TILE_SIZE*2,landscape)
        self.base_tiles_sprite_list = arcade.SpriteList(is_static=True)
        self.soil_sprite_list = arcade.SpriteList(is_static=True)
        self.water_sprite_list = arcade.SpriteList(is_static=True)
        self.landscape_sprite_list = arcade.SpriteList(is_static=True)
        self.st_objects = None
        self.forest = None
        self.soil_sprite_map = {}
        self.water_sprite_map = {}
        self.landscape_sprite_map = {}
        self.animated = []

    def map_sprite_coordinate(self,y:int,x:int,position:int) -> tuple:
        '''
        y - int, y-coordinate on map,
        x - int, x-coordinate on map,
        position - int in [0,1,2,3]. Each map tile consist of four sprites:
            0 - top-left
            1 - top-right
            2 - bottom-left
            3 - bottom-right
        return y and x coordinate on Window where left-bottom point of sprite will be rendered
        '''
        x_del = position%2
        y_del = 1-int(position/2)
        return ((y*2+y_del)*BASE_MAP_TILE_SIZE,(x*2+x_del)*BASE_MAP_TILE_SIZE)

    def get_base_texture_file(self) -> str:
        '''
        Returns path to base tile texture file depending of which kind of map was created.
        Types of base tiles is set depending on landscape type. 
        See tiles.Map.landscapes[landscape_name][base_tile]
        '''
        index = random.choice(['01','02','03','04'])
        file_path = f'{TEXTURES_PATH}base_tiles/{self.base_tile}_base{index}.png'
        if os.path.exists(file_path):
            return file_path
        else:
            return None
    
    def create_base_sprite(self,y: int,x: int) -> None:
        '''
        Creates four arcade.Sprite for base map tile with coordinates:
        y - int
        x - int
        '''
        for i in range(4):
            sprite = arcade.Sprite(self.get_base_texture_file(),SPRITE_SCALING)
            sprite_y, sprite_x = self.map_sprite_coordinate(y,x,i)
            sprite.left = sprite_x
            sprite.bottom = sprite_y
            self.base_tiles_sprite_list.append(sprite)

    def create_base_texture(self) -> None:
        '''
        Creates arcade.Sprites for the whole map
        '''
        for y in range(self.size):
            for x in range(self.size):
                self.create_base_sprite(y,x)

    def get_soil_texture_file(self, tile: tiles.Tile, position: int) -> str:
        '''
        Returns path to soil tile texture file depending on type of soil of tile.
        '''
        tile_type = 'soil'
        if tile.soil_modifier != None:
            index = random.choice(['01','02','03','04'])
            file_path = f'{TEXTURES_PATH}{tile.soil_modifier}/{tile.soil_modifier}_{self.sprite_alignment.get(tile.view[tile_type])[position]}{index}.png'
            if os.path.exists(file_path):
                return file_path
        return None

    def create_soil_sprite(self, tile: tiles.Tile) -> None:
        '''
        Creates four arcade.Sprite for landscape element of tile.
        '''
        if tile.soil_modifier != None:
            tile.calculate_view()
            sprite_alignment = self.sprite_alignment.get(tile.view['soil'])
            sprites = []
            for i in range(4):
                sprite = TileSprite(self.get_soil_texture_file(tile,i),tile,SPRITE_SCALING)
                sprite_y, sprite_x = self.map_sprite_coordinate(tile.y, tile.x,i)
                sprite.left = sprite_x
                sprite.bottom = sprite_y
                self.soil_sprite_list.append(sprite)
                sprites.append(sprite)
            self.soil_sprite_map[(tile.y,tile.x)] = sprites

    def create_soil(self) -> None:
        '''
        Creates soil sprites for all tiles with soil
        '''
        for tile in self.tiles:
            if tile.soil_modifier != None:
                self.create_soil_sprite(tile)

    def get_water_texture_file(self, tile: tiles.Tile, position: int) -> str:
        '''
        Returns path to soil tile texture file depending on type of soil of tile.
        '''
        tile_type = 'water'
        if tile.water_level != None:
            index = random.choice(['01','02','03','04'])
            file_path = f'{TEXTURES_PATH}water/water_{self.sprite_alignment.get(tile.view[tile_type])[position]}{index}.png'
            if os.path.exists(file_path):
                return file_path
        return None

    def create_water_sprite(self, tile: tiles.Tile) -> None:
        '''
        Creates four arcade.Sprite for water element of tile.
        '''
        if tile.water_level != None:
            tile.calculate_view()
            sprite_alignment = self.sprite_alignment.get(tile.view['water'])
            sprites = []
            for i in range(4):
                sprite = TileSprite(self.get_water_texture_file(tile,i),tile,SPRITE_SCALING)
                sprite_y, sprite_x = self.map_sprite_coordinate(tile.y, tile.x,i)
                sprite.left = sprite_x
                sprite.bottom = sprite_y
                self.water_sprite_list.append(sprite)
                sprites.append(sprite)
            self.water_sprite_map[(tile.y,tile.x)] = sprites

    def create_water(self) -> None:
        '''
        Creates water sprites for all tiles with water elements
        '''
        for tile in self.tiles:
            if tile.water_level != None:
                self.create_water_sprite(tile)

    def get_landscape_texture_file(self,tile: tiles.Tile,position: int) -> str:
        '''
        Returns path to landscape element texture file depending on type of landscape of tile.
        '''
        tile_type='entity'
        if tile.entity != None:
            index = random.choice(['01','02','03','04'])
            file_path = f'{TEXTURES_PATH}{tile.entity}/{tile.entity}_{self.sprite_alignment.get(tile.view[tile_type])[position]}{index}.png'
            if os.path.exists(file_path):
                return file_path
        return None
    
    def create_landscape_sprite(self, tile: tiles.Tile) -> None:
        '''
        Creates four arcade.Sprite for landscape element of tile.
        '''
        if tile.entity != None:
            tile.calculate_view()
            sprite_alignment = self.sprite_alignment.get(tile.view['entity'])
            sprites = []
            for i in range(4):
                sprite = TileSprite(self.get_landscape_texture_file(tile,i),tile,SPRITE_SCALING)
                sprite_y, sprite_x = self.map_sprite_coordinate(tile.y, tile.x,i)
                sprite.left = sprite_x
                sprite.bottom = sprite_y
                self.landscape_sprite_list.append(sprite)
                sprites.append(sprite)
            self.landscape_sprite_map[(tile.y,tile.x)] = sprites

    def create_landscape(self) -> None:
        '''
        Creates landscape sprites for all tiles with landscape elements
        '''
        for tile in self.tiles:
            if tile.entity != None:
                self.create_landscape_sprite(tile)

    def new_map(self):
        self.create_map()
        self.create_base_texture()
        self.create_soil()
        self.create_water()
        self.create_landscape()
        self.st_objects = static_objects.StaticObjects(self)
        self.st_objects.generate_random_objects()
        self.forest = plants.Forest(self)
        self.forest.create_random_forest()

        self.animated.append(self.forest.sprite_list)

    def draw_map(self):
        self.base_tiles_sprite_list.draw(filter=GL_NEAREST)
        self.soil_sprite_list.draw(filter=GL_NEAREST)
        self.water_sprite_list.draw(filter=GL_NEAREST)
        self.landscape_sprite_list.draw(filter=GL_NEAREST)
        self.st_objects.sprite_list.draw(filter=GL_NEAREST)
        self.forest.sprite_list.draw(filter=GL_NEAREST)