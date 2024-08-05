import unittest
from app import app, db


class UserAuthServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        self.username = "testuser"
        self.email = "testemail@gmail.com"
        self.password = "testpassword"

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_1_register(self):
        # Successful registration
        case_1_response = self.client.post(
            "/user/register",
            json={
                "username": self.username,
                "email": self.email,
                "password": self.password,
            },
        )
        self.assertEqual(case_1_response.status_code, 201)
        self.assertEqual(
            case_1_response.json.get("message"), "User registered successfully"
        )

        # Successful registration with another email
        case_2_response = self.client.post(
            "/user/register",
            json={
                "username": self.username,
                "email": "testemail2@gmail.com",
                "password": self.password,
            },
        )
        self.assertEqual(case_2_response.status_code, 409)
        self.assertEqual(case_2_response.json.get("message"), "Username already exists")

        # Validation for all fields
        case_3_response = self.client.post(
            "/user/register",
            json={
                "username": "",
                "email": "",
                "password": "",
            },
        )
        self.assertEqual(case_3_response.status_code, 400)
        self.assertEqual(case_3_response.json.get("message"), "All fields are required")

        # Validation for accureate email address
        case_4_response = self.client.post(
            "/user/register",
            json={
                "username": self.username,
                "email": "testemail@gmailcom",
                "password": self.password,
            },
        )

        self.assertEqual(case_4_response.status_code, 400)
        self.assertEqual(case_4_response.json.get("message"), "Invalid email address")

    def test_2_login(self):
        # Successful registration
        case_1_response = self.client.post(
            "/user/register",
            json={
                "username": self.username,
                "email": self.email,
                "password": self.password,
            },
        )
        self.assertEqual(case_1_response.status_code, 201)
        self.assertEqual(
            case_1_response.json.get("message"), "User registered successfully"
        )

        # validation case
        case_2_response = self.client.post(
            "/user/login",
            json={
                "username": "",
                "email": "",
                "password": "",
            },
        )
        self.assertEqual(case_2_response.status_code, 400)

        # Successful login
        case_3_response = self.client.post(
            "/user/login",
            json={
                "username": self.username,
                "email": self.email,
                "password": self.password,
            },
        )
        self.assertEqual(case_3_response.status_code, 200)
        self.assertIn(b"token", case_3_response.data)

        # Invalid email address
        case_5_response = self.client.post(
            "/user/login",
            json={
                "username": self.username,
                "email": "testemail@gmailcom",
                "password": self.password,
            },
        )
        self.assertEqual(case_5_response.status_code, 400)
        self.assertEqual(case_5_response.json.get("message"), "Invalid email address")

        # Invalid credentials
        case_6_response = self.client.post(
            "/user/login",
            json={
                "username": self.username,
                "email": self.email,
                "password": "wrongpassword",
            },
        )
        self.assertEqual(case_6_response.status_code, 401)
        self.assertEqual(case_6_response.json.get("message"), "Invalid credentials")


if __name__ == "__main__":
    unittest.main()
