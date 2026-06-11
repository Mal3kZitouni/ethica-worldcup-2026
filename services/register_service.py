from database.connection import SessionLocal
from database.models import User
from passlib.hash import bcrypt


def register_user(
    name,
    email,
    password,
    country,
    team
):

    email = email.strip().lower()

    db = SessionLocal()

    try:

        # Only Ethica emails allowed
        if not email.endswith("@groupe-ethica.com"):
            return (
                False,
                "Only @groupe-ethica.com email addresses are allowed"
            )

        existing = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing:
            return False, "Email already exists"

        user = User(
            name=name,
            email=email,
            password_hash=bcrypt.hash(password),
            country=country,
            team=team,
            role="user"
        )

        db.add(user)
        db.commit()

        return True, "Account created"

    finally:
        db.close()