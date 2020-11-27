
from typing import Optional, Generator

from game_map.interactive_object import InteractiveObject #type: ignore

class ObjectBlueprint:
    
    def get_objects(self, inter_object: InteractiveObject)->Optional[Generator[InteractiveObject, None, None]]:

        raise NotImplementedError