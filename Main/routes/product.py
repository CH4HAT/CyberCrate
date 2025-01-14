from flask import Blueprint, request, jsonify, render_template
from db import db
from models import Product, Category

product = Blueprint('product', __name__)

@product.route('/category/<int:id>')
def get_products_by_category(id):
    if Category.query.filter_by(id=id).first():
        products = Product.query.filter(Product.category.has(id=id)).all()

        return render_template('show_products_by_category.html', products=products), 200
    return "Non valid category", 400

@product.route('/single/product/<int:id>')
def get_product_by_category(id):
    if Category.query.filter_by(id=id).first():
        products = Product.query.filter(Product.category.has(id=id)).first()

        return render_template('make_order.html', products=products), 200
    return "Non valid category",400