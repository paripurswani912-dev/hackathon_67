from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from database import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect(url_for("dashboard.get_dashboard_data"))

    flash("Invalid email or password", "error")
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered", "error")
        return redirect(url_for("auth.login_page"))

    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id
    session["username"] = new_user.username
    return redirect(url_for("dashboard.get_dashboard_data"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))