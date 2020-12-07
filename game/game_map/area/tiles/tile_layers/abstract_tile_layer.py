from typing import Optional

from game_map.interactive_object import InteractiveObject, Impact


class TileLayer(InteractiveObject):
    '''
    Each tile can consist of several tile layers
    like real soil. For instance rock under sand
    under water. The nasting of layers represents
    the depth
    '''

    def __init__(self, lower_layer: Optional['TileLayer'] = None):

        super().__init__()
        self.add_object(lower_layer)
        self._fertility = 1

    @staticmethod
    def is_tile_layer(inter_object: InteractiveObject) -> bool:
        '''
        Just checks if other object is TileLayer.
        Returns True if it is and False otherwise.
        '''

        result = isinstance(inter_object, TileLayer)

        return result

    def add_object(self, inter_object: InteractiveObject):
        '''
        Tile layer can contain any object but only one other
        tile layer. Next should be placed inside lower level.
        '''

        if TileLayer.is_tile_layer(inter_object):
            tiles_in_container = map(TileLayer.is_tile_layer, self.container)

            if any(tiles_in_container):
                error_message = 'Only one internal TileLayer is allowed'
                raise InteractiveObject.AddingObjectError(error_message)

        super().add_object(inter_object)

    def accept_impact(self, impact: Impact):
        '''
        Any Impact affect only objects on this
        tile layer.
        '''

        for owned_object in self.container:
            if not isinstance(owned_object, TileLayer):
                owned_object.accept_impact(Impact)

    @property
    def lower_layer(self) -> Optional['TileLayer']:
        '''
        If this tile layer contains other tile layer
        the second one is considered as lower.
        '''

        for inter_object in self.container:
            if isinstance(inter_object, TileLayer):
                return inter_object
        return None

    @lower_layer.setter
    def lower_layer(self, tile_layer: Optional['TileLayer']) -> None:

        self.add_object(tile_layer)

    @property
    def fertility(self) -> float:
        '''
        Fertility affects how fast plants grow.
        '''

        return self._fertility

    def __repr__(self, *args, **kwargs):
        info = [
            f'fertility: {self.fertility}'
        ]
        return super().__repr__(*args, **kwargs, info=info)


if __name__ == '__main__':
    top_layer = TileLayer()
    top_layer.upper_layer = TileLayer()
    top_layer.upper_layer._is_passable = False
    top_layer.container.append('fish')
    print(top_layer)
