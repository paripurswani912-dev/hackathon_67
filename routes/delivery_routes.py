from flask import Blueprint, request, jsonify
from database import db
from models.delivery import Delivery
from models.product import Product

delivery_bp = Blueprint("deliveries", __name__)
@delivery_bp.route("/deliveries", methods=["POST"])
def create_delivery():

    data = request.get_json()

    delivery = Delivery(
        customer=data.get("customer"),
        product_id=data.get("product_id"),
        quantity=data.get("quantity")
    )

    db.session.add(delivery)
    db.session.commit()

    return jsonify({
        "message": "Delivery created",
        "delivery_id": delivery.id
    })
@delivery_bp.route("/deliveries/<int:id>/validate", methods=["POST"])
def validate_delivery(id):

    delivery = Delivery.query.get(id)

    if not delivery:
        return jsonify({"message": "Delivery not found"}), 404

    product = Product.query.get(delivery.product_id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    # check stock
    if product.stock < delivery.quantity:
        return jsonify({"message": "Not enough stock"}), 400

    # reduce stock
    product.stock -= delivery.quantity

    db.session.commit()

    return jsonify({
        "message": "Delivery validated",
        "product": product.name,
        "remaining_stock": product.stock
    })   