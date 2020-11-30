import game_objects
import map_sprites
import arcade
import os
import tiles
import random

TEXTURES_PATH = f'{map_sprites.TEXTURES_PATH}/plants/'

class Plant(game_objects.GameObject):
        def __init__(self):
            super().__init__()
            self.size = None
            self.soil_type = None
            self.growth = 0
            self.growth_rate = 0
            self.seed_range = 0
            self.seeding_age = 0
            self.seeding_frequency = 0
            self.texture_path = None
            self.tile = None

        def grow(self):
            fertility = 0
            if self.tiles != []:
                for each_tile in self.tiles:
                    fertility+=each_tile.fertility
                fertility = fertility/len(self.tiles)
            self.growth += self.growth_rate*fertility

class Tree(Plant):

    tree_sizes = [
        'seed',
        'small',
        'medium',
        'big',
        ]

    def __init__(self, number: int, size: str):
        super().__init__()
        self.id = number
        self.type = f'tree_{number}'
        self.size = size
        self.update_texture()
        self.growth_rate = 10
        self.seed_range = 2
        self.seeding_age = 110
        self.seeding_frequency = 0.5

    def grow(self):
        super().grow()
        if self.growth >= 100:
            new_size_index = self.tree_sizes.index(self.size)+1
            if new_size_index < len(self.tree_sizes):
                if self.sprite != None:
                    print('Before Kill',self.sprite.sprite_lists)
                    for each_list in self.sprite.sprite_lists:
                        each_list.remove(self.sprite)
                    self.sprite.sprite_lists.clear()
                    print('Kill',self.sprite.sprite_lists)
                self.size = self.tree_sizes[new_size_index]
                self.update_texture()
                self.create_sprite()
                self.growth = 0
                if self.sprite != None:
                    self.sprite_changed = True
                

    def update_texture(self):
        '''
        Updates path to texture file depending on type and size of tree
        '''
        if self.size == 'seed':
            self.texture = None
        else:
            self.texture = f'{TEXTURES_PATH}trees/{self.type}/{self.size}'

    def create_sprite(self):
        '''
        Creates animated sprite for tree
        '''
        if self.texture != None:
            self.sprite = arcade.AnimatedTimeBasedSprite()
            self.sprite.frames = []
            texture_folders = os.listdir(self.texture)
            texture_folders.sort()
            for each in texture_folders:
                texture = arcade.AnimationKeyframe(0,200,arcade.load_texture(f'{self.texture}/{each}'))
                self.sprite.frames.append(texture)
            self.sprite.texture = self.sprite.frames[0].texture

class Forest:
    tree_ids = {
        'mixed': [1,2,3],
    }

    def __init__(self, game_map: tiles.Map):
        self.type_ = game_map.landscapes[game_map.landscape]['forest']['type']
        self.density = game_map.landscapes[game_map.landscape]['forest']['density']
        self.game_map = game_map
        self.sprite_list = arcade.SpriteList()
        self.tree_list = []

    def create_tree(self, tile: tiles.Tile, id: int, size: str, growth: int):
        '''
        Creates tree of specified id and size on tile. Appends that tree to list of trees and
        to sprite list of forest.
        '''
        tiles = self.game_map.get_tiles((tile.y-1,tile.x-1),(tile.y+1,tile.x+1))
        if tiles == []:
            return None
        for each in tiles:
            if each.entity != None or each.fertility == None:
                return None
        tree = Tree(id,size)
        tree.tile = tile
        for each in tiles:
            each.entity = tree
            tree.tiles.append(each)
        bottom = random.random()+tile.y
        tree.render_bottom = int(bottom*tile.size)
        center = random.random()+tile.x
        tree.render_center_x = int(center*tile.size)
        tree.growth = growth
        tree.create_sprite()
        if tree.sprite != None:
            tree.sprite.bottom = tree.render_bottom
            tree.sprite.center_x = tree.render_center_x
            self.sprite_list.append(tree.sprite)
        self.tree_list.append(tree)

    def create_random_tree(self, tile: tiles.Tile):
        '''
        Creates tree with random type and size
        '''
        id_ = random.choice(self.tree_ids[self.type_])
        size = random.choice(Tree.tree_sizes)
        growth = int(100*random.random())
        self.create_tree(tile,id_,size,growth)

    def create_random_forest(self):
        for tile in self.game_map.tiles:
            if random.random()<self.density:
                self.create_random_tree(tile)

    def grow(self):
        for each_tree in self.tree_list:
            each_tree.grow()
            if each_tree.sprite_changed:
                each_tree.sprite.bottom = each_tree.render_bottom
                each_tree.sprite.center_x = each_tree.render_center_x
                self.sprite_list.append(each_tree.sprite)
                each_tree.sprite_changed = False

    def seed(self):
        for each_tree in self.tree_list:
            if each_tree.seeding_age < each_tree.growth:
                if random.random() < each_tree.seeding_frequency:
                    tile = each_tree.tile
                    range_ = each_tree.seed_range
                    tiles = self.game_map.get_tiles((tile.y-range_-1,tile.x-range_-1),(tile.y+range_+1,tile.x+range_+1))
                    appropriate_tiles = [each for each in tiles if each.entity == None]
                    tile_to_seed = random.choice(appropriate_tiles)
                    print('SEED!!!',f'Sprites:{len(self.sprite_list)}, Trees:{len(self.tree_list)}')
                    self.create_tree(tile_to_seed, each_tree.id, 'seed',0)


        
        
'''
class MyWindow(arcade.Window):

    def __init__(self):
        super().__init__(200, 200)

    def setup(self):
        t = Tree(1,'big')
        t.create_sprite()
        self.sprite = t.sprite
        self.sprite_list = arcade.SpriteList()
        self.sprite.center_x = 100
        self.sprite.center_y = 100
        self.sprite_list.append(self.sprite)
        print(self.sprite.texture)
        print('setup_done')

    def on_draw(self):
        arcade.start_render()
        self.sprite_list.draw()
        return super().on_draw()

    def on_update(self, delta_time):
        self.sprite_list.update_animation()
        #return super().on_update(delta_time)

        




window = MyWindow()
window.setup()
arcade.run()
'''