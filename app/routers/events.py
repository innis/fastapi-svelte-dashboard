from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from starlette.responses import FileResponse
from datetime import datetime, timezone, timedelta
import csv, os, glob

from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..utils import code_generator

router = APIRouter()

@router.get("/events/")
def read_events(offset: int = 0, limit: int = 100, db: Session = Depends(get_db), q: Optional[str] = None):
    events = crud.get_events(db=db, offset=offset, limit=limit)
    return {"event_list":events}

@router.post("/event/", response_model=schemas.Event)
def new_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)

@router.get("/event/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return crud.get_event(db=db, event_id=event_id)

@router.patch("/event/{event_id}", response_model=schemas.Event)
def patch_event(event_id: int, update_event: schemas.EventUpdate, db: Session = Depends(get_db)):
        
    event = crud.get_event(db=db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event_data = update_event.dict(exclude_unset=True)
    for key, value in event_data.items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)

    return event
    

@router.post("/event/{event_id}/make_gifts/")
def create_gifts(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event(db=db, event_id=event_id)

    e_detail = None
    if not event:
        e_detail="Event not found"
    elif event.start_at == None or event.finish_at == None:
        e_detail="Event info is invalid, check start or finish"
    elif event.gift_num <= event.gift_issued_num:
        e_detail="issued gift count is full"
    
    if e_detail != None:
        raise HTTPException(status_code=404, detail=e_detail)
    
    code_list = [code_generator() for _ in range(0,event.gift_num)]
    issued_count = 0
    try:
        issued_count = crud.create_multi_gifts(db=db, code_list=code_list, event_id=event.id, start_at=event.start_at, finish_at=event.finish_at)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"gift code insert error : {e}")

    if issued_count > 0:
        ret = crud.add_event_issued_count(db=db, event_id=event.id, count=issued_count)
        db.refresh(event)

    return {"event":event, "gift_list":code_list, "issued_count": issued_count}

@router.get("/events/{event_id}/download_gifts/")
def download_gifts(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event(db=db, event_id=event_id)
    d = timedelta(hours=9)

    for f in glob.glob("/tmp/*.csv", recursive=False):
        os.remove(f)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    gifts = crud.get_gifts_all(db=db, event_id=event_id)
    details = ["code", "event_id", "event_name", "start", "finish"]
    rows = [[c.code, event.id, event.name, c.start_at+d, c.finish_at+d] for c in gifts]

    file_location = f"/tmp/event_{event.id}.csv"

    with open(file_location, 'w') as f: 
        write = csv.writer(f) 
        write.writerow(details) 
        write.writerows(rows) 
    
    return FileResponse(file_location, media_type='application/octet-stream',filename=f"event_{event.id}_gifts.csv")