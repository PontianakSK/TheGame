class TileHeightGenerator:
    '''
    Abstract class defining generators of
    tile height interface.
    '''

    def get_height(self, y_perc: float, x_perc: float) -> float:
        raise NotImplementedError
