from database import db
class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(200))
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)