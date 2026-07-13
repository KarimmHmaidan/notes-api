import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from jose import jwt,JWTError
from app.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


load_dotenv()
algo = os.getenv("jwt_algorithm")
secret = os.getenv("secret_key")




def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret, algorithms=[algo])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        current_user =db.query(User).filter(User.id == int(user_id)).first()
        if current_user is None:
            raise credentials_exception
        return current_user
    except JWTError:
        raise credentials_exception
        