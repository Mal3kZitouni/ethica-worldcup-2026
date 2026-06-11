from database.connection import SessionLocal
from database.models import User
from utils.security import verify_password


# ----------------------
# AUTH USER
# ----------------------
def authenticate_user(email, password):

    email = email.strip().lower()

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    finally:
        db.close()