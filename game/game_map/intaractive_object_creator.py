from game_map.interactive_object import InteractiveObject  # type: ignore
from game_map.blueprints import ObjectBlueprint  # type: ignore


class InteractiveObjectCreator:

    def __init__(self, blueprint: ObjectBlueprint):
        self.blueprint = blueprint

    def build(self, params: dict) -> InteractiveObject:
        raise NotImplementedError
