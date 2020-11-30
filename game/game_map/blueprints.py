
from typing import Optional, Generator

from game_map.interactive_object import InteractiveObject  # type: ignore

OptGen = Optional[Generator[InteractiveObject, None, None]]


class ObjectBlueprint:

    def get_objects(self, inter_object: InteractiveObject) -> OptGen:

        raise NotImplementedError
