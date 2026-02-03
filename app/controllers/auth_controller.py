from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password is too long")

    password = password.encode("utf-8")
    return pwd.hash(password)


def verify_password(password: str, hashed: str):
    if len(password.encode("utf-8")) > 72:
        return False

    password = password.encode("utf-8")
    return pwd.verify(password, hashed)


def register_user(db: Session, name: str, email: str, password: str):
    if db.query(User).filter(User.email == email).first():
        return None

    hashed_password = hash_password(password)

    user = User(
        name=name,
        email=email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user
