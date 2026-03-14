from flask import Blueprint, request, jsonify
from database import db
from models.transfer import Transfer
from models.product import Product

transfer_bp = Blueprint("transfers", __name__)
@transfer_bp.route("/transfers", methods=["POST"])
def create_transfer():

    data = request.get_json()

    product = Product.query.get(data.get("product_id"))

    if not product:
        return jsonify({"message": "Product not found"}), 404

    quantity = data.get("quantity")

    if product.stock < quantity:
        return jsonify({"message": "Not enough stock"}), 400

    transfer = Transfer(
        product_id=data.get("product_id"),
        from_location=data.get("from_location"),
        to_location=data.get("to_location"),
        quantity=quantity
    )

    db.session.add(transfer)
    db.session.commit()

    return jsonify({
        "message": "Transfer created",
        "transfer_id": transfer.id
    })
@transfer_bp.route("/transfers", methods=["GET"])
def list_transfers():

    transfers = Transfer.query.all()

    result = []

    for t in transfers:
        result.append({
            "id": t.id,
            "product_id": t.product_id,
            "from": t.from_location,
            "to": t.to_location,
            "quantity": t.quantity
        })

    return jsonify(result)    