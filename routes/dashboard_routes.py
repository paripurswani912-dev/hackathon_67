from flask import Blueprint, render_template, session, redirect, url_for
from models.product import Product
from models.receipt import Receipt
from models.delivery import Delivery
from models.transfer import Transfer
from models.adjustment import Adjustment

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard_data():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock < 10).count()
    out_of_stock = Product.query.filter(Product.stock == 0).count()
    pending_receipts = Receipt.query.count()
    pending_deliveries = Delivery.query.count()

    recent_operations = []

    for r in Receipt.query.order_by(Receipt.id.desc()).limit(5).all():
        product = Product.query.get(r.product_id)
        recent_operations.append({
            "reference": f"REC-{r.id:04d}",
            "type": "Receipt",
            "product": product.name if product else "Unknown",
            "qty": f"{r.quantity}",
            "date": "Recent",
            "status": "Done"
        })

    for d in Delivery.query.order_by(Delivery.id.desc()).limit(5).all():
        product = Product.query.get(d.product_id)
        recent_operations.append({
            "reference": f"DEL-{d.id:04d}",
            "type": "Delivery",
            "product": product.name if product else "Unknown",
            "qty": f"{d.quantity}",
            "date": "Recent",
            "status": "Done"
        })

    low_stock_items = []
    for p in Product.query.filter(Product.stock < 10).all():
        low_stock_items.append({
            "name": p.name,
            "location": "Main Warehouse",
            "qty": p.stock
        })

    recent_activity = []
    for r in Receipt.query.order_by(Receipt.id.desc()).limit(3).all():
        product = Product.query.get(r.product_id)
        recent_activity.append({
            "text": f"Receipt validated. Stock +{r.quantity} {product.name if product else ''}.",
            "time": "Recent"
        })

    return render_template("dashboard.html",
        active_page="dashboard",
        page_title="Dashboard",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        total_products=total_products,
        low_stock=low_stock,
        out_of_stock=out_of_stock,
        pending_receipts=pending_receipts,
        pending_deliveries=pending_deliveries,
        recent_operations=recent_operations,
        low_stock_items=low_stock_items,
        recent_activity=recent_activity
    )