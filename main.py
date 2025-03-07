from fastapi import FastAPI
from database import create_database
from fastapi.middleware.cors import CORSMiddleware
from authentication.auth_endpoints import authentication_router
from users.users_endpoints import users_router
from posts.posts_endpoints import posts_router

app = FastAPI(
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Endpoints for user authentication and OTP management.",
        },
        {
            "name": "Users",
            "description": "Endpoints for user profile management.",
        },
        {
            "name": "Posts",
            "description": "Endpoints for Posts management.",
        },
    ]
)

# CORS TO CHANGE, JUST FOR DEVELOPMENT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication_router)
app.include_router(users_router)
app.include_router(posts_router)



