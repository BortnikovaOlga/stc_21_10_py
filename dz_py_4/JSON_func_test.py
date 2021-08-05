from schematics.models import Model
from schematics.types import StringType, DecimalType
from schematics.exceptions import ValidationError, DataError
from enum import Enum
from schematics.validate import validate
from main import valid_all_decorator


class TimeDay(Enum):
    """Пречисление допустимых строк для задания времени суток."""

    MORNING = "morning"
    DAY = "day"
    EVENING = "evening"
    NIGHT = "night"

    @classmethod
    def values(cls):
        """Возвращает лист из всех констант перечисления."""
        return [cls.DAY.value, cls.NIGHT.value, cls.EVENING.value, cls.MORNING.value]


class Weather(Model):
    """Модель для записи о погоде в городе."""

    city = StringType(required=True)
    temperature = DecimalType(required=True)
    taken_at = StringType(required=True, default=TimeDay.DAY.value)

    def validate_taken_at(self, data, value):
        """валидация поля под тип TimeDay."""
        if data["taken_at"] not in TimeDay.values():
            raise ValidationError("invalid value for time of day")
        return value


def json_input_validation(*args, **kwargs) -> bool:
    """Проверка входных параметров для json_function."""
    try:
        validate(Weather, kwargs["weather_dict"])
    except DataError:
        return False
    return True


def json_result_validation(result: dict) -> bool:
    """Проверка возвращаемого результата для json_function."""
    return result["city"] == "Innopolis"


def json_default_behavior():
    """Значение по умолчанию."""
    return "Kazan"


@valid_all_decorator(json_input_validation, json_result_validation)
def json_function(*args, **kwargs):
    """Функция для проверки декоратора."""
    print(kwargs["weather_dict"])
    return kwargs["weather_dict"]
