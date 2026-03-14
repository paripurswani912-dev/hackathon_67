from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models.adjustment import Adjustment
from models.product import Product

adjustment_bp = Blueprint("adjustments", __name__)

@adjustment_bp.route("/adjustments", methods=["GET"])
def list_adjustments():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    adjustments = Adjustment.query.order_by(Adjustment.id.desc()).all()
    products = Product.query.all()

    adjustment_list = []
    for a in adjustments:
        product = Product.query.get(a.product_id)
        adjustment_list.append({
            "id": a.id,
            "reference": f"ADJ-{a.id:04d}",
            "product": product.name if product else "Unknown",
            "location": "Main Warehouse",
            "recorded_qty": product.stock if product else 0,
            "counted_qty": product.stock + a.quantity_change if product else 0,
            "date": "Recent",
            "status": "Done"
        })

    return render_template("adjustments.html",
        active_page="adjustments",
        page_title="Stock Adjustments",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        adjustments=adjustment_list,
        products=products
    )

@adjustment_bp.route("/adjustments/new", methods=["POST"])
def create_adjustment():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    product_id = request.form.get("product_id")
    counted_qty = int(request.form.get("counted_qty") or 0)
    reason = request.form.get("reason")
    action = request.form.get("action")

    product = Product.query.get(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("adjustments.list_adjustments"))

    difference = counted_qty - product.stock

    adjustment = Adjustment(
        product_id=product.id,
        reason=reason,
        quantity_change=difference
    )
    db.session.add(adjustment)
    db.session.commit()

    if action == "validate":
        product.stock = counted_qty
        db.session.commit()
        flash(f"Adjustment validated. {product.name} stock updated to {counted_qty}.", "success")
    else:
        flash("Adjustment saved as draft.", "success")

    return redirect(url_for("adjustments.list_adjustments"))