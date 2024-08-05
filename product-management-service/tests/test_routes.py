import unittest
from app import app, db


class ProductManagementServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_1_add_product(self):
        # Successful product addition
        response = self.client.post(
            "/products",
            json={
                "name": "Product 1",
                "description": "Description for product 1",
                "price": 99.99,
                "stock": 10,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("message"), "Product added successfully")

        # Validation for missing fields
        response = self.client.post(
            "/products",
            json={
                "name": "",
                "description": "",
                "price": "",
                "stock": "",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get("message"), "All fields are required")

    def test_2_get_products(self):
        # Add a product
        self.client.post(
            "/products",
            json={
                "name": "Product 1",
                "description": "Description for product 1",
                "price": 99.99,
                "stock": 10,
            },
        )

        # Get products
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)

    def test_3_get_product(self):
        # Add a product
        self.client.post(
            "/products",
            json={
                "name": "Product 1",
                "description": "Description for product 1",
                "price": 99.99,
                "stock": 10,
            },
        )

        # Get product
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Product 1")

        # Get non-existent product
        response = self.client.get("/products/2")
        self.assertEqual(response.status_code, 404)

    def test_4_update_product(self):
        # Add a product
        self.client.post(
            "/products",
            json={
                "name": "Product 1",
                "description": "Description for product 1",
                "price": 99.99,
                "stock": 10,
            },
        )

        # Update product
        response = self.client.put(
            "/products/1",
            json={
                "name": "Updated Product 1",
                "description": "Updated description for product 1",
                "price": 89.99,
                "stock": 5,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("message"), "Product updated successfully")

        # Validation for missing fields
        response = self.client.put(
            "/products/1",
            json={
                "name": "",
                "description": "",
                "price": "",
                "stock": "",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get("message"), "All fields are required")

    def test_5_delete_product(self):
        # Add a product
        self.client.post(
            "/products",
            json={
                "name": "Product 1",
                "description": "Description for product 1",
                "price": 99.99,
                "stock": 10,
            },
        )

        # Delete product
        response = self.client.delete("/products/1")
        self.assertEqual(response.status_code, 204)

        # Delete non-existent product
        response = self.client.delete("/products/1")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
