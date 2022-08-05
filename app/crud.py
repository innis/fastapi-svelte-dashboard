from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from datetime import datetime

from . import models, schemas
from .utils import code_generator

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Event).offset(offset).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(name=event.name, desc=event.desc, gift_num=event.gift_num)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def add_event_issued_count(db: Session, event_id: int, count: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).update({'gift_issued_num': models.Event.gift_issued_num + count})
    db.commit()
    return db_event


def get_gift(db: Session, code_id: str):
    return db.query(models.Gift).filter(models.Gift.code == code_id).first()

def get_gift_by_user(db: Session, user_pid: str):
    return db.query(models.Gift).filter(models.Gift.user_pid == user_pid).first()

def get_gifts(db: Session, event_id: int, offset: int = 0, limit: int = 100):
    return db.query(models.Gift).filter(models.Gift.event_id == event_id).offset(offset).limit(limit).all()

def get_gifts_all(db: Session, event_id: int):
    return db.query(models.Gift).filter(models.Gift.event_id == event_id).all()

def create_gift(db: Session, gift: schemas.GiftCreate, event_id: int):
    code = code_generator() # TODO gift_id 가 중복이 있는지 체크하여야 함
    db_gift = models.Gift(**gift.dict(), code=code ,event_id=event_id)
    db.add(db_gift)
    db.commit()
    db.refresh(db_gift)
    return db_gift

def create_multi_gifts(db: Session, code_list: list, event_id: int, start_at: datetime, finish_at: datetime):

    # code 겹침 충돌이 나면 어쩌야 하나....
    gift_list = [models.Gift(code=code, event_id=event_id, start_at=start_at, finish_at=finish_at) for code in code_list]

    db.bulk_save_objects(gift_list)
    db.commit()
    
    gift_count = db.query(models.Gift).filter(models.Gift.event_id == event_id).count()

    return gift_count