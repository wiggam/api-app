from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utility, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentails.username).first()

    # if emails does not exist
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # if hashed passwords do not match
    if not utility.verify(user_credentails.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
    