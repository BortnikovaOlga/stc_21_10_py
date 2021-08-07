import sqlite3
import unittest
from main import (
    goods_validate,
    create_table,
    goods_append,
    import_from_json_to_database,
)
import sys
import os
from json_test_cases import (
    TEST_CASE_POSITIVE_ONE_PRODUCT,
    TEST_CASE_POSITIVE_N_PRODUCTS,
    TEST_CASE_NEGATIVE,
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class JsonImportGoodsTestCase(unittest.TestCase):
    def setUp(self):
        self.json_schema = "goods_schema.json"
        self.conn = sqlite3.connect("goods_db_test")
        create_table(self.conn)

    def test_goods_validate_positive(self):
        """Тестирование функци валидации данных по json схеме, позитивные проверки."""
        # проверка валидации одного продукта
        self.assertTrue(
            goods_validate(TEST_CASE_POSITIVE_ONE_PRODUCT, self.json_schema)
        )
        # проверка валидации списка
        self.assertTrue(goods_validate(TEST_CASE_POSITIVE_N_PRODUCTS, self.json_schema))

    def test_goods_validate_negative(self):
        """Тестирование функци валидации данных по json схеме, негативная проверка."""
        self.assertFalse(goods_validate(TEST_CASE_NEGATIVE, self.json_schema))

    def test_product_append(self):
        """Тестирование функции добавления товаров для случая одного продукта."""
        goods_append(TEST_CASE_POSITIVE_ONE_PRODUCT, self.conn)
        test_id_product = TEST_CASE_POSITIVE_ONE_PRODUCT["id"]
        # проверка, что продукт добавлен в БД
        cur = self.conn.cursor()
        cur.execute("SELECT * from goods WHERE id = " + str(test_id_product))
        self.assertEqual(cur.fetchone()[0], test_id_product)

    def test_goods_append(self):
        """Тестирование функции добавления товаров для случая списка из N товаров."""
        goods_append(TEST_CASE_POSITIVE_N_PRODUCTS, self.conn)
        test_id_product = TEST_CASE_POSITIVE_N_PRODUCTS[1]["id"]
        test_name_product = TEST_CASE_POSITIVE_N_PRODUCTS[1]["name"]
        # проверка, что повторное добавление товара не создает дублирующих записей в БД
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) from goods WHERE id = " + str(test_id_product))
        self.assertEqual(cur.fetchone()[0], 1)
        # проверка, что при повторном добавлении товара изменяется содержание полей
        cur.execute(
            "SELECT count(*) from goods WHERE id = ? and name = ?",
            (test_id_product, test_name_product),
        )
        self.assertEqual(cur.fetchone()[0], 1)

    def test_import_from_file(self):
        """Проверка главной функции с логикой импорта из файла в БД."""
        self.assertTrue(
            import_from_json_to_database("goods.json", "goods_schema.json", "test_db")
        )


if __name__ == "__main__":
    unittest.main()
