from .. import models, schemas, oauth2
from fastapi import status, HTTPException, Depends, Response, FastAPI, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import TypeVarTuple, Optional, List
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])



# We need a list here because, we are sending all the post
#@router.get("/")
@router.get("/" ,response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
             limit:int = 10, skip :int = 0, search : Optional[str]= ""):
    #cursor.execute(""" SELECT * from posts""")
    #posts = cursor.fetchall()

    # we can use this to get all posts by a user who is logged in
    # this logic works when we are trying to make a app like notes, and we only share note 
    # the user has created for themselves not other peoples notes
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # this will show all the posts to the user that is logged in , its like social media app
    # where post from other users are also visible to everyone
    #posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit=limit).offset(skip).all() 
    # {{URL}}posts?limit=10&skip=0&search
    # left inner is default
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    print("=======================================================================================")
    print(results)
    return results
    

# Depends(oauth2.get_current_user) forces the user to loggeg in 
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostBase, db: Session = Depends(get_db), 
                 current_user :int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (title, content,published) VALUES (%s, %s, %s) RETURNING * """,
    #               (post.title, post.content, post.published))
    
    #new_post = cursor.fetchone()
    #conn.commit()
    #logic to get the owner id of the post based on the user that is loggedin


    new_post = models.Post(owner_id = current_user.id , **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # reteive post and store it in new_post
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db),
             current_user :int = Depends(oauth2.get_current_user)): 
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                     models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with {id} doesn't exist")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    delete_post_query = db.query(models.Post).filter(models.Post.id == id)

    delete_post = delete_post_query.first()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exist")
    
    #conn.commit()
    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not allowed to perform the requested action")
    
    delete_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, post: schemas.PostBase, db: Session = Depends(get_db),
                current_user :int = Depends(oauth2.get_current_user)):
    
    #updated_post = cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
    #RETURNING *""", 
                   #(post.title, post.content, post.published, str(id)))
    ##updated_post = cursor.fetchone() 
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
   
    post_to_update = post_query.first()

    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="Not allows to perfrom the action")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
