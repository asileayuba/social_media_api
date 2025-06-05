from typing import Dict

from fastapi import APIRouter, HTTPException

from storeapi.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()

post_table: Dict[int, UserPost] = {}
comment_table: Dict[int, Comment] = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn) -> UserPost:
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = UserPost(id=last_record_id, **data)
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = Comment(id=last_record_id, **data)
    comment_table[last_record_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [comment for comment in comment_table.values() if comment.post_id == post_id]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
