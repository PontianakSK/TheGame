from typing import Any


class Impact:
    '''
    Visitor class used for performing
    game actions with Interactive Objects
    Composite.
    '''

    def affect(self, target: Any) -> None:

        raise NotImplementedError
