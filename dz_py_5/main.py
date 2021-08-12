# This is a sample Python script.
from abc import ABC, abstractmethod
from enum import Enum
from random import random


class ItemType(Enum):
    SWORD = "SWORD"
    BOW = "BOW"
    BOOK = "BOOK"
    APPLE = "APPLE"
    TOTEM = "TOTEM"
    ATTACK = "ATTACK"


class KnightClass(Enum):
    SWORDSMAN = "swordsman"
    ARCHER = "archer"
    MAG = "mag"


class Strategy(ABC):
    @abstractmethod
    def action(self):
        pass


class SwordStrategy(Strategy):
    def action(self):
        print("бой мечом")


class BowStrategy(Strategy):
    def action(self):
        print("стрельба из лука")


class MagikBookStrategy(Strategy):
    def action(self):
        print("Чтение заклинания")


class TotemStrategy(Strategy):
    def action(self):
        print("сохранить состояние игры")


class StrategyManager:
    strategy_dict = {ItemType.SWORD: SwordStrategy,
                     ItemType.BOW: BowStrategy,
                     ItemType.BOOK: MagikBookStrategy,
                     }

    @classmethod
    def get_strategy(cls, item: ItemType) -> Strategy:
        return cls.strategy_dict[item]


class ItemActions:
    def __init__(self):
        self._item_action_dict = {
            ItemType.SWORD: ItemActions.sword_action,
            ItemType.BOOK: ItemActions.book_action,
            ItemType.BOW: ItemActions.bow_action,
            ItemType.APPLE: ItemActions.apple_action,
            ItemType.TOTEM: ItemActions.totem_action}

    @staticmethod
    def sword_action():
        print("внутри меча")

    @staticmethod
    def book_action():
        ...

    @staticmethod
    def bow_action():
        ...

    @staticmethod
    def apple_action():
        ...

    @staticmethod
    def totem_action():
        ...

    def do_meet_action(self, item_type: ItemType):
        self._item_action_dict[item_type]()


class Item:

    def __init__(self, item_type: ItemType = ItemType.SWORD, power: int = 10):
        self.type = item_type
        self.power = power

    def __repr__(self):
        return " ".join((self.type.value, str(self.power)))


class Knight:
    """Класс Рыцарь"""

    def __init__(self, knight_class: KnightClass = KnightClass.SWORDSMAN, hp: int = 10,
                 fire: Item = Item(ItemType.SWORD, 10)):
        """Args: knight_class - класс рыцаря, item - первое оружие."""
        self.knight_class = knight_class
        self.hp = hp
        self.choice_fire_type = fire.type  # предмет выбранный для атаки или назначенный при создании/загрузке рыцаря
        self.items = []  # весь набор предметов которыми владеет рыцарь
        self.items.append(fire)

    @property
    def strategy(self) -> Strategy:
        """Стратегия ищется  в соответствии с выбранным оружием"""
        return StrategyManager.get_strategy(self.choice_fire_type)

    def set_fire_type(self, item: Item):
        self.choice_fire_type = item

    def __repr__(self):
        return " ".join((self.knight_class.value, str(self.hp), str(self.items), str(self.strategy)))


class Game:
    def __init__(self):
        self.finish = False
        self.hero = Knight()
        self.item_actions = ItemActions()
        # self.generator_items = GeneratorItems()

    @staticmethod
    def generate_item(self) -> Item:
        # случайный предмет
        item = Item(item_type=random.choice(list(ItemType), power=random.range(3, 15)))

        if item.type == ItemType.SWORD and self.hero.knight_class == KnightClass.SWORDSMAN:
            ...
        elif item.type == ItemType.BOW and self.hero.knight_class == KnightClass.ARCHER:
            ...
        elif item.type == ItemType.BOOK and self.hero.knight_class == KnightClass.MAG:
            ...
        return item

    def start(self):
        while not self.finish:
            item = Game.generate_item()
            self.item_actions.do_meet_action(item.type)
            #


if __name__ == '__main__':
    print(Knight())
    ItemActions().do_meet_action(ItemType.SWORD)
