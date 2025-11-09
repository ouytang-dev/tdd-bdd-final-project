
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test cases for Product Model
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel
"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)
    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()
    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()
    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)
    #
    # ADD YOUR TEST CASES HERE
    #
    def test_read_a_product(self):
        """It should read a product"""
        # Create the product
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        #Try and read the created product id
        read_product = Product.find(product.id)
        self.assertEqual(read_product.id,product.id)
    #
    def test_update_a_product(self):
        """It should update a product"""
        # Create the product
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # change product description and update
        product.description = "new description"
        product.update()
        # read the same ID and see if description has changed
        read_product = Product.find(product.id)
        self.assertEqual(read_product.id,product.id)
        self.assertEqual(read_product.description,"new description")

    def test_delete_a_product(self):
        """It should delete a product"""
        # Create the product
        product = ProductFactory()
        product.create()
        # confirm that it was created
        self.assertEqual(len(Product.all()), 1)
        # delete it then confirm it was deleted.
        product.delete()
        self.assertEqual(len(Product.all()), 0)
 
    def test_list_all_product(self):
        """It should list all products"""
        # Retrieve all current products, should be empty
        products = Product.all()
        self.assertEqual(len(products), 0)
        # add 5 products
        for _ in range(5):
            product = ProductFactory()
            product.create()
        # retieve all products again and check that there are now 5 products
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_product_find_by_name(self):
        """It should find a product by product name"""
        # Create 5 fake products
        products = ProductFactory.create_batch(5)
        # Add products to database
        for product in products:
            product.create()
        # get name of first product
        first_name = products[0].name
        # save same name count in products.
        count = 0
        for product in products:
            if product.name == first_name:
                count += 1 
        # find the product by name and confirm the same occurs
        found_products = Product.find_by_name(first_name)
        self.assertEqual(found_products.count(),count)
        for product in found_products:
            self.assertEqual(product.name,first_name)

    def test_product_find_by_price(self):
        """It should find a product by product price"""
        # Create 5 fake products
        products = ProductFactory.create_batch(10)
        # Add products to database
        for product in products:
            product.create()
        # get name of first product
        first_price = products[0].price
        # count number of of same availability
        count = 0
        for product in products:
            if product.price == first_price:
                count += 1
        # find the product by name and confirm the same occurs
        found_products = Product.find_by_price(first_price)
        self.assertEqual(found_products.count(),count)
        for product in found_products:
            self.assertEqual(product.price,first_price)

    def test_product_find_by_availability(self):
        """It should find a product by product availability"""
        # Create 5 fake products
        products = ProductFactory.create_batch(10)
        # Add products to database
        for product in products:
            product.create()
        # get name of first product
        first_available = products[0].available
        # count number of of same availability
        count = 0
        for product in products:
            if product.available == first_available:
                count += 1
        # find the product by name and confirm the same occurs
        found_products = Product.find_by_availability(first_available)
        self.assertEqual(found_products.count(),count)
        for product in found_products:
            self.assertEqual(product.available,first_available)

    def test_product_find_by_category(self):
        """It should find a product by product category"""
        # Create 5 fake products
        products = ProductFactory.create_batch(10)
        # Add products to database
        for product in products:
            product.create()
        # get name of first product
        first_category = products[0].category
        # count number of of same category
        count = 0
        for product in products:
            if product.category == first_category:
                count += 1
        # find the product by name and confirm the same occurs
        found_products = Product.find_by_category(first_category)
        self.assertEqual(found_products.count(),count)
        for product in found_products:
            self.assertEqual(product.category,first_category)
