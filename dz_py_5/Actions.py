class Actions:

    @staticmethod
    def read_choice(message: str) -> bool:
        """Печать вопроса и чтение на него ответа, возвращает True в случае согласия, False в противном случае."""
        i = ""
        while not (i == "1" or i == "2"):
            print(message)
            i = input("Ввести 1 - если ДА, 2 - если НЕТ : ").strip()
        return i == "1"
