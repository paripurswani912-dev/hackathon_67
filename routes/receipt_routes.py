from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models.receipt import Receipt
from models.product import Product

receipt_bp = Blueprint("receipts", __name__)

@receipt_bp.route("/receipts", methods=["GET"])
def list_receipts():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    receipts = Receipt.query.order_by(Receipt.id.desc()).all()
    products = Product.query.all()

    receipt_list = []
    for r in receipts:
        product = Product.query.get(r.product_id)
        receipt_list.append({
            "id": r.id,
            "reference": f"REC-{r.id:04d}",
            "supplier": r.supplier,
            "product": product.name if product else "Unknown",
            "qty": f"{r.quantity}",
            "warehouse": "Main Warehouse",
            "date": "Recent",
            "status": "Done"
        })

    return render_template("receipts.html",
        active_page="receipts",
        page_title="Receipts",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        receipts=receipt_list,
        products=products
    )

@receipt_bp.route("/receipts/new", methods=["POST"])
def create_receipt():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    supplier = request.form.get("supplier")
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("qty") or 0)
    action = request.form.get("action")

    receipt = Receipt(
        supplier=supplier,
        product_id=product_id,
        quantity=quantity
    )
    db.session.add(receipt)
    db.session.commit()

    if action == "validate":
        product = Product.query.get(product_id)
        if product:
            product.stock += quantity
            db.session.commit()
            flash(f"Receipt validated. Stock +{quantity} for {product.name}.", "success")
        else:
            flash("Product not found.", "error")
    else:
        flash("Receipt saved as draft.", "success")

    return redirect(url_for("receipts.list_receipts"))