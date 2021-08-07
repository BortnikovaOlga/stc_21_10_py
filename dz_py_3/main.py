import json
import sys
import jsonschema
import sqlite3
from sqlite3 import Connection


def goods_validate(goods_list: dict, goods_schema_name: str) -> bool:
    """Выполняет валидацию данных из буфера goods_list в соотв со схемой goods_schema. Возврещ True в случае успеха."""
    with open(goods_schema_name, "r") as gs:
        goods_schema = json.load(gs)  # загружаем схему
    try:
        if isinstance(goods_list, dict):
            jsonschema.validate(goods_list, goods_schema)  # единственный товар
        else:
            for product in goods_list:  # если в буфере список товаров
                jsonschema.validate(product, goods_schema)
    except Exception:
        return False
    return True


def product_append(product: dict, conn: Connection) -> None:
    """Добавляет или обновляет данные в таблицах по одному товару product."""
    cur = conn.cursor()
    # добавление/обновление товара в таблицу goods
    _id = product["id"]
    _name = product["name"]
    _package_height = product["package_params"]["height"]
    _package_width = product["package_params"]["width"]
    # проверка наличия данных по id товара
    cur.execute("SELECT * from goods WHERE id = " + str(_id))
    if cur.fetchone() is None:  # если нет, то вставляем
        str_exe = """INSERT INTO goods VALUES(?, ?, ?, ?);"""
        _product = (_id, _name, _package_height, _package_width)
    else:  # если есть, то обновляем
        _product = (_name, _package_height, _package_width, _id)
        str_exe = """UPDATE goods SET name = ? , package_height = ?, package_width = ? WHERE id = ? ;"""
    cur.execute(str_exe, _product)
    conn.commit()

    # добавление/обновление locations для товара в таблице shops_goods
    for _id_shop in range(0, len(product["location_and_quantity"])):
        _location = product["location_and_quantity"][_id_shop]["location"]
        _amount = product["location_and_quantity"][_id_shop]["amount"]
        # нет сведенеий по id локаций ! в БД нужна отдельная таблица для справочника локаций !
        # проверка наличия данных по названию локации и ид товара в таблице shops_goods
        cur.execute(
            "SELECT * from shops_goods WHERE id_good = ? and location = ? ;",
            (_id, _location),
        )
        if cur.fetchone() is None:
            str_exe = """INSERT INTO shops_goods VALUES(?, ?, ?, ?);"""
            cur.execute(str_exe, (None, _id, _location, _amount))
        else:
            str_exe = """UPDATE shops_goods SET amount = ? WHERE location = ? ;"""
            cur.execute(str_exe, (_amount, _location))
        conn.commit()


def goods_append(goods_list: dict, conn: Connection) -> None:
    """Добавляет данные по товарам из буфера goods_list в таблицы БД с открытым соединением conn."""
    if isinstance(goods_list, dict):
        product_append(goods_list, conn)
    else:
        for product in goods_list:
            product_append(product, conn)


def create_table(conn: Connection) -> None:
    """Создает таблицы в БД, если они не существуют."""
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS goods(
       id INT PRIMARY KEY,
       name TEXT,
       package_height REAL,
       package_width REAL
       );"""
    )
    conn.commit()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS shops_goods(
       id INT,
       id_good INT,
       location TEXT,
       amount INT
       );"""
    )
    conn.commit()


def import_from_json_to_database(
    json_file: str, schema_name: str, db_name: str
) -> bool:
    """Выполняет импорт данных по товарам."""
    # загружаем данные из json файла в буфер
    with open(json_file, "r") as gf:
        goods_dict = json.load(gf)
    # валидация загруженных данных по заданной схеме
    if not goods_validate(goods_dict, schema_name):
        print("ошибка валидации")
        return False
    # открываем соединение с бд
    conn = sqlite3.connect(db_name)
    # создаем таблицы
    create_table(conn)
    # перемещение данных из буфера в таблицы бд
    goods_append(goods_dict, conn)
    # печать конечного состояния таблиц, это можно убрать
    cur = conn.cursor()
    cur.execute("SELECT * FROM goods;")
    all_results = cur.fetchall()
    print(all_results)
    cur.execute("SELECT * FROM shops_goods;")
    all_results = cur.fetchall()
    print(all_results)
    return True


if __name__ == "__main__":
    # загружаем данные из файла в буфер
    if not import_from_json_to_database("goods.json", "goods_schema.json", "goods_db"):
        sys.exit(-1)
