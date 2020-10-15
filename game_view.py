import arcade
import map_sprites
import interface

class MapView:

    VIEW_HEIGHT = 720
    VIEW_WIDTH = 900

    def __init__(self):
        self.screen_center_list = None
        self.screen_center = None
        self.view_left = 0
        self.view_bottom = 0
        self.screen_change = True
        self.scaling = 1
        self.view_scale_x = self.VIEW_WIDTH
        self.view_scale_y = self.VIEW_HEIGHT
        self.view_left = 0
        self.view_bottom = 0
        self.view_right = self.view_scale_x
        self.view_top = self.view_scale_y
        self.interface = None

    def new_view(self, y: int, x: int):
        '''
        Creates initial game view  frame at point y,x
        '''
        self.screen_center_list = arcade.SpriteList()
        self.screen_center = arcade.Sprite(f'{map_sprites.TEXTURES_PATH}water.png', 1)         
        self.screen_center.center_y = y
        self.screen_center.center_x = x
        self.screen_center.alpha = 50
        self.screen_center_list.append(self.screen_center)
        self.view_scale_x = self.VIEW_WIDTH
        self.view_scale_y = self.VIEW_HEIGHT
        self.view_left = x-self.view_scale_x/2
        self.view_bottom = y-self.view_scale_y/2
        self.view_right = x+self.view_scale_x/2
        self.view_top = y+self.view_scale_y/2
        self.interface = interface.Interface(self.view_scale_y,self.view_scale_x,y,x,self.scaling)
        
    def draw(self):
        self.screen_center_list.draw()
        self.interface.draw_static()

    def scale(self, value: int):
        '''
        Scale view frame by value
        '''
        if self.view_scale_y+value < 720:
            self.view_scale_y = 720
        elif self.view_scale_y+value > 10000:
            self.view_scale_y = 10000
        else:
            self.view_scale_y += value
        self.view_scale_x = self.view_scale_y*1.25
        self.scaling = self.view_scale_y/self.VIEW_HEIGHT
        self.screen_center_list.rescale(self.scaling/self.screen_center.scale)
        self.interface.height = self.view_scale_y
        self.interface.width = self.view_scale_x
        self.interface.scaling = self.scaling
        self.screen_change = True



    def move_left(self):
        '''
        Starts moving view frame left
        '''
        self.screen_center.change_x = -self.view_scale_x/100
        self.screen_change = True
    def move_right(self):
        '''
        Starts moving view frame right
        '''
        self.screen_center.change_x = self.view_scale_x/100
        self.screen_change = True
    def move_up(self):
        '''
        Starts moving view frame up
        '''
        self.screen_center.change_y = self.view_scale_x/100
        self.screen_change = True
    def move_down(self):
        '''
        Starts moving view frame down
        '''
        self.screen_center.change_y = -self.view_scale_x/100
        self.screen_change = True

    def stop_left(self):
        '''
        Stops moving view frame left
        '''
        self.screen_center.change_x = 0
        self.screen_change = False
    def stop_right(self):
        '''
        Stops moving view frame right
        '''
        self.screen_center.change_x = 0
        self.screen_change = False
    def stop_up(self):
        '''
        Stops moving view frame up
        '''
        self.screen_center.change_y = 0
        self.screen_change = False
    def stop_down(self):
        '''
        Stops moving view frame down
        '''
        self.screen_center.change_y = 0
        self.screen_change = False

    def change_view(self):
        '''
        Resizes view frame
        '''
        if self.screen_change is True:
            self.screen_center.center_x+=self.screen_center.change_x
            self.screen_center.center_y+=self.screen_center.change_y
            self.view_left =  self.screen_center.position[0]-self.view_scale_x/2
            self.view_right = self.screen_center.position[0]+self.view_scale_x/2
            self.view_bottom = self.screen_center.position[1]-self.view_scale_y/2
            self.view_top = self.screen_center.position[1]+self.view_scale_y/2
            self.interface.center_x = self.screen_center.center_x
            self.interface.center_y = self.screen_center.center_y


    def update(self):
        self.change_view()
        arcade.set_viewport(
            self.view_left,
            self.view_right,
            self.view_bottom,
            self.view_top
            )

    def in_view(self, sprite_list: arcade.SpriteList) -> arcade.SpriteList():
        in_view_list = arcade.SpriteList()
        for each_sprite in sprite_list:
                if (
                    self.view_left-each_sprite.width/2 <= each_sprite.center_x <= self.view_right+each_sprite.width/2
                    and
                    self.view_bottom-each_sprite.height/2 <= each_sprite.center_y <= self.view_top+each_sprite.height/2
                ):
                    in_view_list.append(each_sprite)
        return in_view_list
    
    
