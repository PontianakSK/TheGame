import arcade
import map_sprites
import game_state
import game_view
from pyglet.gl import GL_NEAREST
from pyglet.gl import GL_LINEAR


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 720
MAP_HEIGHT = 50
MAP_WIDTH = 50
SCALED_SIZE = int(MAP_HEIGHT*map_sprites.BASE_MAP_TILE_SIZE/map_sprites.SCALED_TILE_SIZE)


        

class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.to_animate = arcade.SpriteList()
        print('Init done')

    def setup(self):
        print('setup_started')
        self.state = game_state.GameState()
        print('Game State created')
        self.state.create_new_game('Fuck',100)
        print('Game created')
        arcade.set_background_color(arcade.color.DARK_BROWN)
        print('setup_done')

    def on_draw(self):

        arcade.start_render()
        self.state.draw()
        #output = self.state.time.__str__()
        #self.timer = arcade.draw_text(output, 300, 300, arcade.color.WHITE, 32)
        


    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        print(scroll_y//10)
        self.state.view_frame.scale((scroll_y//10)*100)
        return super().on_mouse_scroll(x, y, scroll_x, scroll_y)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.state.view_frame.move_left()
        elif key == arcade.key.RIGHT:
            self.state.view_frame.move_right()
        elif key == arcade.key.UP:
            self.state.view_frame.move_up()
        elif key == arcade.key.DOWN:
            self.state.view_frame.move_down()
        elif key == arcade.key.EQUAL:
            self.state.time.plus_speed()
        elif key == arcade.key.MINUS:
            self.state.time.minus_speed()
        elif key == arcade.key.SPACE:
            self.state.time.stop()
        elif key == arcade.key.BRACELEFT:
            self.state.view_frame.scale(-100)
        elif key == arcade.key.BRACERIGHT:
            self.state.view_frame.scale(100)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.state.view_frame.stop_left()
        elif key == arcade.key.RIGHT:
            self.state.view_frame.stop_right()
        elif key == arcade.key.UP:
            self.state.view_frame.stop_up()
        elif key == arcade.key.DOWN:
            self.state.view_frame.stop_down()

    def update(self, delta_time):
        if self.state.view_frame.screen_change is True:
            self.state.view_frame.update()
            self.to_animate = arcade.SpriteList()
            for each_list in self.state.map.animated:
                self.to_animate.extend(self.state.view_frame.in_view(each_list))
        self.state.increase_time(delta_time)
        self.to_animate.update_animation()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()

main()