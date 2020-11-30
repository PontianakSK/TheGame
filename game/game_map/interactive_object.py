from typing import Optional, List, Dict

from game_map.damage import Damage  # type: ignore


class InteractiveObject:

    def __init__(self):

        self.health: int = 100
        self.location: Optional['InteractiveObject'] = None
        self._container: List['InteractiveObject'] = []
        self._resists: Dict[type, float] = {}

    class AddingObjectError(ValueError):

        def __init__(self, arg):
            self.args = (arg,)

    @property
    def container(self):

        return self._container.copy()

    def add_object(self, inter_object: 'InteractiveObject'):

        self._container.append(inter_object)

    def deal_damage(self, inter_object: 'InteractiveObject') -> None:

        raise NotImplementedError

    def accept_damage(self, damage: 'Damage') -> None:

        for owned_object in self.container:
            owned_object.accept_damage(damage)

    def move(destination: 'InteractiveObject') -> None:

        raise NotImplementedError

    def pass_adventurer(adventurer: 'InteractiveObject') -> bool:

        return True

    def __repr__(
                 self,
                 indent: int = 0,
                 max_depth: int = 3, *,
                 info: list = []
                 ) -> str:

        sep = '\n'+'\t'*indent

        if max_depth <= 0:
            return '[...]'

        self_data = f'{__name__}.{self.__class__.__name__}({id(self)}){{'
        result = ['']
        result.append(self_data)

        for line in info:
            result.append('\t'+str(line))
        result.append('\tcontains:')

        for inter_object in self.container:

            if inter_object is None:
                result.append(str(inter_object))
            else:
                result.append(inter_object.__repr__(indent+2, max_depth-1))

        string_repr = sep.join(result)+f'{sep}}}'

        return string_repr
