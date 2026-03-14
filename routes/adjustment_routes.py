from flask import Blueprint, request, jsonify
from database import db
from models.adjustment import Adjustment
from models.product import Product

adjustment_bp = Blueprint("adjustments", __name__)
@adjustment_bp.route("/adjustments", methods=["POST"])
def create_adjustment():

    data = request.get_json()

    product = Product.query.get(data.get("product_id"))

    if not product:
        return jsonify({"message": "Product not found"}), 404

    counted_quantity = data.get("counted_quantity")

    difference = counted_quantity - product.stock

    # update stock
    product.stock = counted_quantity

    adjustment = Adjustment(
        product_id=product.id,
        reason=data.get("reason"),
        quantity_change=difference
    )

    db.session.add(adjustment)
    db.session.commit()

    return jsonify({
        "message": "Stock adjusted",
        "product": product.name,
        "old_stock": product.stock - difference,
        "new_stock": product.stock,
        "change": difference
    })
@adjustment_bp.route("/adjustments", methods=["GET"])
def list_adjustments():

    adjustments = Adjustment.query.all()

    result = []

    for a in adjustments:
        result.append({
            "id": a.id,
            "product_id": a.product_id,
            "reason": a.reason,
            "quantity_change": a.quantity_change
        })

    return jsonify(result)    