from fastapi import FastAPI
from typing import Optional, List
# from current file import models.py
from . import models
from .database import engine
# brings in post.py and user.py
from .routers import post, user, auth, vote
from .config import Settings
# allows other domains to interact with our API
from fastapi.middleware.cors import CORSMiddleware

# From FastAPI documentation, uses the model we set in models.py, creates the table with the schema set in models.py, no longer needed because we are using alembic
# models.Base.metadata.create_all(bind=engine)

# creates FastAPI instance
app = FastAPI()

# A list of domains that can access our API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# routes the request to each file, if it finds a match it will deploy the appropriate action and response
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {'message': 'hello world'}




 