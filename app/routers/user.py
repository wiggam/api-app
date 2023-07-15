from .. import models, schemas, utility
# only new import here was APIRouter, rest were from main.py, router allows main.py to route requests to this file
from fastapi import APIRouter
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

# allows for routing from main.py, sets prefix for path
router = APIRouter(prefix='/users', tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utility.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return user
