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

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)

@app.route("/")
def home():
    return {"message": "CoreInventory Running"}

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)