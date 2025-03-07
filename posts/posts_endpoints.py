from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
import authentication.auth_service as auth_service
from sqlalchemy.orm import Session
from database import get_db
import schemas
from security import oauth2_scheme
import posts.posts_service as posts_service

posts_router = APIRouter(prefix="/posts", tags=["Posts"])

@posts_router.post("/create-post", response_model=schemas.PostResponse)
async def create_post(postData: schemas.PostCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = auth_service.get_user_from_token(token, db)
        new_post = posts_service.create_post_data(user, postData, db)
        print('creato')
        return schemas.PostResponse.model_validate(new_post)

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error creating post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )