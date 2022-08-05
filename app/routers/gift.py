from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/gifts/{event_id}")
def read_gifts(event_id: int, offset: int = 0, limit: int = 100, db: Session = Depends(get_db), q: Optional[str] = None):
    gifts = crud.get_gifts(db=db, event_id=event_id, offset=offset, limit=limit)
    return {"gift_list":gifts}

@router.get("/gift/{code_id}", response_model=schemas.Gift)
def read_gift(code_id: str, db: Session = Depends(get_db)):
    return crud.get_gift(db=db, code_id=code_id)

@router.post("/gift/{code_id}/use", response_model=schemas.Gift)
@router.patch("/gift/{code_id}/use", response_model=schemas.Gift)
def use_gift(code_id: str, use_gift: schemas.GiftUse, db: Session = Depends(get_db)):
    gift = crud.get_gift(db=db, code_id=code_id)
    e_detail = None
    now = datetime.now()
    if not gift:
        e_detail = "Gift not found"
    elif gift.used == True:
        e_detail = "Already Used Gift code"
    elif gift.start_at > now or gift.finish_at < now:
        e_detail = "expired gift"
    
    if e_detail != None:
        raise HTTPException(status_code=404, detail=e_detail)

    gift.used = True
    gift.used_at = now
    gift.user_pid = use_gift.user_pid
    gift.user_platform = use_gift.user_platform
    gift.use_info = use_gift.use_info
    db.commit()
    db.refresh(gift)

    return gift

@router.get("/user/{user_pid}", response_model=schemas.Gift)
def chk_user(user_pid: str, db: Session = Depends(get_db)):
    gift = crud.get_gift_by_user(db=db, user_pid=user_pid)

    if not gift:
        raise HTTPException(status_code=404, detail="Can not find user pid in gifts")

    return gift