import random
from Item import ItemType, Item
from GameItems import Sword, MagikBook, BowAndArrows, Apple, Totem, Attack


class ItemManager:
    item_dict = {
        ItemType.SWORD: Sword,
        ItemType.BOOK: MagikBook,
        ItemType.BOW: BowAndArrows,
        ItemType.APPLE: Apple,
        ItemType.TOTEM: Totem,
        ItemType.ATTACK: Attack}

    @classmethod
    def item_class(cls, item_type: ItemType):
        return cls.item_dict[item_type]

    @classmethod
    def generate_item(cls) -> Item:
        # случайный предмет
        # power = random.randint(3, 15)
        item = cls.item_class(random.choice(list(ItemType)))

        """if item.type == ItemType.SWORD and hero.knight_class == KnightClass.SWORDSMAN:
            ...
        elif item.type == ItemType.BOW and hero.knight_class == KnightClass.ARCHER:
            ...
        elif item.type == ItemType.BOOK and hero.knight_class == KnightClass.MAG:
            ..."""
        return item()
