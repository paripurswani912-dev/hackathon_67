from flask import Blueprint, render_template, session, redirect, url_for
from models.receipt import Receipt
from models.delivery import Delivery
from models.transfer import Transfer
from models.adjustment import Adjustment
from models.product import Product

move_history_bp = Blueprint("move_history", __name__)

@move_history_bp.route("/history", methods=["GET"])
def get_move_history():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    history = []

    for r in Receipt.query.order_by(Receipt.id.desc()).all():
        product = Product.query.get(r.product_id)
        history.append({
            "datetime": "Recent",
            "reference": f"REC-{r.id:04d}",
            "type": "Receipt",
            "product": product.name if product else "Unknown",
            "from_location": r.supplier,
            "to_location": "Main Warehouse",
            "qty_change": r.quantity,
            "user": "Admin"
        })

    for d in Delivery.query.order_by(Delivery.id.desc()).all():
        product = Product.query.get(d.product_id)
        history.append({
            "datetime": "Recent",
            "reference": f"DEL-{d.id:04d}",
            "type": "Delivery",
            "product": product.name if product else "Unknown",
            "from_location": "Main Warehouse",
            "to_location": d.customer,
            "qty_change": -d.quantity,
            "user": "Admin"
        })

    for t in Transfer.query.order_by(Transfer.id.desc()).all():
        product = Product.query.get(t.product_id)
        history.append({
            "datetime": "Recent",
            "reference": f"TRF-{t.id:04d}",
            "type": "Transfer",
            "product": product.name if product else "Unknown",
            "from_location": t.from_location,
            "to_location": t.to_location,
            "qty_change": 0,
            "user": "Admin"
        })

    for a in Adjustment.query.order_by(Adjustment.id.desc()).all():
        product = Product.query.get(a.product_id)
        history.append({
            "datetime": "Recent",
            "reference": f"ADJ-{a.id:04d}",
            "type": "Adjustment",
            "product": product.name if product else "Unknown",
            "from_location": None,
            "to_location": None,
            "qty_change": a.quantity_change,
            "user": "Admin"
        })

    return render_template("history.html",
        active_page="history",
        page_title="Move History",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        history=history,
        receipt_count=Receipt.query.count(),
        delivery_count=Delivery.query.count(),
        transfer_count=Transfer.query.count(),
        adjustment_count=Adjustment.query.count()
    )