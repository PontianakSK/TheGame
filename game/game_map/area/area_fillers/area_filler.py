from game_map.area.area import Area  # type: ignore


class AreaFiller:
    '''
    Abstract class defining interface for classes
    used to fill Are with interactive objects.
    '''

    def fill(self, area: Area) -> Area:

        raise NotImplementedError
