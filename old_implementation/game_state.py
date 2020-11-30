import map_sprites
import game_time
import game_view

class GameState:

    def __init__(self):
        self.map = None
        self.time = None
        self.view_frame = None

    def create_new_game(self, seed: str, size: int):
        '''
        Creates new game state from seed with map of corresponding size.
        '''
        self.map = map_sprites.SpriteMap(seed,size)
        self.map.new_map()
        self.time = game_time.GameTime()
        self.view_frame = game_view.MapView()
        self.view_frame.new_view(0,0)

    def new_year(self):
        print('New year')
    def new_month(self):
        print('New month')
    def new_day(self):
        #print('New day')
        self.map.forest.grow()
        self.map.forest.seed()
    def new_hour(self):
        #print('New hour')
        pass
    def new_minute(self):
        #print('New minute')
        pass

    def increase_time(self, seconds:int):
        '''
        Increases time and trigger corresponding events
        '''
        year = self.time.time.year
        month = self.time.time.month
        day = self.time.time.day
        hour = self.time.time.hour
        minute = self.time.time.minute
        self.time.increase(seconds)
        if self.time.time.year - year != 0:
            self.new_year()
            self.new_month()
            self.new_day()
            self.new_hour()
            self.new_minute()
        elif self.time.time.month - month != 0:
            self.new_month()
            self.new_day()
            self.new_hour()
            self.new_minute()
        elif self.time.time.day - day != 0:
            self.new_day()
            self.new_hour()
            self.new_minute()
        elif self.time.time.hour - hour != 0:
            self.new_hour()
            self.new_minute()
        elif self.time.time.minute - minute != 0:
            self.new_minute()

    def draw(self):
        self.map.draw_map()
        self.view_frame.draw()
        self.view_frame.interface.draw_time(self.time.get_date(),self.time.get_hour_s(),self.time.get_minute_s())