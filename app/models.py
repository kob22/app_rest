from datetime import time
from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='products', lazy=True)
    name = db.Column(db.String(360), index=True)
    link = db.Column(db.String(360), unique=True, index=True)
    rating = db.Column(db.Float(2))
    votes = db.Column(db.Integer)
    orders = db.Column(db.Integer)
    reg_low_price = db.Column(db.Float(2))
    reg_high_price = db.Column(db.Float(2))
    dis_low_price = db.Column(db.Float(2))
    dis_high_price = db.Column(db.Float(2))
    img_link = db.Column(db.String(360), index=True)