from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

#user is providin login information, schema to force it into proper format
# OAuth2PasswordRequestForm will return username and password , so need to change emal

# user can use the access token to access the data from the api 
#@router.post('/login', response_model=schemas.Token)
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail="Invalid Credential")

    access_token = oauth2.create_access_token(data={"user_id":user.id})


    return {"token": access_token, "token_type": "bearer"}
    
