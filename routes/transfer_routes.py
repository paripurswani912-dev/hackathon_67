from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models.transfer import Transfer
from models.product import Product

transfer_bp = Blueprint("transfers", __name__)

@transfer_bp.route("/transfers", methods=["GET"])
def list_transfers():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    transfers = Transfer.query.order_by(Transfer.id.desc()).all()
    products = Product.query.all()

    transfer_list = []
    for t in transfers:
        product = Product.query.get(t.product_id)
        transfer_list.append({
            "id": t.id,
            "reference": f"TRF-{t.id:04d}",
            "product": product.name if product else "Unknown",
            "qty": f"{t.quantity}",
            "from_location": t.from_location,
            "to_location": t.to_location,
            "date": "Recent",
            "status": "Done"
        })

    return render_template("transfers.html",
        active_page="transfers",
        page_title="Internal Transfers",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        transfers=transfer_list,
        products=products
    )

@transfer_bp.route("/transfers/new", methods=["POST"])
def create_transfer():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    product_id = request.form.get("product_id")
    quantity = int(request.form.get("qty") or 0)
    from_location = request.form.get("from_location")
    to_location = request.form.get("to_location")
    action = request.form.get("action")

    product = Product.query.get(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("transfers.list_transfers"))

    if product.stock < quantity:
        flash(f"Not enough stock. Only {product.stock} available.", "error")
        return redirect(url_for("transfers.list_transfers"))

    transfer = Transfer(
        product_id=product_id,
        from_location=from_location,
        to_location=to_location,
        quantity=quantity
    )
    db.session.add(transfer)
    db.session.commit()

    if action == "validate":
        flash(f"Transfer validated. {quantity} units moved from {from_location} to {to_location}.", "success")
    else:
        flash("Transfer saved as draft.", "success")

    return redirect(url_for("transfers.list_transfers"))