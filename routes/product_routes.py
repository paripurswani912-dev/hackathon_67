from flask import Blueprint, request, jsonify
from database import db
from models.product import Product

product_bp = Blueprint("products", __name__)
@product_bp.route("/products", methods=["POST"])
def add_product():

    data = request.get_json()

    product = Product(
        name=data.get("name"),
        sku=data.get("sku"),
        category=data.get("category"),
        unit=data.get("unit"),
        stock=data.get("stock", 0)
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added successfully"})

@product_bp.route("/products", methods=["GET"])
def list_products():

    products = Product.query.all()

    result = []

    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "category": p.category,
            "unit": p.unit,
            "stock": p.stock
        })

    return jsonify(result)    
@product_bp.route("/products/<int:id>", methods=["GET"])
def view_product(id):

    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "sku": product.sku,
        "category": product.category,
        "unit": product.unit,
        "stock": product.stock
    })    