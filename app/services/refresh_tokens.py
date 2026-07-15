from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import RefreshToken
from app.security import hash_token


def save_refresh_token(
    db: Session,
    user_id: int,
    refresh_token: str,
):
    token_hash = hash_token(refresh_token)

    expires_at = datetime.utcnow() + timedelta(days=7)

    existing_token: RefreshToken | None = (
        db.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id)
        .first()
    )

    if existing_token:
        existing_token.token_hash = token_hash
        existing_token.expires_at = expires_at
        existing_token.revoked = False

    else:
        db_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            revoked=False,
        )

        db.add(db_token)

    db.commit()


def get_refresh_token(
    db: Session,
    user_id: int,
    token_hash: str,
):
    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.token_hash == token_hash
        )
        .first()
    )


def revoke_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
):
    refresh_token.revoked = True
    db.commit()



def revoke_refresh_token_by_value(
    db: Session,
    refresh_token: str
):
    token_hash = hash_token(refresh_token)

    stored_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash
        )
        .first()
    )

    if stored_token is None:
        return None

    if stored_token.revoked:
        return None

    stored_token.revoked = True
    db.commit()

    return stored_token