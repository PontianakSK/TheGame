from typing import Any


class Damage:

    def __init__(self, amount: float):

        self.amount = amount

    def deal_damage(self, target: Any) -> None:

        raise NotImplementedError
