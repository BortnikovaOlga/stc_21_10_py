import datetime

from flask import Flask, jsonify, request, abort
from sqlalchemy import func
from datetime import datetime
from models import Driver, Client, Order
from session_scope import *
from status import *

bad_request_str = "Неправильный запрос"
not_found_str = "Объект в базе не найден"
resource_already_exists = "Ресурс уже существует"

app = Flask("__name__")


@app.errorhandler(400)
def bed_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/drivers", methods=["POST"])
def post_driver():
    content = request.get_json()
    try:
        with session_scope() as session:
            # в описании к базе нет требования на уникальность имени, здесь реализовано через поиск и проверку
            if session.query(Driver).filter(Driver.name == content["name"]).first() is None:
                driver = Driver(name=content["name"], car=content["car"])
                session.add(driver)
                driver = session.query(Driver).filter(Driver.name == content["name"]).first()
                return driver.__repr__(), 201
    except:
        abort(400, description=bad_request_str)
    else:
        abort(400, description=resource_already_exists)


@app.route("/drivers/<int:driver_id>", methods=["GET"])
def get_driver_by_id(driver_id):
    with session_scope() as session:
        driver = session.query(Driver).filter(Driver.id == driver_id).first()
        if driver is not None:
            return driver.__repr__(), 200
        else:
            abort(404, description=not_found_str)


@app.route("/drivers/<path:driver_name>", methods=["GET"])
def get_driver_by_name(driver_name):
    with session_scope() as session:
        driver = session.query(Driver).filter(Driver.name == driver_name).first()
        if driver is not None:
            return driver.__repr__(), 200
        else:
            abort(404, description=not_found_str)


@app.route("/drivers", methods=["GET"])
def get_all_drivers():
    with session_scope() as session:
        drivers = session.query(Driver).all()
        if len(drivers) > 0:
            return drivers.__repr__(), 200
        else:
            abort(404, description=not_found_str)


@app.route("/drivers/<int:driver_id>", methods=["DELETE"])
def delete_driver_by_id(driver_id):
    try:
        with session_scope() as session:
            driver = session.query(Driver).filter(Driver.id == driver_id).first()
            if driver is not None:
                driver_response = driver.__repr__()
                session.query(Driver).filter(Driver.id == driver_id).delete()
                return driver_response, 204
    except:
        abort(400, description=bad_request_str)
    else:
        abort(404, description=not_found_str)


@app.route("/clients", methods=["POST"])
def post_client():
    content = request.get_json()
    try:
        with session_scope() as session:
            if session.query(Client).filter(Client.name == content["name"]).first() is None:
                client = Client(name=content["name"],
                                is_vip=True if content["is_vip"].strip().upper() == "TRUE" else False)
                session.add(client)
                client = session.query(Client).filter(Client.name == content["name"]).first()
                return client.__repr__(), 201
    except:
        abort(400, description=bad_request_str)
    else:
        abort(400, description=resource_already_exists)


@app.route("/clients/<int:client_id>", methods=["GET"])
def get_client_by_id(client_id):
    with session_scope() as session:
        client = session.query(Client).filter(Client.id == client_id).first()
        if client is None:
            abort(404, description=not_found_str)
        return client.__repr__(), 200


@app.route("/clients/<path:client_name>", methods=["GET"])
def get_client_by_name(client_name):
    with session_scope() as session:
        client = session.query(Client).filter(Client.name == client_name).first()
        if client is None:
            abort(404, description=not_found_str)
        return client.__repr__(), 200


@app.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client_by_id(client_id):
    try:
        with session_scope() as session:
            client = session.query(Client).filter(Client.id == client_id).first()
            if client is not None:
                client_response = client.__repr__()
                session.query(Client).filter(Client.id == client_id).delete()
                return client_response, 204
    except:
        abort(400, description=bad_request_str)
    else:
        abort(404, description=not_found_str)


@app.route("/orders", methods=["POST"])
def post_order():
    content = request.get_json()
    try:
        with session_scope() as session:
            _date_created = content["date_created"] if "date_created" in content.keys() else func.now()
            _status = content["status"] if "status" in content.keys() else Status.not_accepted.value
            order = Order(address_from=content["address_from"],
                          address_to=content["address_to"],
                          driver_id=content["driver_id"],
                          client_id=content["client_id"],
                          status=_status,
                          date_created=_date_created)
            session.add(order)
            # order = session.query(Order).filter(???).first()
            return {}, 201
    except:
        abort(400, description=bad_request_str)


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    with session_scope() as session:
        order = session.query(Order).filter(Order.id == order_id).first()
        if order is None:
            abort(404, description=not_found_str)
        return order.__repr__(), 200


@app.route("/orders", methods=["GET"])
def get_all_orders():
    with session_scope() as session:
        orders_list = session.query(Order).all()
        if len(orders_list) > 0:
            return orders_list.__repr__(), 200
        else:
            abort(404, description=not_found_str)


@app.route("/orders/<int:order_id>", methods=["PUT"])
def put_order(order_id):
    content = request.get_json()
    try:
        with session_scope() as session:
            order = session.query(Order).filter(Order.id == order_id).first()
            if order is not None:
                # проверить старый статус
                # если not_accepted , то можно менять дату создания , id водителя и  id клиента
                #
                order = Order(address_from=content["address_from"],
                              address_to=content["address_to"],
                              driver_id=content["driver_id"],
                              client_id=content["client_id"],
                              status=content["status"])
                order = session.query(Order).filter(Order.id == order_id).update()
    except:
        abort(400, description=bad_request_str)
    else:
        abort(404, description=not_found_str)
    return order.__repr__(), 201


if __name__ == "__main__":
    app.run()
