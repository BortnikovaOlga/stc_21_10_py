from enum import Enum


class ItemType(Enum):
    SWORD = "МЕЧ"
    BOW = "ЛУК"
    BOOK = "КНИГА"
    APPLE = "ЯБЛОКО"
    TOTEM = "ТОТЕМ"
    ATTACK = "БОЙ"


class Item:

    def __init__(self, item_type: ItemType = ItemType.SWORD, power: int = 10):
        self.__type = item_type
        self.__power = power

    def __repr__(self):
        return " ".join((self.type.value, str(self.power)))

    def __hash__(self):
        return hash(self.__type.value)

    @property
    def power(self):
        return self.__power

    @property
    def type(self):
        return self.__type

    @power.setter
    def power(self, pw):
        # здесь проверки по типу рыцаря
        self.__power = pw

    def to_find_action(self):
        pass

    def to_take_action(self, arg):
        pass
