from sqlalchemy.orm import Session

from database.models import User


def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    name: str,
    email: str,
    password_hash: str,
    country: str,
    team: str,
    role: str = "user"
):
    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        country=country,
        team=team,
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def list_users(db: Session):
    return db.query(User).all()