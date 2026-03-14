
from flask import Flask
from database import db

# Import models so SQLAlchemy registers them
from models.user import User
from models.product import Product
from models.receipt import Receipt
from models.delivery import Delivery
from models.transfer import Transfer
from models.adjustment import Adjustment

# Import routes
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.receipt_routes import receipt_bp
from routes.delivery_routes import delivery_bp
from routes.transfer_routes import transfer_bp
from routes.adjustment_routes import adjustment_bp
from routes.dashboard_routes import dashboard_bp
from routes.move_history_routes import move_history_bp


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'koshex-secret-2026'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(receipt_bp)
app.register_blueprint(delivery_bp)
app.register_blueprint(transfer_bp)
app.register_blueprint(adjustment_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(move_history_bp)
@app.route("/")
def home():
    from flask import redirect
    return redirect("/login")
@app.route("/profile")
def profile():
    from flask import render_template, session, redirect, url_for
    from models.user import User
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    user = User.query.get(session["user_id"])
    return render_template("profile.html",
        active_page="profile",
        page_title="My Profile",
        current_user=user
    )
@app.route("/settings")
def settings():
    from flask import render_template, session, redirect, url_for
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("settings.html",
        active_page="settings",
        page_title="Settings",
        current_user=type("User", (), {"username": session.get("username", "U")})()
    )
# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)




