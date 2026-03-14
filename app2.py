
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

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)




