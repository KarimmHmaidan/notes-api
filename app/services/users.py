from app.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.users import UserCreate
from app.security import hash_password, verify_password


def create_user(db: Session, user: UserCreate):
    normalized_username = user.username.lower()
    normalized_email = user.email.lower()
    existing_user = db.query(User).filter((User.username == normalized_username) | (User.email == normalized_email)).first()
    if existing_user:
        raise UserAlreadyExistsException()
    hashed_pw = hash_password(user.password)
    db_user = User(username=normalized_username, email=normalized_email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, login_identifier: str, password: str):
    normalized_identifier = login_identifier.lower()
    user = db.query(User).filter((User.username == normalized_identifier) | (User.email == normalized_identifier)).first()
    if not user:
        raise InvalidCredentialsException()
    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException()
    return user
    

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()       



