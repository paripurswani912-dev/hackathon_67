from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models.product import Product

product_bp = Blueprint("products", __name__)

@product_bp.route("/products", methods=["GET"])
def list_products():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    products = Product.query.all()
    return render_template("products.html",
        active_page="products",
        page_title="Products",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        products=products
    )

@product_bp.route("/products/new", methods=["POST"])
def add_product():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    name = request.form.get("name")
    sku = request.form.get("sku")
    category = request.form.get("category")
    unit = request.form.get("unit")
    stock = int(request.form.get("initial_stock") or 0)
    location = request.form.get("location")

    product = Product(
        name=name,
        sku=sku,
        category=category,
        unit=unit,
        stock=stock
    )
    db.session.add(product)
    db.session.commit()

    flash("Product added successfully", "success")
    return redirect(url_for("products.list_products"))

@product_bp.route("/products/<int:id>/edit", methods=["GET"])
def edit_product(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    product = Product.query.get(id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("products.list_products"))

    products = Product.query.all()
    return render_template("products.html",
        active_page="products",
        page_title="Products",
        current_user=type("User", (), {"username": session.get("username", "U")})(),
        products=products,
        edit_product=product
    )