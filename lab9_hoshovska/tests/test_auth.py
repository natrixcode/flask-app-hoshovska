import unittest

from app import create_app, db
from app.users.models import User


class AuthenticationTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.context = self.app.app_context()
        self.context.push()

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def create_user(self):
        user = User(
            username="NataliaTest",
            email="nataliatest@example.com"
        )
        user.set_password("TestPassword2026!")
        db.session.add(user)
        db.session.commit()
        return user

    def test_registration_page(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Створити акаунт", response.get_data(as_text=True))

    def test_login_page(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn("З поверненням!", response.get_data(as_text=True))

    def test_password_hashing(self):
        user = self.create_user()
        self.assertNotEqual(user.password, "TestPassword2026!")
        self.assertTrue(user.password.startswith("$2"))
        self.assertTrue(user.check_password("TestPassword2026!"))
        self.assertFalse(user.check_password("WrongPassword"))

    def test_successful_registration(self):
        response = self.client.post("/register", data={
            "username": "NewUser9",
            "email": "newuser9@example.com",
            "password": "TestPassword2026!",
            "confirm_password": "TestPassword2026!"
        })

        self.assertEqual(response.status_code, 302)

        user = db.session.scalar(
            db.select(User).where(User.username == "NewUser9")
        )

        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("TestPassword2026!"))

    def test_duplicate_username(self):
        self.create_user()

        response = self.client.post("/register", data={
            "username": "NataliaTest",
            "email": "another@example.com",
            "password": "TestPassword2026!",
            "confirm_password": "TestPassword2026!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "вже зайняте",
            response.get_data(as_text=True)
        )

    def test_password_mismatch(self):
        response = self.client.post("/register", data={
            "username": "NewUser9",
            "email": "newuser9@example.com",
            "password": "TestPassword2026!",
            "confirm_password": "DifferentPassword2026!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Паролі не збігаються",
            response.get_data(as_text=True)
        )

    def test_successful_login(self):
        self.create_user()

        response = self.client.post("/login", data={
            "username": "NataliaTest",
            "password": "TestPassword2026!"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Мій профіль",
            response.get_data(as_text=True)
        )
        self.assertIn(
            "nataliatest@example.com",
            response.get_data(as_text=True)
        )

    def test_wrong_password(self):
        self.create_user()

        response = self.client.post("/login", data={
            "username": "NataliaTest",
            "password": "WrongPassword"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Неправильне ім",
            response.get_data(as_text=True)
        )

    def test_account_requires_login(self):
        response = self.client.get("/account")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_users_requires_login(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_users_list(self):
        self.create_user()

        self.client.post("/login", data={
            "username": "NataliaTest",
            "password": "TestPassword2026!"
        })

        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "NataliaTest",
            response.get_data(as_text=True)
        )

    def test_logout(self):
        self.create_user()

        self.client.post("/login", data={
            "username": "NataliaTest",
            "password": "TestPassword2026!"
        })

        response = self.client.post("/logout", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Ви успішно вийшли",
            response.get_data(as_text=True)
        )

        protected = self.client.get("/account")
        self.assertEqual(protected.status_code, 302)

    def test_logout_get_not_allowed(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
