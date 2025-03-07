from models import User
from datetime import datetime, timezone
from fastapi import HTTPException, status


def edit_user_data(db, user, userData):

    # Check for username uniqueness (if changed)
    if userData.username != user.username:
        existing_user = db.query(User).filter(User.username == userData.username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    user.username = userData.username
    user.full_name = userData.full_name
    user.date_of_birth = userData.date_of_birth
    user.gender = userData.gender
    user.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)