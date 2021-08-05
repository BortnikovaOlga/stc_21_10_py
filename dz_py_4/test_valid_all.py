import unittest
import json
from JSON_func_test import json_function
from main import InputParameterVerificationError, ResultVerificationError


class ValidAllTestCase(unittest.TestCase):
    def test_json_positive(self):
        json_str = '{"city": "Innopolis", "temperature":19, "taken_at" : "day"}'
        result = json_function(weather_dict=json.loads(json_str))
        self.assertEqual(result["city"], "Innopolis")

    def test_json_input_validation_exception(self):
        """Проверка типа исключения от input_validation при неверном json."""
        json_error_str = '{"temperature":19, "taken_at" : "day"}'
        try:
            json_function(weather_dict=json.loads(json_error_str))
        except Exception as ex:
            self.assertEqual(type(ex), InputParameterVerificationError)

    def test_json_result_validation_exception(self):
        """Проверка типа исключения от result_validation."""
        json_str = '{"city": "Barnaul", "temperature":19, "taken_at" : "day"}'
        try:
            json_function(weather_dict=json.loads(json_str))
        except Exception as ex:
            self.assertEqual(type(ex), ResultVerificationError)


if __name__ == "__main__":
    unittest.main()
