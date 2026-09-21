import unittest

from app.auth.security import verify_password
from app.database import SessionLocal, init_db
from app.models.user import User


class DemoAuthSeedTests(unittest.TestCase):
    def test_seeded_demo_accounts_use_default_password(self):
        init_db()

        with SessionLocal() as db:
            simphiwe = db.query(User).filter(User.email == "simphiwe@simplycomplex.africa").one()
            siphiwe = db.query(User).filter(User.email == "siphiwe@simplycomplex.africa").one()

        self.assertTrue(verify_password("Password123!", simphiwe.password_hash))
        self.assertTrue(verify_password("Password123!", siphiwe.password_hash))


if __name__ == "__main__":
    unittest.main()
