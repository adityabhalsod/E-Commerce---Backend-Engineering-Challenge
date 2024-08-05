import unittest
from app import app, db
from app.models import Order
from flask_jwt_extended import create_access_token
from datetime import datetime


class OrderManagementServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create a test user and generate a token
            self.test_user_id = 1  # assuming a user ID for testing
            self.access_token = create_access_token(identity=self.test_user_id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_1_create_order(self):
        # Successful order creation
        response = self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 2,
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("message"), "Order created successfully")

    def test_2_get_orders(self):
        # Create an order
        self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 2,
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Get orders
        response = self.client.get(
            "/orders", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)

    def test_3_get_order(self):
        # Create an order
        self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 2,
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Get order
        response = self.client.get(
            "/orders/1", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["product_id"], 1)

        # Get non-existent order
        response = self.client.get(
            "/orders/2", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json.get("message"), "Order not found")

    def test_4_update_order(self):
        # Create an order
        self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 2,
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Update order
        response = self.client.put(
            "/orders/1",
            json={"status": "Shipped"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("message"), "Order updated successfully")

    def test_5_delete_order(self):
        # Create an order
        self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 2,
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Delete order
        response = self.client.delete(
            "/orders/1", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        self.assertEqual(response.status_code, 204)

        # Delete non-existent order
        response = self.client.delete(
            "/orders/1", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json.get("message"), "Order not found")


if __name__ == "__main__":
    unittest.main()
