from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.database import get_session
from api.models import Tag

router = APIRouter()


@router.get("/api/tags")
def get_tags(session: Session = Depends(get_session)):
    try:
        return session.exec(select(Tag)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/api/tags")
def new_tag(new_tag: str, session: Session = Depends(get_session)):
    print(new_tag)
    try:
        tag_to_create = Tag(id=new_tag)
        ret = tag_to_create.model_copy()

        session.add(tag_to_create)
        session.commit()
        return ret
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
