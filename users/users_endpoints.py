from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
import authentication.auth_service as auth_service
from sqlalchemy.orm import Session
from database import get_db
import schemas
import users.users_service as users_service
from security import oauth2_scheme

users_router = APIRouter(prefix="/users", tags=["Users"])
@users_router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth_service.get_user_from_token(token, db)
    return user

@users_router.put("/edit-profile")
async def edit_profile( userData: schemas.UserUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = auth_service.get_user_from_token(token, db)
        users_service.edit_user_data(db, user, userData)
        return {"message": "Profile updated successfully"}

    except HTTPException as e:
        raise e  # Re-raise HTTPExceptions from auth_service
    except Exception as e:
        # Log the error (optional)
        print(f"Error updating profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

@users_router.get("/protected-resource")
async def protected_resource(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected resource"}