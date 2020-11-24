from typing import Optional, Literal
class TileLayer:


    @staticmethod
    def bind_layers(upper_layer: Optional['TileLayer'], lower_layer: Optional['TileLayer'])->None:
        if lower_layer:
            lower_layer.upper_layer = upper_layer
        if upper_layer:
            upper_layer.lower_layer = lower_layer


    def __init__(self, upper_layer=None, lower_layer=None):
        self.bind_layers(upper_layer,self)
        self.bind_layers(self,lower_layer)
        self.lower_layer = lower_layer
        self._is_passable = True
        self._fertility = 1
        self.container = []


    @property
    def upper_layer(self)->Optional['TileLayer']:

        return self._upper_layer


    @upper_layer.setter
    def upper_layer(self, tile_layer: Optional['TileLayer'])->None:

        self._upper_layer = tile_layer


    @property
    def lower_layer(self)->Optional['TileLayer']:

        return self._lower_layer


    @lower_layer.setter
    def lower_layer(self, tile_layer: Optional['TileLayer'])->None:

        self._lower_layer = tile_layer


    @property
    def is_passable(self)->bool:

        return self._is_passable


    @property
    def fertility(self)->float:

        return self._fertility
    

    def __repr__(self, indent:int=1, direction:Literal[-1,0,1]=0)->str:

        sep = '\n'+'\t'*indent
        end = '\n'+'\t'*(indent-1)
        result = [f'{__name__}.{self.__class__.__name__}({id(self)}){{',]
        result.append(f'{self.fertility=},{sep}{self.is_passable=},{sep}{self.container=}}}')

        if direction in [0,1]:

            if self.upper_layer:
                result.append(f'self.upper_layer={self.upper_layer.__repr__(indent+1,1)}')
            else:
                result.append(f'{self.upper_layer=}')

        if direction in [-1,0]:

            if self.lower_layer:
                result.append(f'self.lower_layer={self.lower_layer.__repr__(indent+1,-1)}')
            else:
                result.append(f'{self.lower_layer=}')

        return sep.join(result)+end
        


if __name__ == '__main__':
   top_layer = TileLayer()
   top_layer.upper_layer = TileLayer()
   top_layer.upper_layer._is_passable = False
   top_layer.container.append('fish')
   print(top_layer)

