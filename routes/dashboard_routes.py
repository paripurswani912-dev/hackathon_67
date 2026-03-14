from flask import Blueprint, jsonify
from models.product import Product
from models.receipt import Receipt
from models.delivery import Delivery
from models.transfer import Transfer

dashboard_bp = Blueprint("dashboard", __name__)
@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard_data():

    # total products
    total_products = Product.query.count()

    # total stock quantity
    total_stock = sum(p.stock for p in Product.query.all())

    # low stock (example threshold = 10)
    low_stock = Product.query.filter(Product.stock < 10).count()

    # out of stock
    out_of_stock = Product.query.filter(Product.stock == 0).count()

    # total receipts
    total_receipts = Receipt.query.count()

    # total deliveries
    total_deliveries = Delivery.query.count()

    # total transfers
    total_transfers = Transfer.query.count()

    return jsonify({
        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock_items": low_stock,
        "out_of_stock_items": out_of_stock,
        "receipts": total_receipts,
        "deliveries": total_deliveries,
        "transfers": total_transfers
    })
    