from typing import Optional, List, Dict

from game_map.impact import Impact  # type: ignore


class InteractiveObject:
    '''
    Every object in the game are Interactive objects,
    containing other object. Utilizes Composite pattern.
    '''

    def __init__(self):

        self.location: Optional['InteractiveObject'] = None
        self._container: List['InteractiveObject'] = []
        self._resists: Dict[type, float] = {}

    class AddingObjectError(ValueError):
        '''
        Exception class for cases when object can not
        be added to other object container. (Possibly
        due to the limitations on types that can be added
        to target)
        '''
        def __init__(self, arg):
            self.args = (arg,)

    @property
    def container(self) -> List['InteractiveObject']:
        '''
        Returns a copy of List with all objects this object
        contains.
        '''

        return self._container.copy()

    def add_object(self, inter_object: 'InteractiveObject') -> None:
        '''
        Adds target object to this object's container.
        '''

        self._container.append(inter_object)

    def remove_object(self, inter_object: 'InteractiveObject') -> None:
        '''
        Removes target object from this object's container.
        '''

        self._container.remove(inter_object)

    def affect(self, inter_object: 'InteractiveObject') -> None:
        '''
        Performs some actions with other object. Should be
        overridden in subclases.
        '''

        raise NotImplementedError

    def accept_impact(self, impact: 'Impact') -> 'Impact':
        '''
        Accepts Impact object. Utilizes Visitor pattern.
        There can be different Impact object with different
        behavior when being accepted. Should be overridden in
        subclasses.
        '''

        for owned_object in self.container:

            if owned_object:
                owned_object.accept_impact(impact)

        return Impact

    def move(self, destination: 'InteractiveObject') -> None:
        '''
        Moves this object to other objects container.
        '''

        if self.location:
            self.location.remove_object(self)
        destination.add_object(self)
        self.location = destination

    def pass_adventurer(self, adventurer: 'InteractiveObject') -> bool:
        '''
        Returns True or False in case other object can pass through this
        object or not, respectively. Common object always passes
        everybody. May be overridden in subclasses.
        '''

        return True

    def __repr__(
                 self,
                 indent: int = 0,
                 max_depth: int = 3, *,
                 info: list = []
                 ) -> str:

        '''
        Returns str for this objects and all objects
        it contains to the specified depth.
        Indent is used to show objects heirarchy.
        Info used for adding some info in subclasses.
        '''

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
