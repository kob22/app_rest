from app import app
from app.models import Product
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    items = Product.query.all()

    return render_template('index.html', products = items)