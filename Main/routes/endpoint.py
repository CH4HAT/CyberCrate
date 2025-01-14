from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from auth import login_manager
from flask_login import login_user, logout_user, current_user
from models import Customer, Order, Product

endpoint = Blueprint('main', __name__)

@login_manager.user_loader
def loader_user(customer_id):
    return Customer.query.get(customer_id)

@endpoint.route('/')
def homepage():
    return render_template("index.html")

@endpoint.route("/profile")
def profile():
    if current_user.is_authenticated:
        return render_template("profile.html")
    else:
        return redirect(url_for("main.homepage"))

@endpoint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        customer = Customer.query.filter_by(email=request.form.get("email")).first()
        if customer and customer.password == request.form.get("password"):
            login_user(customer)
            return redirect(url_for("main.profile"))
    return render_template("login.html")

@endpoint.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")

        if (Customer.query.filter_by(name=request.form.get("name")).first()):
            return render_template("sign_up.html")
        
        customer = Customer(name=name, phone=phone, email=email, password=password)
        
        db.session.add(customer)
        db.session.commit()
        
        return redirect(url_for("main.login"))
    
    return render_template("sign_up.html")

@endpoint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.homepage"))

@endpoint.route('/categories/')
def get_categories():
    return render_template("show_categories.html")