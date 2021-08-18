from Item import ItemType, Item
from ItemManager import ItemManager
from GameItems import Sword, MagikBook, BowAndArrows, Apple, Totem, Attack
from Knight import Knight


class Game:
    def __init__(self):
        self.finish = False
        self.hero = Knight()
        self.item_manager = ItemManager()
        self.monster = None

    def battle(self):
        print("бой")

    def start(self):
        while not self.finish:
            it = self.item_manager.generate_item()
            if it.type == ItemType.ATTACK:
                self.battle()
            elif it.type in (ItemType.SWORD, ItemType.BOOK, ItemType.BOW):
                if it.to_find_action():
                    it.to_take_action(self.hero)
            elif it.type == ItemType.APPLE:
                it.to_find_action()
            elif it.type == ItemType.TOTEM:
                pass


if __name__ == '__main__':
    knt = Knight()
    it = Sword(20)
    it.to_find_action()
    it.to_take_action(knt)
    print(knt.items)
