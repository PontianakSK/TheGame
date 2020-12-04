from datetime import datetime
from datetime import timedelta

class GameTime:
    MIN_SPEED = 0
    #MAX_SPEED = 288
    MAX_SPEED = 40000
    
    def __init__(self):
        self.time = datetime(200,1,1,0,0,0)
        self.speed = 39000
        self.pause = True

    def __str__(self):
        paused = ''
        if self.pause:
            paused = 'PAUSE'
        return f'{self.get_time_string()} {paused}'

    def change_speed(self,delta: int):
        '''
        Adds delta to gamespeed. Delta can be negative.
        '''
        self.speed += delta
        list_ = [self.MIN_SPEED,self.MAX_SPEED,self.speed]
        list_.sort()
        self.speed = list_[1]

    def plus_speed(self):
        '''
        Increases speed by 36
        '''
        self.change_speed(36)

    def minus_speed(self):
        '''
        Decreases speed by 36
        '''
        self.change_speed(-36)

    def stop(self):
        '''
        Pauses the game
        '''
        self.pause = (not self.pause)

    def increase(self, seconds: int):
        '''
        Increases game time in accordance with speed
        '''
        if not self.pause:
            delta = timedelta(seconds=seconds*self.speed)
            self.time += delta

    def get_time_string(self) -> str:
        '''
        Returns current game time as string
        '''
        string_ = self.time.strftime('%d.%m.%Y %H:%M:%S')
        return string_

    def get_hour_s(self) -> str:
        '''
        Returns current hour as string
        '''
        return f'{self.time.hour:02d}'
    
    def get_minute_s(self) -> str:
        '''
        Returns current minute as string
        '''
        return f'{self.time.minute:02d}'

    def get_date(self) -> str:
        '''
        Returns current date as string
        '''
        return self.time.strftime('%d.%m.%Y')

    def weekday(self) -> str:
        '''
        Returns current weekday as string
        '''
        days = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday',
            }
        return days[self.time.weekday()]
