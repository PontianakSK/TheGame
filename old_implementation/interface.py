import arcade

class Interface:

    BOTTOM_BACKGROUN_HEIGHT = 180
    TOP_BACKGROUN_HEIGHT = 20
    FONT_SIZE = 12
    
    def __init__(self, height, width, center_y, center_x, scaling):
        self.height = height
        self.width = width
        self.center_y = center_y
        self.center_x = center_x
        self.scaling = scaling
        self.background = arcade.SpriteList()
        self.top_rectangle = None
        self.bottom_rectangle = None


    def left(self):
        return self.center_x - self.width/2
    def right(self):
        return self.center_x + self.width/2
    def top(self):
        return self.center_y + self.height/2
    def bottom(self):
        return self.center_y - self.height/2


    def draw_background(self):
        '''
        Draws interface background
        '''
        self.bottom_rectangle = arcade.draw_lrtb_rectangle_filled(
            self.left(),
            self.right(),
            self.bottom()+self.BOTTOM_BACKGROUN_HEIGHT*self.scaling,
            self.bottom(),
            arcade.color.DARK_BYZANTIUM
            )
        self.top_rectangle = arcade.draw_lrtb_rectangle_filled(
            self.left(),
            self.right(),
            self.top(),
            self.top()-self.TOP_BACKGROUN_HEIGHT*self.scaling,
            arcade.color.DARK_BYZANTIUM
            )
    
    def draw_time(self,date,hours,minutes):
        '''
        Draws current date and time
        '''
        date = arcade.draw_text(f'{date}  ',self.left(),self.top()-(self.TOP_BACKGROUN_HEIGHT+1)*self.scaling,arcade.color.WHITE,self.FONT_SIZE*self.scaling)
        hour = arcade.draw_text(f'{hours}',date.right,self.top()-(self.TOP_BACKGROUN_HEIGHT+1)*self.scaling,arcade.color.WHITE,self.FONT_SIZE*self.scaling)
        dots = arcade.draw_text(f':',hour.right,self.top()-(self.TOP_BACKGROUN_HEIGHT+1)*self.scaling,arcade.color.WHITE,self.FONT_SIZE*self.scaling)
        minute = arcade.draw_text(f'{minutes}',dots.right,self.top()-(self.TOP_BACKGROUN_HEIGHT+1)*self.scaling,arcade.color.WHITE,self.FONT_SIZE*self.scaling)

    def draw_static(self):
        self.draw_background()
