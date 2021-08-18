from enum import Enum
from Item import Item, ItemType
from Entity import Entity, EntityType


class Knight(Entity):
    """Класс Рыцарь"""

    def __init__(self, knight_type: Entity = EntityType.SWORDSMAN, hp: int = 10,
                 fire: Item = Item(ItemType.SWORD, 10)):
        """Args: knight_class - тип рыцаря, item - первое оружие."""
        super().__init__(knight_type, hp, fire)

        self.items = dict()  # весь набор предметов которыми владеет рыцарь ,
        self.append_item(fire)

    def append_item(self, item: Item):
        self.items[item.type] = item.power

    def __repr__(self):
        return " ".join((self.type.value, str(self.hp), str(self.items)))
