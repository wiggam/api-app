from .. import models, schemas, oauth2
# only new import here was APIRouter, rest were from main.py, router allows main.py to route requests to this file
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
# allows us to use count function in our ORM queries
from sqlalchemy import func

# allows for routing from main.py, sets prefix for path
router = APIRouter(prefix="/posts", tags=['Posts'])

# app = instance
# get = method
# "/" = path
# root = function

## ORM GET query
# must use List[] from typing library because FastAPI trys to up all posts into a single dict
@router.get("/", response_model=List[schemas.PostResponseVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # SQL code: 
    # SELECT posts.id, posts.owner_id, COUNT(votes.post_id) as LIKES FROM posts
    # LEFT JOIN votes
    # ON posts.id = votes.post_id
    # WHERE posts.id = 10
    # GROUP BY posts.id;
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results

## SQL GET query
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts;""")
#     posts = cursor.fetchall()
#     return {"data": posts} 

## ORM POST query
# user_id parameter is the token that the user recieves when their login is successful. 
# The depends function allows you to declare these dependencies directly within the function signature, 
# making it clear what requirements need to be met before executing the function.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(posts: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # turns the posts object into a dictionary and unpacks it into the method, assigns user id login as owner id
    new_post = models.Post(owner_id=current_user.id, **posts.dict())
    # OLD : new_post = models.Post(title=posts.title, content=posts.content, published=posts.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

## SQL POST query
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(posts: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (posts.title, posts.content, posts.published))
#     created_post = cursor.fetchone()
#     conn.commit()
#     return {"data": created_post} 

# ORM GET{ID} query
@router.get("/{id}", response_model=schemas.PostResponseVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found")
        # alternative code
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with ID {id} was not found"}
    return post
    
## SQL GET{ID} query
# must be int in fuction so that user is forced to enter int, not str, do not need a commit() since we are not making a change
# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s; """, (str(id)),)
#     fetched_post = cursor.fetchone()
#     if not fetched_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found")
#         # alternative code
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with ID {id} was not found"}
#     return {"post_detail": fetched_post}


## ORM DELETE query
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # see SQLAlchemy Documentation for explaination
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## SQL DELETE query
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     # deleting post
#     cursor.execute("""DELETE FROM posts where id = %s RETURNING *;""", (str(id)),)
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

## ORM UPDATE query
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post
    

## SQL UPDATE query
# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     return {"data": updated_post}