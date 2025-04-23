from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from src.api.database import get_session
from src.api.models import Tag

tag_router = APIRouter()


@tag_router.get("/api/tags")
def get_tags(session: Session = Depends(get_session)):
    try:
        tags = session.exec(select(Tag)).all()
        return tags
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


class TagPost(BaseModel):
    tag: str


@tag_router.post("/api/tags")
def new_tag(body: TagPost, session: Session = Depends(get_session)):
    try:
        tag_to_create = Tag(id=body.tag)
        ret = tag_to_create.model_copy()

        session.add(tag_to_create)
        session.commit()
        return ret
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
