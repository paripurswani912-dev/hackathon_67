from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models.delivery import Delivery
from models.product import Product

delivery_bp = Blueprint("deliveries", __name__)

@delivery_bp.route("/delivery", methods=["GET"])
def list_deliveries():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    deliveries = Delivery.query.order_by(Delivery.id.desc()).all()
    products = Product.query.all()

    delivery_list = []
    for d in deliveries:
        product = Product.query.get(d.product_id)
        delivery_list.append({
            "id": d.id,
            "reference": f"DEL-{d.id:04d}",
            "customer": d.customer,
            "product": product.name if product else "Unknown",
            "qty": f"{d.quantity}",
            "warehouse": "Main Warehouse",
            "date": "Recent",
            "status": "Done"
        })

    return render_template("delivery.html",
        active_page="delivery",
        page_title="Delivery Orders",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        deliveries=delivery_list,
        products=products
    )

@delivery_bp.route("/delivery/new", methods=["POST"])
def create_delivery():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    customer = request.form.get("customer")
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("qty") or 0)
    action = request.form.get("action")

    delivery = Delivery(
        customer=customer,
        product_id=product_id,
        quantity=quantity
    )
    db.session.add(delivery)
    db.session.commit()

    if action == "validate":
        product = Product.query.get(product_id)
        if not product:
            flash("Product not found.", "error")
            return redirect(url_for("deliveries.list_deliveries"))

        if product.stock < quantity:
            flash(f"Not enough stock. Only {product.stock} available.", "error")
            return redirect(url_for("deliveries.list_deliveries"))

        product.stock -= quantity
        db.session.commit()
        flash(f"Delivery validated. Stock -{quantity} for {product.name}.", "success")
    else:
        flash("Delivery saved as draft.", "success")

    return redirect(url_for("deliveries.list_deliveries"))