from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from app.schemas.users import UserCreate, UserResponse, TokenResponse, RefreshTokenRequest
from app.services.users import authenticate_user, create_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.security import create_access_token, create_refresh_token, hash_token, secret, algo
from fastapi.security import OAuth2PasswordRequestForm
from app.services.refresh_tokens import save_refresh_token, get_refresh_token, revoke_refresh_token, revoke_refresh_token_by_value

router = APIRouter()    

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
    except UserAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    
    return db_user

@router.post("/login", response_model=TokenResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(
            db,
            form_data.username,
            form_data.password
        )
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    save_refresh_token(
        db=db,
        user_id=user.id,
        refresh_token=refresh_token
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
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


    token_hash = hash_token(request.refresh_token)

    stored_token = get_refresh_token(
        db=db,
        user_id=int(user_id),
        token_hash=token_hash
    )


    if stored_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )


    if stored_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked"
        )


    if stored_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )


   
    revoke_refresh_token(
        db,
        stored_token
    )


    
    access_token = create_access_token(
        data={"sub": str(user_id)}
    )

    new_refresh_token = create_refresh_token(
        data={"sub": str(user_id)}
    )


    
    save_refresh_token(
        db=db,
        user_id=int(user_id),
        refresh_token=new_refresh_token
    )


    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    token = revoke_refresh_token_by_value(
        db,
        request.refresh_token
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    return {
        "message": "Successfully logged out"
    }