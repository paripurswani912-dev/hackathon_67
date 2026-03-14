from database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    sku = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(100))
    unit = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)