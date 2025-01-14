from .product import product
from .order import order
from .endpoint import endpoint

def init_app(app):
    app.register_blueprint(product)
    app.register_blueprint(order)
    app.register_blueprint(endpoint)
