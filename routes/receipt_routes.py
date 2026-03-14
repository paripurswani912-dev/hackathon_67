from flask import Blueprint, request, jsonify
from database import db
from models.receipt import Receipt
from models.product import Product

receipt_bp = Blueprint("receipts", __name__)
@receipt_bp.route("/receipts", methods=["POST"])
def create_receipt():

    data = request.get_json()

    receipt = Receipt(
        supplier=data.get("supplier"),
        product_id=data.get("product_id"),
        quantity=data.get("quantity")
    )

    db.session.add(receipt)
    db.session.commit()

    return jsonify({
        "message": "Receipt created",
        "receipt_id": receipt.id
    })
@receipt_bp.route("/receipts/<int:id>/validate", methods=["POST"])
def validate_receipt(id):

    receipt = Receipt.query.get(id)

    if not receipt:
        return jsonify({"message": "Receipt not found"}), 404

    product = Product.query.get(receipt.product_id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    product.stock += receipt.quantity

    db.session.commit()

    return jsonify({
        "message": "Receipt validated",
        "product": product.name,
        "new_stock": product.stock
    })    