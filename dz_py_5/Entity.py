from enum import Enum
from Item import Item, ItemType


class EntityType(Enum):
    SWORDSMAN = "swordsman"
    ARCHER = "archer"
    MAG = "mag"


class Entity:
    def __init__(self, entity_type: EntityType = EntityType.SWORDSMAN, hp: int = 10,
                 fire: Item = Item(ItemType.SWORD, 10)):
        self.__type = entity_type
        self.__hp = hp
        self.__fire_item = fire

    @property
    def type(self):
        return self.__type

    @property
    def hp(self):
        return self.__hp

    @property
    def fire_item(self):
        return self.__fire_item

    @fire_item.setter
    def fire_item(self, fire: Item):
        if isinstance(fire == Item) and fire.type in (ItemType.SWORD, ItemType.BOW, ItemType.BOOK):
            self.__fire_item = fire

    def reduce_hp(self, dhp: int):
        self.__hp -= dhp
