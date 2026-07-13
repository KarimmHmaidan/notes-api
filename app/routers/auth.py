from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from app.schemas.users import UserCreate, UserResponse, TokenResponse, RefreshTokenRequest
from app.services.users import authenticate_user, create_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.security import create_access_token, create_refresh_token, secret, algo
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()    

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
    except UserAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    
    return db_user

@router.post("/login", response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except InvalidCredentialsException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return {
        "access_token": create_access_token(data={"sub": str(user.id)}),
        "refresh_token": create_refresh_token(data={"sub": str(user.id)}),
        "token_type": "bearer"
    }    


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    request: RefreshTokenRequest
):
    try:
        payload = jwt.decode(
            request.refresh_token,
            secret,
            algorithms=[algo]
        )
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    access_token = create_access_token(
        data={"sub": str(user_id)}
    )

    new_refresh_token = create_refresh_token(
        data={"sub": str(user_id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }