from sqlalchemy import func
from models import User, Post
from schemas import PostCreate
from sqlalchemy.orm import Session

def create_post_data(user : User, postData : PostCreate, db: Session):
    post_data_dict = postData.model_dump()
    post_data_dict["user_phone_number"] = user.phone_number

    new_post = Post(**post_data_dict)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post