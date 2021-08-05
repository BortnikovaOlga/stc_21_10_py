from typing import Callable, Any


# on_fail_repeat_time - 0 выдать написанное самостоятельно исключение,
# TODO ! При отрицательном значении параметра функция,над котором стоит декоратор, выполнится до тех пор,
#  пока результат не пройдёт условия проверки, либо будет выполняться вечно !


class InputParameterVerificationError(Exception):
    """Исключение на ошибку во входных данных."""

    def __init__(self) -> None:
        """-."""
        super().__init__("Ошибка верификации входных данных ")


class ResultVerificationError(Exception):
    """Исключение на ошибку в результирующих данных."""

    def __init__(self) -> None:
        """-."""
        super().__init__("Ошибка верификации выходных данных ")


class FailRepeatTymeIsZerro(Exception):
    """on_fail_repeat_time - 0 выдать написанное самостоятельно исключение."""

    def __init__(self) -> None:
        """-."""
        super().__init__("on_fail_repeat_time should not be equal 0")


def valid_all_decorator(
        input_validation: Callable, result_validation: Callable,
        default_behavior: Callable = None, on_fail_repeat_time: int = 1, ) -> Callable:
    """Декоратор для валидации входных , результирующих значений."""

    def decoration(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            if not input_validation(*args, **kwargs):
                raise InputParameterVerificationError
            if on_fail_repeat_time == 0:
                raise FailRepeatTymeIsZerro
            for i in range(on_fail_repeat_time):
                result = func(*args, **kwargs)
                print(i)
                if result_validation(result):
                    return result

            if default_behavior:
                return default_behavior()
            else:
                raise ResultVerificationError

        return wrapper

    return decoration


if __name__ == "__main__":
    """def my_input_validation(*args):
        return args[0] == "INPUT"


    def my_result_validation(*args):
        return args[0] == "OK"


    def my_default_behavior():
        return "DEFAULT"


    @valid_all_decorator(my_input_validation, my_result_validation, my_default_behavior, 3)
    def my_function(parameter):
        print(parameter)
        return "OK_"


    # проверка работы декоратора
    print(my_function("INPUT"))"""
