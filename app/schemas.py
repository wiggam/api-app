from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
# allow us to set class variables to specific values
from pydantic.types import conint

# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# response when account is created
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # Pydantic's orm_mode will tell the Pydantic model to read the data even if its not a dict, but and ORM model (or any other arbitary object with attributes)
    class Config:
        orm_mode = True

# shcema to limit what can be sent in authorization
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# subclass that pust restrictions on post requests, schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

# class for the FastAPI response, limits what is sent in resposne, schema, this is used within the decorator under main.py
class PostResponse(PostBase):
    # other attributes inherited from class PostBase 
    id: int
    owner_id: int
    created_at: datetime
    # New property type: owner, Returns a pydantic model type: UserOut 
    owner: UserOut

    # Pydantic's orm_mode will tell the Pydantic model to read the data even if its not a dict, but and ORM model (or any other arbitary object with attributes)
    class Config:
        orm_mode = True

class PostResponseVote(BaseModel):
    Post: PostResponse
    votes: int    

    # Pydantic's orm_mode will tell the Pydantic model to read the data even if its not a dict, but and ORM model (or any other arbitary object with attributes)
    class Config:
        orm_mode = True   

# schema for authorizing token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# schema for voting
class Vote(BaseModel):
    post_id: int
    #either 0 or 1, for liking and unliking a post, less than or equal to one, greater than 0
    dir: conint(ge=0, le=1)
