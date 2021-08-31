from enum import Enum


class Status(Enum):
    """Перечисление допустимых статусов заказов."""

    not_accepted = "not_accepted"
    in_progress = "in_progress"
    cancelled = "cancelled"
    done = "done"


class TransStatus:
    """Хранит таблицу переходов между статусами и предоставляет метод для проверки валидности переходов.
    blblack
    Последовательности смены статусов заказа допускаются только такие:
    1) not_accepted → in_progress → done
    2) not_accepted → in_progress → cancelled
    3) not_accepted → cancelled
    """

    transitions = {
        Status.not_accepted: (
            Status.not_accepted.value,
            Status.in_progress.value,
            Status.cancelled.value,
        ),
        Status.in_progress: (Status.cancelled.value, Status.done.value),
    }

    @classmethod
    def is_valid(cls, status_old, status_new: str) -> bool:
        """Метод для проверки валидности перехода между статусами от status_old в статус status_new."""
        return status_new in cls.transitions[status_old]
