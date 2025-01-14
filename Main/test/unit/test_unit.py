import pytest
from app import app, db
from models import Customer, Product, Category, Order, ProductOrder
from manage import create_database


@pytest.fixture
def create_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    return app

@pytest.fixture
def setup_data(create_app):
    with create_app.app_context():
        db.drop_all()
        db.create_all()

        customer = Customer(name="Test User", 
            phone="123-456-7891", 
            email="test@example.com", 
            password="test123"
        )
        
        category = Category(name="spoons", 
            description="N/A"
        )

        product = Product(
            product="large spoon",
            price=1,
            available=10,
            category=category
        )

        order=Order(
            customer=customer
        )
        
        new_order = ProductOrder(
            order=order,
            product=product,
            quantity=2
        )
        db.session.add(customer)
        db.session.add(category)
        db.session.add(product)
        db.session.add(order)
        db.session.add(new_order)
        db.session.commit()

    yield

    with create_app.app_context():
        # Clean up the data after the test runs
        ProductOrder.query.delete()
        Order.query.delete()
        Product.query.delete()
        Category.query.delete()
        Customer.query.delete()
        db.session.commit()
        create_database()

# Model Tests

def test_customer(create_app, setup_data):
    with app.app_context():
        customer = Customer(name="John Doe", phone="1234567890", balance=100.0, email="john@example.com", password="password")
        db.session.add(customer)
        db.session.commit()

        queried_customer = db.session.query(Customer).filter_by(email="john@example.com").first()
        assert queried_customer is not None
        assert queried_customer.name == "John Doe"
        assert queried_customer.balance == 100.0

def test_create_category(create_app, setup_data):
    with app.app_context():
        category = Category(name="electronics", description="Electronic items")
        db.session.add(category)
        db.session.commit()

        queried_category = db.session.query(Category).filter_by(name="electronics").first()
        assert queried_category is not None
        assert queried_category.description == "Electronic items"

def test_create_order_fail(create_app, setup_data):
    with app.app_context():
        customer = db.session.query(Customer).filter_by(id=1).first()
        order = Order(customer=customer, total=150.0)
        db.session.add(order)
        db.session.commit()

        queried_order = db.session.query(Order).filter_by(customer_id=customer.id).first()
        assert queried_order is not None
        assert queried_order.total == 0.0

def test_process_order_fail(create_app, setup_data):
    with app.app_context():
        customer = db.session.query(Customer).filter_by(id=1).first()
        category = db.session.query(Category).filter_by(id=1).first()
        product = db.session.query(Product).filter_by(id=1).first()

        order = db.session.query(Order).filter_by(customer_id=customer.id).first()

        success, message = order.process()
        assert success is False
        assert order.processed is None
        assert customer.balance == 0.0
        assert product.available == 10

def test_create_product_order_fail(create_app, setup_data):
    with app.app_context():
        product = db.session.query(Product).filter_by(id=1).first()
        order = db.session.query(Order).filter_by(id=1).first()

        product_order = ProductOrder(order_id=order.id, product_id=product.id, quantity=2)
        db.session.add(product_order)
        db.session.commit()

        queried_product_order = db.session.query(ProductOrder).filter_by(order_id=order.id).first()
        assert queried_product_order is not None
        assert queried_product_order.quantity == 2
