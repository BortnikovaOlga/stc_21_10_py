import json
import sqlite3
import sys

import jsonschema


def goods_validate(goods_list, goods_schema: dict) -> bool:
    """Выполняет валидацию данных в буфере goods_list в соответствии со схемой goods_schema,
    возвращает True в случае успеха."""
    try:
        if isinstance(goods_list, dict):
            jsonschema.validate(goods_list, goods_schema)  # единственный товар
        else:
            for product in goods_list:  # если в буфере список товаров
                jsonschema.validate(product, goods_schema)
    except Exception as ex:
        print(ex)
        return False
    return True


def product_append(product: dict, cur) -> None:
    """Добавляет или обновляет данные в таблицах по одному товару product."""
    # добавление/обновление товара в таблицу goods
    _id = product['id']
    _name = product['name']
    _package_height = product['package_params']['height']
    _package_width = product['package_params']['width']
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
    for _id_shop in range(0, len(product['location_and_quantity'])):
        _location = product['location_and_quantity'][_id_shop]['location']
        _amount = product['location_and_quantity'][_id_shop]['amount']
        _id_shop = None  # нет сведенеий по id локаций ! в БД нужна отдельная таблица для справочника локаций !
        # проверка наличия данных по названию локации и ид товара в таблице shops_goods
        cur.execute("SELECT * from shops_goods WHERE id_good = ? and location = ? ;", (_id, _location))
        if cur.fetchone() is None:
            str_exe = """INSERT INTO shops_goods VALUES(?, ?, ?, ?);"""
            cur.execute(str_exe, (_id_shop, _id, _location, _amount))
        else:
            str_exe = """UPDATE shops_goods SET amount = ? WHERE location = ? ;"""
            cur.execute(str_exe, (_amount, _location))
        conn.commit()


def goods_append(goods_list, cur) -> None:
    """Добавляет данные из буфера goods_list в таблицы по курсору cur."""
    if isinstance(goods_list, dict):
        product_append(goods_list, cur)
    else:
        for product in goods_list:
            product_append(product, cur)


def create_table(cur) -> None:
    """Создает таблицы в бд, если они не существуют."""
    cur.execute("""CREATE TABLE IF NOT EXISTS goods(
       id INT PRIMARY KEY,
       name TEXT,
       package_height REAL,
       package_width REAL
       );""")
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS shops_goods(
       id INT,
       id_good INT,
       location TEXT,
       amount INT
       );""")
    conn.commit()


# загружаем схему
with open("goods_schema.json", "r") as gs:
    goods_schema = json.load(gs)

# загружаем данные из файла в буфер
with open("goods.json", "r") as gf:
    goods_dict = json.load(gf)

# валидация загруженных данных
if not goods_validate(goods_dict, goods_schema):
    print("ошибка валидации")
    sys.exit(-1)
print(goods_dict)

# открываем соединение с бд
conn = sqlite3.connect('goods_db')
cur = conn.cursor()
# создаем таблицы
create_table(cur)

# перемещение данных из буфера в таблицы бд
goods_append(goods_dict, cur)

# печать конечного состояния таблиц, это можно убрать
cur.execute("SELECT * FROM goods;")
all_results = cur.fetchall()
print(all_results)
cur.execute("SELECT * FROM shops_goods;")
all_results = cur.fetchall()
print(all_results)
