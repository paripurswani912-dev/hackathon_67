from database import db
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200))
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)