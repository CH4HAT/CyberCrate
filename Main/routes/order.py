from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from db import db
from models import Order, Customer, ProductOrder, Product

order = Blueprint('order', __name__)

@order.route('/test/<string:item_name>', methods=['GET','POST'])
def add_order(item_name):
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        customer_id = current_user.id
        
        order = Order(customer_id=customer_id)
        db.session.add(order)

        db.session.commit()
        product = Product.query.filter_by(product=item_name).first()
        if product:
            product.available -= int(quantity)
            new_order = ProductOrder(order=order, product=product, quantity=quantity)
            db.session.add(new_order)

        db.session.commit()
            
        return render_template('profile.html'), 200
    return render_template('show_categories.html'), 200

@order.route('/cart', methods=['GET'])
def show_cart():
    get_orders = Order.query.filter_by(customer_id=current_user.id).all()

    get_product_orders = []
    for i in get_orders:
        get_product_orders.append(ProductOrder.query.filter_by(order_id=i.id).first())
    
    products = []
    totals = 0
    for i in get_product_orders:
        products.append(Product.query.filter_by(id=i.product_id).first())
    
    for i in products:
        totals += i.price

    return render_template('cart.html', products=products, total=totals), 200
