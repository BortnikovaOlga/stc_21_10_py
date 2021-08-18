from Item import ItemType, Item
from Knight import Knight
from Actions import Actions


class Sword(Item):

    def __init__(self, pw: int = 10):
        super().__init__(item_type=ItemType.SWORD, power=pw)

    def __hash__(self):
        return hash(self.type.value)

    def to_find_action(self) -> bool:
        return Actions.read_choice("найден " + str(self.type.value) + " Поднять его ?")

    def fight_step(self):
        print("бой " + str(self.type))

    def to_take_action(self, kn: Knight):
        kn.append_item(self)
        return False


class BowAndArrows(Item):

    def __init__(self, pw: int = 10):
        super().__init__(item_type=ItemType.BOW, power=pw)

    def __hash__(self):
        return hash(self.type.value)

    def to_find_action(self):
        return Actions.read_choice("найден " + str(self.type.value) + " Поднять его ?")

    def fight_step(self):
        print("стрельба" + str(self.type))

    def to_take_action(self, kn: Knight):
        kn.append_item(self)
        return False


class MagikBook(Item):

    def __init__(self, pw: int = 10):
        super().__init__(item_type=ItemType.BOOK, power=pw)

    def __hash__(self):
        return hash(self.type.value)

    def to_find_action(self):
        return Actions.read_choice("найдена " + str(self.type.value) + " Поднять его ?")

    def fight_step(self):
        print("бой" + str(self.type))

    def to_take_action(self, kn: Knight):
        kn.append_item(self)
        return False


class Attack(Item):

    def __init__(self, pw: int = 10):
        super().__init__(item_type=ItemType.ATTACK, power=pw)

    def to_find_action(self):
        # сгенерировать чудовище
        return Actions.read_choice("Встреча с чудовищем, принять " + str(self.type.value) + " ?")

    def to_take_action(self):
        pass


class Apple(Item):

    def __init__(self, life: int = 10):
        super().__init__(item_type=ItemType.APPLE, power=life)

    def to_find_action(self):
        # здесь улучшить здоровье
        ...

    def to_take_action(self):
        pass


class Totem(Item):

    def __init__(self):
        super().__init__(item_type=ItemType.TOTEM, power=0)

    def to_find_action(self):
        return Actions.read_choice("найден " + str(self.type.value) + " Сохранить игру сейчас ?")

    def to_take_action(self):
        pass
