import random
import os
import game_objects
import arcade
import tiles

TEXTURES_PATH = 'textures/static_objects/'

class StaticMapObject(game_objects.GameObject):
    def __init__(self):
        super().__init__()
        self.size = None
        self.left = None
        self.bottom = None

class StaticObjects:
    def __init__(self, game_map: tiles.Map):
        self.game_map = game_map
        self.sprite_list = arcade.SpriteList()
        self.static_objects_list = []
        self.textures = self.prepare_texture_paths()

    def prepare_texture_paths(self):
        '''
        Returns a dict of paths to texture images. Used in __init__ only
        '''
        static_textures = {}
        texture_folders = os.listdir(TEXTURES_PATH)
        for each in texture_folders:
            path = f'{TEXTURES_PATH}{each}'
            if os.path.isdir(path):
                list_of_textures = [f'{TEXTURES_PATH}{each}/{x}' for x in os.listdir(path) if x[-3:] == 'png']
                static_textures[each] = list_of_textures
        return static_textures

    def create(self, tile: tiles.Tile, texture: str,scale: int = 1) -> None:
        '''
        Creates new static object on specified tile with chosen texture.
        '''
        new_object = StaticMapObject()
        new_object.texture = texture
        new_object.sprite = arcade.Sprite(texture,scale)
        new_object.size = (new_object.sprite.height, new_object.sprite.width)
        new_object.bottom = random.random()+tile.y
        new_object.sprite.bottom = int(new_object.bottom*tile.size)
        new_object.left = random.random()+tile.x
        new_object.sprite.left = int(new_object.left*tile.size)
        new_object.tiles = self.game_map.get_tiles(
            (
                int(new_object.bottom),
                int(new_object.left)
                ),
            (
                int(new_object.bottom+new_object.size[0]/tile.size),
                int(new_object.left+new_object.size[1]/tile.size)
                )
            )
        for tile in new_object.tiles:
            if tile.entity != None:
                return None
        for tile in new_object.tiles:
            tile.entity = new_object
        self.sprite_list.append(new_object.sprite)
        self.static_objects_list.append(new_object)

    def generate_random_objects(self):
        '''
        Creates random static objects for the whole map
        '''
        for tile in self.game_map.tiles:
            if tile.entity == None and tile.water_level == None and tile.coating == None:
                modifier = tile.soil_modifier
                if modifier == None:
                    modifier = 'base'
                if tile.view['soil'] == 'middle' or modifier == 'base':
                    decision = random.random()
                    if decision > 0.9:
                        texture = random.choices(self.textures[modifier])[0]
                        self.create(tile,texture)




