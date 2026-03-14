from flask import Blueprint, jsonify
from models.receipt import Receipt
from models.delivery import Delivery
from models.transfer import Transfer
from models.adjustment import Adjustment

move_history_bp = Blueprint("move_history", __name__)
@move_history_bp.route("/move-history", methods=["GET"])
def get_move_history():

    history = []

    # receipts
    receipts = Receipt.query.all()
    for r in receipts:
        history.append({
            "type": "receipt",
            "product_id": r.product_id,
            "quantity": r.quantity,
            "source": r.supplier
        })

    # deliveries
    deliveries = Delivery.query.all()
    for d in deliveries:
        history.append({
            "type": "delivery",
            "product_id": d.product_id,
            "quantity": -d.quantity,
            "source": d.customer
        })

    # transfers
    transfers = Transfer.query.all()
    for t in transfers:
        history.append({
            "type": "transfer",
            "product_id": t.product_id,
            "quantity": 0,
            "from": t.from_location,
            "to": t.to_location
        })

    # adjustments
    adjustments = Adjustment.query.all()
    for a in adjustments:
        history.append({
            "type": "adjustment",
            "product_id": a.product_id,
            "quantity_change": a.quantity_change,
            "reason": a.reason
        })

    return jsonify(history)