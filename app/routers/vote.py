from fastapi import status, HTTPException, Depends, Response, FastAPI, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=['Votes'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote , db : Session = Depends(database.get_db), 
         current_user : int = Depends(oauth2.get_current_user)):
   
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested post with id {vote.post_id} not found")
    
    # if this user has alreasy voted for this post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                     models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if ( vote.dir==1 ):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id } already voted for this post id {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "SUcessfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail= "vote does not exits")
        vote_query.delete(synchronize_session=False)
        db.commit()
         
        return {"message":"sucesscfully deleted vote"}
        

        
        
        

