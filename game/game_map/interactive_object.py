from typing import Optional, List, Dict

from game_map.impact import Impact  # type: ignore


class InteractiveObject:

    def __init__(self):

        self.location: Optional['InteractiveObject'] = None
        self._container: List['InteractiveObject'] = []
        self._resists: Dict[type, float] = {}

    class AddingObjectError(ValueError):

        def __init__(self, arg):
            self.args = (arg,)

    @property
    def container(self):

        return self._container.copy()

    def add_object(self, inter_object: 'InteractiveObject') -> None:

        self._container.append(inter_object)

    def remove_object(self, inter_object: 'InteractiveObject') -> None:

        self._container.remove(inter_object)

    def affect(self, inter_object: 'InteractiveObject') -> None:

        raise NotImplementedError

    def accept_impact(self, impact: 'Impact') -> 'Impact':

        for owned_object in self.container:

            if owned_object:
                owned_object.accept_impact(impact)

        return Impact

    def move(self, destination: 'InteractiveObject') -> None:

        if self.location:
            self.location.remove_object(self)
        destination.add_object(self)
        self.location = destination

    def pass_adventurer(self, adventurer: 'InteractiveObject') -> bool:

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
