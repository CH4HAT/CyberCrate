import pytest
from app import app
from routes.endpoint import register, login, profile, register, get_categories
from routes.product import get_product_by_category
from flask import url_for
from flask_testing import TestCase
from flask_login import current_user
from db import db
from models import Customer
from manage import create_database

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_homepage(self):
        response = self.client.get(url_for('main.homepage'))
        assert response.status_code == 200
        assert b"Home" in response.data  # Assuming "Home" text is in index.html

    def test_profile_unauthenticated(self):
        response = self.client.get(url_for('main.profile'))
        assert response.status_code == 302  # Redirect to login page

    def test_login_get(self):
        response = self.client.get(url_for('main.login'))
        assert response.status_code == 200
        assert b"Login" in response.data  # Assuming "Login" text is in login.html

    def test_register_get(self):
        response = self.client.get(url_for('main.register'))
        assert response.status_code == 200
        assert b"Create an account" in response.data  # Assuming "Register" text is in sign_up.html

    def test_profile_authenticated(self):
        # Register a user
        self.client.post('/register', data=dict(
            name='Test User',
            phone='1234567890',
            email='test@example.com',
            password='testpassword'
        ))

        # Login the user
        self.client.post('/login', data=dict(
            email='test@example.com',
            password='testpassword'
        ))

        response = self.client.get(url_for('main.profile'))
        assert response.status_code == 200
        assert b"Profile" in response.data  # Assuming "Profile" text is in profile.html

    def test_register_post(self):
        response = self.client.post('/register', data=dict(
            name='New User',
            phone='0987654321',
            email='new@example.com',
            password='newpassword'
        ))
        assert response.status_code == 302  # Redirect after successful registration

        # Check if the user is added to the database
        user = Customer.query.filter_by(email='new@example.com').first()
        assert user is not None
        assert user.name == 'New User'

    def test_login_post(self):
        # Register a user
        self.client.post('/register', data=dict(
            name='Test User',
            phone='1234567890',
            email='test@example.com',
            password='testpassword'
        ))

        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='testpassword'
        ))
        assert response.status_code == 302  # Redirect after successful login
        assert current_user.is_authenticated

    def test_logout(self):
        # Register and login a user
        self.client.post('/register', data=dict(
            name='Test User',
            phone='1234567890',
            email='test@example.com',
            password='testpassword'
        ))

        self.client.post('/login', data=dict(
            email='test@example.com',
            password='testpassword'
        ))

        response = self.client.get(url_for('main.logout'))
        assert response.status_code == 302  # Redirect after logout
        assert not current_user.is_authenticated

    def test_get_product_by_category(self):
        # Assuming the categories exist and have products associated with them
        for category_id in range(1, 4):
            response = self.client.get(url_for('product.get_product_by_category', id=category_id))
            assert response.status_code == 200

        # Test a non-existing category
        response = self.client.get(url_for('product.get_product_by_category', id=999))
        assert response.status_code == 400  # Assuming 404 for non-existing category

    def test_get_categories(self):
        response = self.client.get(url_for('main.get_categories'))
        assert response.status_code == 200
        assert b"Store A" in response.data  # Assuming "Categories" text is in show_categories.html

    def test_add_order(self):
        self.client.post('/register', data=dict(
            name='Test User',
            phone='1234567890',
            email='test@example.com',
            password='testpassword'
        ))

        self.client.post('/login', data=dict(
            email='test@example.com',
            password='testpassword'
        ))

        response = self.client.post(url_for('order.add_order', item_name='test_item', customer_id = 1), data={'quantity': 2})
        assert response.status_code == 200
        # Add assertions to check if the order is created correctly

        
if __name__ == '__main__':
    pytest.main()
