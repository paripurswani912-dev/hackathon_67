from flask import Blueprint, request, jsonify
from database import db
from models.receipt import Receipt
from models.product import Product

receipt_bp = Blueprint("receipts", __name__)