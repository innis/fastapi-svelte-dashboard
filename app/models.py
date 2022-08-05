from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    desc = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    start_at = Column(DateTime)
    finish_at = Column(DateTime)
    gift_num = Column(Integer, default=2000)
    gift_used_num = Column(Integer, default=0)
    gift_issued_num = Column(Integer, default=0)
    category = Column(String(10))
    event_info = Column(Text)

    gifts = relationship("Gift", back_populates="event")


class Gift(Base):
    __tablename__ = "gifts"

    code = Column(String(14), primary_key=True, index=True)
    used = Column(Boolean, default=False)
    issued_at = Column(DateTime, default=datetime.now())
    start_at = Column(DateTime)
    finish_at = Column(DateTime)
    use_info = Column(Text)
    user_pid = Column(String(100))
    user_platform = Column(String(100))
    used_at = Column(DateTime, default=None)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="gifts")