from database import db

class Adjustment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    reason = db.Column(db.String(200))
    quantity_change = db.Column(db.Integer)