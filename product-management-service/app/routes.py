from flask import request, jsonify
from app import app, db
from app.models import Product

import warnings
from sqlalchemy.exc import SAWarning

warnings.filterwarnings("ignore", category=SAWarning)


@app.route("/products", methods=["GET", "POST"])
def manage_products():
    if request.method == "GET":
        products = Product.query.all()
        return (
            jsonify(
                [
                    {
                        "id": p.id,
                        "name": p.name,
                        "description": p.description,
                        "price": p.price,
                        "stock": p.stock,
                        "version": p.version,
                        "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for p in products
                ]
            ),
            200,
        )

    if request.method == "POST":
        data = request.get_json()

        # validation for every field data
        if (
            not data["name"]
            or not data["description"]
            or not data["price"]
            or not data["stock"]
        ):
            return jsonify({"message": "All fields are required"}), 400

        product = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"],
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"}), 201


@app.route("/products/<int:id>", methods=["GET", "PUT", "DELETE"])
def handle_product(id):
    product = Product.query.filter_by(id=id).first()

    if request.method == "GET":
        if product:
            return (
                jsonify(
                    {
                        "id": id,
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "stock": product.stock,
                        "version": product.version,
                        "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                ),
                200,
            )
        return jsonify({"message": "Product not found"}), 404

    if request.method == "PUT":
        data = request.get_json()

        # validation for every field data
        if (
            not data["name"]
            or not data["description"]
            or not data["price"]
            or not data["stock"]
        ):
            return jsonify({"message": "All fields are required"}), 400

        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.stock = data["stock"]
        product.version += 1
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200

    if request.method == "DELETE":
        if not product:
            return jsonify({"message": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 204
