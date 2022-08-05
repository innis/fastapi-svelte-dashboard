from pydantic import BaseModel, Field, ValidationError
from datetime import datetime, timezone, timedelta
from typing import Optional
from enum import Enum, IntEnum


class GiftBase(BaseModel):
    used: bool
    issued_at: datetime
    user_pid: str | None = None
    user_platform: str | None = None

class GiftUse(BaseModel):
    user_pid: str | None = None
    user_platform: str | None = None
    use_info: str

class GiftCreate(GiftBase):
    code: str
    event_id: int
    start_at: datetime
    finish_at: datetime

class Gift(GiftBase):
    code: str
    event_id: int
    start_at: datetime
    finish_at: datetime
    use_info: str | None = None
    used_at: datetime | None = None

    class Config:
        orm_mode = True

######################################################

class EventCategoryEnum(str, Enum):
    event_type = 'event'
    user_type = 'user'

class EventBase(BaseModel):
    desc: Optional[str] = None
    gift_num: Optional[int] = Field(
        2000,
        title='gift count',
        description='this is the value of gift count',
        ge=1,
        le=5000,
    )
    start_at: datetime| None = None
    finish_at: datetime| None = None

class EventUpdate(EventBase):
    pass

class EventCreate(EventBase):
    name: str
    category: EventCategoryEnum = EventCategoryEnum.event_type
    event_info: str
    class Config:
        schema_extra = {
            "example" : {
                "name" : "event name",
                "gift_num" : 2000,
                "desc" : "event description",
                "category" : EventCategoryEnum.event_type,
                "event_info" : "additonal infomation",
                "start_at" : datetime.now(),
                "finish_at" : datetime.now() + timedelta(days=365)
            }
        }

class Event(EventBase):
    id: int
    created_at: datetime | None = None
    start_at: datetime| None = None
    finish_at: datetime| None = None
    gift_num: int
    desc: str
    gift_used_num: int
    gift_issued_num: int
    #gifts: list[Gift] = []

    class Config:
        orm_mode = True