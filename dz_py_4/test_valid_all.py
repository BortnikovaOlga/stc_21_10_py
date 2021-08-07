import unittest
import json
from JSON_func_test import json_input_validation, json_result_validation, json_default_behavior
from main import InputParameterVerificationError, ResultVerificationError, FailRepeatTymeIsZerro, valid_all_decorator


class ValidAllTestCase(unittest.TestCase):
    _input_strs = {
        "test_json_positive": '{"city": "Innopolis", "temperature":19, "taken_at" : "day"}',
        "test_json_input_validation_exception": '{"temperature":19, "taken_at" : "day"}',
        "test_json_result_validation_exception": '{"city": "Barnaul", "temperature":19, "taken_at" : "night"}',
        "test_on_fail_repeat_time_is_zero": '{"city": "Barnaul", "temperature":19, "taken_at" : "day"}',
        "test_json_default_behavior": '{"city": "Barnaul", "temperature":19, "taken_at" : "evening"}'
    }
    _decorator_params = {
        "test_json_positive": (json_input_validation, json_result_validation, 1, None),
        "test_json_input_validation_exception": (json_input_validation, json_result_validation, 1, None),
        "test_json_result_validation_exception": (json_input_validation, json_result_validation, 1, None),
        "test_on_fail_repeat_time_is_zero": (json_input_validation, json_result_validation, 0, None),
        "test_json_default_behavior": (json_input_validation, json_result_validation, 3, json_default_behavior)

    }

    def setUp(self) -> None:
        self._input_str = self._input_strs[self._testMethodName]

        _input_validation = self._decorator_params[self._testMethodName][0]
        _result_validation = self._decorator_params[self._testMethodName][1]
        _on_fail_repeat_time = self._decorator_params[self._testMethodName][2]
        _default_behavior = self._decorator_params[self._testMethodName][3]

        @valid_all_decorator(_input_validation, _result_validation, expected_result="Innopolis",
                             on_fail_repeat_time=_on_fail_repeat_time, default_behavior=_default_behavior)
        def json_function(*args, **kwargs):
            print(kwargs["weather_dict"])
            return kwargs["weather_dict"]

        self._func = json_function

    def test_json_positive(self):
        """Позитивный тест, валидная входная строка , результат соответствует ожиданиям"""
        result = self._func(weather_dict=json.loads(self._input_str))
        self.assertEqual(result["city"], "Innopolis")

    def test_json_input_validation_exception(self):
        """Проверка типа исключения от input_validation при неверном json."""
        try:
            self._func(weather_dict=json.loads(self._input_str))
        except Exception as ex:
            self.assertEqual(type(ex), InputParameterVerificationError)

    def test_json_result_validation_exception(self):
        """Проверка типа исключения от result_validation."""
        try:
            self._func(weather_dict=json.loads(self._input_str))
        except Exception as ex:
            self.assertEqual(type(ex), ResultVerificationError)

    def test_on_fail_repeat_time_is_zero(self):
        """Проверка типа исключения от ."""
        try:
            self._func(weather_dict=json.loads(self._input_str))
        except Exception as ex:
            self.assertEqual(type(ex), FailRepeatTymeIsZerro)

    def test_json_default_behavior(self):
        """Проверка default_behavior."""
        result = self._func(weather_dict=json.loads(self._input_str))
        print(result)
        self.assertEqual(result["city"], "Kazan")


if __name__ == "__main__":
    unittest.main()
