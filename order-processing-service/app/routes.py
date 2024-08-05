from flask import request, jsonify
from app import app, db
from app.models import Order
from flask_jwt_extended import jwt_required, get_jwt_identity


import warnings
from sqlalchemy.exc import SAWarning

warnings.filterwarnings("ignore", category=SAWarning)


@app.route("/orders", methods=["GET", "POST"])
@jwt_required()
def manage_orders():
    user_id = get_jwt_identity()

    if request.method == "GET":
        orders = Order.query.filter_by(user_id=user_id).all()
        return (
            jsonify(
                [
                    {
                        "id": o.id,
                        "user_id": o.user_id,
                        "product_id": o.product_id,
                        "quantity": o.quantity,
                        "status": o.status,
                        "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for o in orders
                ]
            ),
            200,
        )

    if request.method == "POST":
        data = request.get_json()
        order = Order(
            user_id=user_id, product_id=data["product_id"], quantity=data["quantity"]
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({"message": "Order created successfully"}), 201


@app.route("/orders/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def handle_order(id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=id, user_id=user_id).first()

    if not order:
        return jsonify({"message": "Order not found"}), 404

    if request.method == "GET":
        return (
            jsonify(
                {
                    "id": order.id,
                    "user_id": order.user_id,
                    "product_id": order.product_id,
                    "quantity": order.quantity,
                    "status": order.status,
                    "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            ),
            200,
        )

    if request.method == "PUT":
        data = request.get_json()
        order.status = data["status"]
        db.session.commit()
        return jsonify({"message": "Order updated successfully"}), 200

    if request.method == "DELETE":
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 204
